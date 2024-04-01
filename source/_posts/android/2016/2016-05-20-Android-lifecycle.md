---
layout: post
title:  "Android 生命周期监听"
date:   2016-05-20 08:00:00 +0800
categories: android
tag: [android]
---
[navi](https://github.com/trello/navi)，这个库比较好玩，实现了我早就想要的一种开发方式：让组件主动监听 Activity 以及 Fragment 的生命周期，然后注册相应的回调。

在日常开发中，经常会有某些操作或者对象需要响应 Activity 以及 Fragment 的生命周期转换，这个时候要么我们得在 Activity 的生命周期方法里面主动来处理，
要么提供一个包装过的 Activity，让目标 Activity 继承这个包装 Activity，当然，实际上都是一样的。
比如，如果我们想在 OnResume 的时候开启一个定时任务，在 OnPause 的时候关闭定时器，我们会这么写：

```java

public class Main3Activity extends AppCompatActivity {
    HandlerTimer handlerTimer = new HandlerTimer();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main3);
    }

    @Override
    protected void onResume() {
        super.onResume();
        handlerTimer.start();
    }

    @Override
    protected void onPause() {
        super.onPause();
        handlerTimer.stop();
    }

    public static class HandlerTimer extends Handler {
        String TAG = getClass().getName();

        public HandlerTimer() {
        }

        @Override
        public void handleMessage(Message msg) {
            if (msg.what == 1) {
                Log.e(TAG, "Tick");
                sendEmptyMessageDelayed(1, 1000);
            }
        }

        public void start() {
            Log.e(TAG, "Start");
            sendEmptyMessageDelayed(1, 1000);
        }

        public void stop() {
            Log.e(TAG, "Stop");
            removeMessages(1);
        }
    }
}
```

这样写不仅特别繁琐，还需要各种第三方代码（这里是 HandlerTimer ）暴露每一个对应的生命周期方法。
于是，我们的考虑就是：这些响应生命周期状态转换的工作应该交给第三方代码自己去完成，第三方代码可以主动去监听 Activity 的生命周期变化，从而做出自己认为最合适的动作。

navi 就是基于这种目的而产生的。运用 navi， 上面的代码可以改写为：

```java
public class Main2Activity extends NaviAppCompatActivity {

    HandlerTimer handlerTimer = new HandlerTimer();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        handlerTimer.bind(this);
    }

    public static class HandlerTimer extends Handler {
        String TAG = getClass().getName();

        public HandlerTimer() {
        }

        @Override
        public void handleMessage(Message msg) {
            if (msg.what == 1) {
                Log.e(TAG, "Tick");
                sendEmptyMessageDelayed(1, 1000);
            }
        }

        public void bind(NaviAppCompatActivity activity) {

            activity.addListener(Event.RESUME, new Listener<Void>() {
                @Override
                public void call(Void aVoid) {
                    Log.e(TAG, "Start");
                    sendEmptyMessageDelayed(1, 1000);
                }
            });
            activity.addListener(Event.PAUSE, new Listener<Void>() {
                @Override
                public void call(Void aVoid) {
                    Log.e(TAG, "Stop");
                    removeMessages(1);
                }
            });
        }
    }
}
```

更多细节可以参考 navi 的示例与源码。

需要指出的是，个人觉得这个库还不是很完善，现在只能支持 Activity 和 Fragment，而且支持方式也略具侵入性。
尽管如此，这种设计我还是很喜欢的，把 Activity 变为一个纯容器，模式运用会更灵活，当然，坑也更多。














