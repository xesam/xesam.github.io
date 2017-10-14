---
layout: post
title:  "【Android】前后台切换监听"
date:   2016-03-07 12:46:04 +0800
categories: android
tag: [android]
---

# 【Android】前后台切换监听

Android 本身并有提供这样的监听，所以就只能走偏门了。

首先，需要定义一下，什么叫“前台”，什么叫“后台”。本文定义如下：

前台

    Activity 处在 FOREGROUND 优先级

后台

    App进程没有停止，除去在“前台”的所有情况

所以，退到后台的方式太多了，大致有：

1. 按Home键
2. 按“最近任务”键
3. 从通知栏启动其他应用
4. 从应用内部启动其他应用
5. 关掉屏幕

既然是监听变化，所以肯定是在相关生命周期的回调中来进行处理。ActivityA 启动 ActivityB 的生命周期方法调用顺序如下：

    ActivityA#onPause -> ActivityB#onStart -> ActivityB#onResume -> ActivityA#onStop

从 ActivityB 回退到 ActivityA 的生命周期方法调用顺序如下：

    ActivityB#onPause -> ActivityA#onStart -> ActivityA#onResume -> ActivityB#onStop -> ActivityB#onDestroy


一个思路就是通过统计当前活动的 Activity 数目来计算。

在 Activity#onStart 中来检测前一个状态是否是“后台”，如果是，则触发“切换到前台”事件，并将活动 Activity 数目加1。
在 Activity#onStop 中并将活动 Activity 数目减1。如果活动的 Activity 数目等于0，
就认为当前应用处于“后台”状态， 并触发“切换到后台”事件。

所以，一个初步方案大致是，实现一个基类 BaseActivity，并重写以下 onStart 和 onStop 回调方法：

```java
    private static int compatStartCount = 0;
    private static boolean isCompatForeground = true;

    @Override
    public void onStart() {
        super.onStart();
        compatStartCount++;
        if (!isCompatForeground) {
            isCompatForeground = true;
            onBackgroundToForeground(activity);
        }
    }
    
    @Override
    public void onStop() {
        super.onStop();
        compatStartCount--;
        if (compatStartCount == 0) {
            isCompatForeground = false;
            onForegroundToBackground(activity);
        }
    }
```

## 开始趟坑

1. 在关掉/点亮屏幕的情况下，android3 之前不会触发 onStart 和 onStop 回调。只会触发 onPause 和 onStop。所以以上代码失效。
按理来说，这应该是 Android 的含糊之处，onStop 的触发时机定义如下：

        Called when you are no longer visible to the user
    
按理来说，屏幕关闭的时候也符合条件，但是 android3 之前并未按照如此定义而来。所以需要 hack 一下：

```java
    private static boolean isCompatLockStop = false;

    private static boolean isStandard() {
        return Build.VERSION.SDK_INT >= Build.VERSION_CODES.HONEYCOMB;
    }
    
    public static boolean isInteractive(Context context) {
        PowerManager pm = (PowerManager) context.getSystemService(Context.POWER_SERVICE);
        if (Build.VERSION.SDK_INT >= VERSION_CODES.KITKAT_WATCH) {
            return pm.isInteractive();
        } else {
            return pm.isScreenOn();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (isStandard()) {
            //np
        } else {
            if (isCompatLockStop) {
                isCompatLockStop = false;
                onStart();
            }
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (isStandard()) {
            //np
        } else {
            if (!isInteractive(activity)) { //锁屏触发
                isCompatLockStop = true;
                onStop();
            }
        }
    }
``` 

对于 android3 之前的系统，我们在 onPause 中处理 锁屏问题，如果 onPause 被触发的时候，手机处于 “非交互” 状态，就认为是按下了电源键（或者其他锁屏方式），触发“后台”状态。
在 onResume 中判断如果是从锁屏界面恢复，则回到“前台”状态。

存在问题：点亮屏幕的时候就被认为回到“前台”状态，这个暂未找到好的方法避免。

2. 快速锁屏/点亮的情况下，会多次触发生命周期回调。

这个问题在 nexus 5 （Android 6.0） 上稳定重现，重现步骤：关掉屏幕后快速点亮再快速关闭。本来预期的表现应该是：
    
    onPause
    onStop

但是实际的表现如下：

    onPause
    onStop
    onStart
    onResume
    onPause
    onStop

所以，最终结果就是：
    
    前台 -> 后台
    后台 -> 前台 
    前台 -> 后台
    
多了一个周期。

这个问题我还没有解决。尝试过解决办法有：

1.在 onStart 中判断 inKeyguardRestrictedInputMode 状态：

```java
    public static boolean inKeyguardRestrictedInputMode(Context context) {
        KeyguardManager keyguardManager = (KeyguardManager) context.getSystemService(Context.KEYGUARD_SERVICE);
        return keyguardManager.inKeyguardRestrictedInputMode();
    }
``` 

在锁屏状态下就不触发计数。但是这个判断根本不可信，在快速切换的情况下，在非锁屏情况下返回 true 的几率也比较大。

2. 网上有一种判断应用是否在前台的方法

```java
    public boolean isAppOnForeground() {
    
        ActivityManager activityManager = (ActivityManager) getApplicationContext().getSystemService(Context.ACTIVITY_SERVICE); 
        String packageName = getApplicationContext().getPackageName(); 
        
        List<ActivityManager.RunningAppProcessInfo> appProcesses = activityManager 
            .getRunningAppProcesses(); 
        if (appProcesses == null) 
          return false; 
        
        for (ActivityManager.RunningAppProcessInfo appProcess : appProcesses) { 
          // The name of the process that this object is associated with. 
          if (appProcess.processName.equals(packageName) 
              && appProcess.importance == ActivityManager.RunningAppProcessInfo.IMPORTANCE_FOREGROUND) { 
            return true; 
          } 
        } 
        return false; 
    } 
``` 

但是这种测试方法并不靠谱，比如在魅族手机上，锁屏状态下也是返回 true。

3. 监听 ACTION_USER_PRESENT， ACTION_SCREEN_ON， ACTION_SCREEN_OFF 等事件。

回调事件比较晚，在生命周期中已经跑完好几圈之后，广播才接收到。而且在各个生命周期内无法判断是否因为锁屏导致的周期变化。

顺便说一下， ACTION_USER_PRESENT 和 ACTION_SCREEN_ON 存在下面几种情况:

1. 只触发 ACTION_SCREEN_ON
2. 先触发 ACTION_SCREEN_ON，再触发 ACTION_USER_PRESENT （电源键，然后解锁）
3. 先触发 ACTION_USER_PRESENT，再触发 ACTION_SCREEN_ON （指纹解锁）

这样的话，无法通过简单的计数来判断，需要加入 hashCode 来处理。

所以最终这种快速切换的情况被我忽略了，因为无非就是多了一个周期而已。

## 不完美实现

对于 API>=14 的系统上，可以直接增加 ActivityLifecycleCallbacks 监听，这样可以省去定义 BaseActivity 的步骤，减少侵入性。

所以在 API>=14 的系统上，直接使用 ActivityLifecycleCallbacks， 如果需要兼容 2.3，那么还是需要抽象出 BaseActivity。

演示代码地址 ： [https://github.com/xesam/AppMonitor](https://github.com/xesam/AppMonitor)

