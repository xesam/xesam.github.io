---
layout: post
title:  "Android 定时任务"
date:   2015-07-17 12:46:04 +0800
categories: android
tag: [android]
---
基于Handler的Android定时器与倒计时器

源码地址：[Github AndroidTimer]( https://github.com/xesam/AndroidTimer)


## 特性

支持操作 :

1. start
1. pause
1. resume
1. cancel

### 注意
*以上方法是同步方法，请不要在回调方法里面调用以上方法。*

## 使用

### CountTimer

```java
    new CountTimer(100) {

        @Override
        public void onTick(long millisFly) { // millisFly is the Elapsed time at *Running State*
            vCountSwitcher.setText((millisFly) + "");
            Log.d("onTick", millisFly + "");
        }
    };
```

### CountDownTimer

```java
    new CountDownTimer(100) {

        @Override
        public void onTick(long millisUntilFinished) { // millisUntilFinished is the left time at *Running State*
            Log.d("onTick", millisFly + "");
        }

        @Override
        public void onCancel(long millisUntilFinished) {
        }

        @Override
        public void onPause(long millisUntilFinished) {
        }

        @Override
        public void onResume(long millisUntilFinished) {
        }

        @Override
        public void onFinish() {
        }
    };
```

## 使用一个 Handler 同时管理多个定时任务

创建多个任务：

```java
    MultiCountTimer multiCountTimer = new MultiCountTimer(10);
        multiCountTimer.registerTask(new CounterTimerTask(1) {
            @Override
            public void onTick(long millisFly) {
                vMulti1.setText("multi_1:" + millisFly);
            }
        }).registerTask(new CounterTimerTask(2, 100) {
            @Override
            public void onTick(long millisFly) {
                vMulti2.setText("multi_2:" + millisFly);
            }
        }).registerTask(new CounterTimerTask(3, 1000) {
            @Override
            public void onTick(long millisFly) {
                vMulti3.setText("multi_3:" + millisFly);
            }
        });

        multiCountTimer.startAll();
```

取消任务：

```java
    multiCountTimer.cancel(2);
    或者
    multiCountTimer.cancelAll();
```

## 截图

![timer](./timer.png)


参考自 Android SDK 中的 [CountDownTimer](http://developer.android.com/reference/android/os/CountDownTimer.html)
