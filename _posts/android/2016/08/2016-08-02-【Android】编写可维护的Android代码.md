---
layout: post
title:  "【Android】编写可维护的Android代码"
date:   2016-08-02 08:00:00 +0800
categories: android
tag: [android]
---

让一个程序可维护是多方面的，本文不谈各种模式，只谈原则。兴起随笔，勿喷。。

## 模块之间的通信，基于接口的通信，用方法来表明意图，而不是用参数来表明意图

比如发送消息

```java

    public static final int MSG_START = 0;
    public static final int MSG_STOP = 1;

    // start
    Message.obtain(handler, MSG_START).sendToTarget();
    
    // stop
    Message.obtain(handler, MSG_STOP).sendToTarget();
    
```
   
更容易维护的代码：

```

    private static final int MSG_START = 0;
    private static final int MSG_STOP = 1;

    // start
    public void start(){
        Message.obtain(handler, MSG_START).sendToTarget();
    }
    
    // stop
    public void stop(){
        Message.obtain(handler, MSG_STOP).sendToTarget();
    }

```

## 隐藏细节

BroadcastReceiver 的例子

```java
public abstract class BroadcastReceiverA extends BroadcastReceiver {

    static final String ACTION_A = "action.a";
    private IntentFilter mIntentFilter;

    public CityBroadcastReceiver() {
        mIntentFilter = new IntentFilter();
        mIntentFilter.addAction(ACTION_A);
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        final String action = intent.getAction();
        if (TextUtils.isEmpty(action)) {
            return;
        }

        switch (action) {
            case ACTION_A:
                onActionXXX(context);
                break;
        }
    }

    public final void register(Context context) {
        FireFlyBroadcastManager.getInstance(context).registerReceiver(this, mIntentFilter);
    }

    public final void unRegister(Context context) {
        FireFlyBroadcastManager.getInstance(context).unregisterReceiver(this);
    }

    protected void onActionXXX(Context context, Intent intent) {

    }
}
```

出发点就是将注册，接收，解析的各个部分都封装在一起，即，相关的责任交由相关的组件处理。
当然，这个例子里面每个广播都会使用一个 IntentFilter，加重了系统负担，但是你可以通过合适的设计，使用一个广播持有集合来管理所有的接口。
总而言之，这里主要想说明的是，在责任划分完毕之后，隐藏细节。
    
## 用层次来构建人与机器的桥梁

通常一个 app 的数据流向是

    Server <--> App <--> User

这个时候，程序员至少应该构建两层抽象，分别对应：

代码与接口之间的抽象：

    Server <--> App 
    
代码与需求之间的抽象：

    App <--> User

而后者的优先级更高，所以，需要先制定代码与需求之间的抽象。比如有个用户登陆的需求，要求功能：

1. 注册
2. 登录
3. 退出登录

这个时候，需要构建的抽象就是：

```java
    UserMgr:
        register()
        login()
        logout()
```
用户的每一步操作，我们都只需要调用对应的方法而已。至于方法内部怎么实现，那是另一层抽象的问题。


待补充，待整理。。。


