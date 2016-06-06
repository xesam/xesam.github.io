---
layout: post
title:  "【Android】Handler（三）WeakHandler"
date:   2016-04-24 00:00:00 +0800
categories: android
tag: [android]
---
# 【Android】Handler（三）WeakHandler

本文是对 [https://github.com/badoo/android-weak-handler](https://github.com/badoo/android-weak-handler) 的原理讲解。

在 [Handler（一）内存泄漏](http://xesam.github.io/android/2016/03/27/Android-Handler-%E4%B8%80-%E5%86%85%E5%AD%98%E6%B3%84%E6%BC%8F.html) 中已经清除，
匿名内部类隐式持有外层对象的强引用是导致内存泄漏的一个主因。比如下面的例子：

```java
public class TActivity extends Activity {
    private Handler mHandler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mHandler = new Handler();
        mHandler.postDelayed(new Runnable() {
            @Override
            public void run() {
                Log.d("task", "task finished");
            }
        }, 10000);

    }
}

```
其中 Runnable 就隐式持有外层 TActivity 的引用。除了前文讨论过的在 TActivity 销毁的时候清空消息队列，还有没有其他更自动化的方法呢？

我们先看一下上面代码中的引用关系是怎样的：

![1]({{ site.baseurl }}/image/android-handler-3-1.png)

既然问题是由强引用导致的，那么，我们就看看是不是有办法将强引用替换为弱引用来解决这个问题。下面开始尝试：

### 1. 将隐式的强引用转换为隐式的弱引用

这个是语言机制，根本没办法修改，所以行不通。

### 2. 将对 Runnable 的强引用转换为对 Runnable 的弱引用

这里实际持有 Runnable 的是 Message，所以我们可以让 Message 持有对 Runnable 弱引用，而不是现在的强引用。
原始代码如下：

```java
    public final boolean postDelayed(Runnable r, long delayMillis){
        return sendMessageDelayed(getPostMessage(r), delayMillis);
    }
    
    private static Message getPostMessage(Runnable r) {
        Message m = Message.obtain();
        m.callback = r;
        return m;
    }
```

按照我们改造 Runnable 弱引用的思路， 稍微修改一下：

```java
class WeakHandler {
    static class WeakRunnable implements Runnable {
        private WeakReference<Runnable> mRunnable;

        public WeakRunnable(Runnable runnable) {
            this.mRunnable = new WeakReference<>(runnable);
        }

        @Override
        public void run() {
            Runnable runnable = mRunnable.get();
            if (runnable != null) {
                runnable.run();
            }
        }
    }

    private Handler mHandler;

    public WeakHandler() {
        mHandler = new Handler();
    }

    public final boolean postDelayed(Runnable r, long delayMillis) {
        WeakRunnable weakRunnable = new WeakRunnable(r);
        return mHandler.postDelayed(weakRunnable, delayMillis);
    }
}
```

这样行不行呢，显然是不行的。

因为在这种情况下，引用情况如下：

![1]({{ site.baseurl }}/image/android-handler-3-2.png)

上图说明，就算在 Activity 还没有被销毁的时候，也只有一个弱引用持有 Runnable ，也就以意味着这个 Runnable 随时都会被回收，这显然不符合我们的意图。
因此，我们还需要想办法在 Activity 存活的时候，保证 Runnable 也一定存活。
因此，只需要让 Activity 持有 Runnable 的强引用即可，为了方便，这个任务交给 WeakHandler 来处理，因为 Activity 直接持有 WeakHandler，如果 WeakHandler 也直接持有 Runnable，
效果就相当于 Activity 直接持有 Runnable。

修改如下，在 WeakHandler 里面保持一个实际的 Runnable 集合，这样就可以避免 Runnable 被回收。 
在实际的 Runnable 执行完毕后，将 Runnable 从集合中移除，释放不必要的资源。
当然，这一步的释放与 Activity 销毁并没有关系，因为如果 Activity 被销毁，这个 Runnable 集合一样会被回收。

![1]({{ site.baseurl }}/image/android-handler-3-3.png)

```java
public class WeakHandler {

    private static class RunnableRefs {
        private List<Runnable> mRunnables = new ArrayList<>();

        public RunnableRefs() {
        }

        public void add(Runnable runnable) {
            mRunnables.add(runnable);
        }

        public void remove(Runnable runnable) {
            mRunnables.remove(runnable);
        }
    }

    private static class WeakRunnable implements Runnable {
        private RunnableRefs mRunnableRefs;
        private WeakReference<Runnable> mRunnable;

        public WeakRunnable(Runnable runnable, RunnableRefs runnableRefs) {
            this.mRunnableRefs = runnableRefs;
            this.mRunnable = new WeakReference<>(runnable);
            mRunnableRefs.add(runnable);
        }

        @Override
        public void run() {
            Runnable runnable = mRunnable.get();
            if (runnable != null) {
                mRunnableRefs.remove(runnable);
                runnable.run();
            }
        }
    }

    private RunnableRefs mRunnableRefs;
    private Handler mHandler;

    public WeakHandler() {
        mHandler = new Handler();
        mRunnableRefs = new RunnableRefs();
    }

    public final boolean postDelayed(Runnable r, long delayMillis) {
        WeakRunnable weakRunnable = new WeakRunnable(r, mRunnableRefs);
        return mHandler.postDelayed(weakRunnable, delayMillis);
    }

}
```

上面有一步需要重视：

Activity 直接持有 WeakHandler，如果 WeakHandler 也直接持有 Runnable。

这句话的意思就是要求 WeakHandler 是 Activity 的一个实例变量。不然类似下面的写法

```java
    new WeakHandler().postDelayed(new Runnable() {

        @Override
        public void run() {
            //xxxx
        }
    }, 50_000);
```

WeakHandler 是一个局部变量，等方法执行完毕，WeakHandler 就被回收了。等待执行的 Runnable 又成了一个孤儿。

## 总结

java 的回收机制依赖于引用，而引用的根节点最后都会落到线程上面，如果想让 jre 自动回收某一个对象或者一组对象，
那就让这一组对象相互之间形成一个自封闭空间就行了。
也就是说，让根节点无法通过强引用搜索找到这组对象，就像现实中一样，封闭的小团体圈子，一旦上头没有人，自然就被打掉了。

当然，原理归原理， GC 的时机是没法控制的，所以，最保险的时机还是手动清空 Handler 的消息队列，个人认为，这样才靠谱。


