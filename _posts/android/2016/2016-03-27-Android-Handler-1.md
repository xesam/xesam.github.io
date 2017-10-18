---
layout: post
title:  "【Android】Handler（一）内存泄漏"
date:   2016-03-27 13:46:04 +0800
categories: android
tag: [android]
---

内存泄漏的最终原因无非就是逻辑上应该被回收的资源实际上无法被回收。

如果我们将 Activity 看做一个封闭环境，那么导致内存泄漏的原因通常就是：实际上有外部环境中的其他存活对象持有这个逻辑上应该被回收的 Activity 的强引用。

回到 Handler，Handler 内部肯定不存在内存泄露的问题，那问题肯定处在我们的写法上，而主要的问题就是在延时 Message 中持有强引用。
因为虽然 Handler 跟随 Activity 的生命周期，但是 Message 却是跟随着执行线程的生命周期。

### 1. 显式引用

在延时回调中直接持有 Activity：

```java
    new Handler().postDelayed(new Runnable() {
        @Override
        public void run() {
            activity.setVisibility(View.VISIBLE);
        }
    }, 10000);
```

虽然使用了静态类，但是内部持有了 View， view 又持有外层 Activity 引用。

```java
    public static class CbkHandler extends Handler {

        private View mView;

        public CbkHandler(View view) {
            mView = view;
        }

        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            mView.setVisibility(View.VISIBLE);
        }
    }
    
    new CbkHandler(view).sendEmptyMessage(0);
```

### 2. 隐式引用

匿名内部隐式持有外层类的引用，比如 Runnable 持有外层类的引用，如果外层类是一个 Activity，那么这个 Activity 就只会在 10 秒之后才可能被回收。

```java
    new Handler().postDelayed(new Runnable() {
        @Override
        public void run() {
            //op
        }
    }, 10000);
```

## 如何解决

1. 及时清理延时 Message，如果没有延时 Message，那么顶多可能会存在短时间的内存泄漏，而不会产生大问题。此时的风险是，在 Message 中可能引用了已经被销毁的 View 或者其他，导致空指针。
2. 避免使用匿名内部类，在静态类中使用弱引用来引用外层的 View 或者 Activity。
3. 与第 2 条类似，但是是对整个 Runnable 对象持有弱引用，这样无论 Runnable 里面是怎样的，都不会影响到外层的内存回收。参见[android-weak-handler](https://github.com/badoo/android-weak-handler)。
weak-handler 的问题就是必须要求外层类持有 weak-handler 的强引用，不然 weak-handler 自身也会被回收掉。

## 补充

更多内存泄漏请参考：

1. [https://techblog.badoo.com/blog/2014/08/28/android-handler-memory-leaks](https://techblog.badoo.com/blog/2014/08/28/android-handler-memory-leaks)
1. [内存泄露从入门到精通三部曲之基础知识篇](http://bugly.qq.com/bbs/forum.php?mod=viewthread&tid=21&highlight=%E5%86%85%E5%AD%98%E6%B3%84%E9%9C%B2%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E7%B2%BE%E9%80%9A%E4%B8%89%E9%83%A8%E6%9B%B2%E4%B9%8B%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86%E7%AF%87)
2. [内存泄露从入门到精通三部曲之排查方法篇](http://bugly.qq.com/bbs/forum.php?mod=viewthread&tid=62&highlight=%E5%86%85%E5%AD%98%E6%B3%84%E9%9C%B2%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E7%B2%BE%E9%80%9A%E4%B8%89%E9%83%A8%E6%9B%B2%E4%B9%8B%E6%8E%92%E6%9F%A5%E6%96%B9%E6%B3%95%E7%AF%87)
3. [内存泄露从入门到精通三部曲之常见原因与用户实践](http://bugly.qq.com/bbs/forum.php?mod=viewthread&tid=125&highlight=%E5%86%85%E5%AD%98%E6%B3%84%E9%9C%B2%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E7%B2%BE%E9%80%9A%E4%B8%89%E9%83%A8%E6%9B%B2%E4%B9%8B%E5%B8%B8%E8%A7%81%E5%8E%9F%E5%9B%A0%E4%B8%8E%E7%94%A8%E6%88%B7%E5%AE%9E%E8%B7%B5)


