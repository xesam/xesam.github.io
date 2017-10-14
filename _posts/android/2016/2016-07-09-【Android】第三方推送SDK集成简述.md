---
layout: post
title:  "【Android】第三方推送SDK集成简述"
date:   2016-07-09 18:20:04 +0800
categories: android
tag: [android]
---

由于我们 Android 应用的推送（Push）效果一直不是很理想，所以前段时间调研了现在国内市场上几种推送集成方案，大致包括：

1. 个推推送
2. 极光推送
3. 阿里云推送
4. 友盟推送。

不过鉴于混乱的 Android 局面来说， 各个推送效果都不算很好，也都是难兄难弟。

## 前言

就实现来说，iOS 的推送机制就很好，系统统一管理推送，然后分发给对应的应用，各个应用自己处理来自系统的推送消息。
这样既不用考虑应用进程的保活问题，也不用考虑无休止的兼容问题。

虽然小米或者华为之列有自己的系统推送，通知栏推送效果还好，至于透传推送，效果就呵呵了。
我们暂且不论效果，他们各自的不兼容不仅没有给开发者减压，还给 App 增加了压力。

举个例子，如果我针对 MIUI 包含 MIUI 的系统推送，并在小米应用市场上架，这样小米手机的用户推送就棒棒哒。

不过华为手机怎么办，那就集成华为的系统推送呗，然后在华为应用市场上架。

三星手机怎么办，一样啊，集成三星系统 SDK，在三星应用市场上架。

至于其他的应用市场，都用第三方 Push SDK 吧，毕竟要优先照顾主流手机厂商用户。

那么问题来了，如果各个应用市场相互抓包怎么办，比如一个应用市场抓取了小米应用市场的 APK， MIUI 用户下载了怎么办，或者 MIUI 用户从百度应用市场下载怎么办，这就尴尬了。
除非我在一个 APK 里面集成所有的第三方厂商的系统推送，然后还得外送一个第三方 Push SDK，不然就没法预防各种情况。所以最终还是只用第三方 Push SDK 简单。

国内太监 Android 应用的一部分保活需求，就来自推送，这样不但让系统背了锅，也恶心了自己，更恶心了用户。

## 集成指南

为了在各个 Push SDK 之间无缝切换，所以肯定会对 Push 层进行封装，另一个常见的需求是：

    当 Push 消息到达的时候，如果用户在接收消息界面，那就直接更新界面，如果用户不在接收消息界面，那就弹出通知栏提示。

所以，针对这样的现状与需求，大致的结构如下：

![android_push]({{ site.baseurl }}/image/android_push.png)

过程描述：

1. App 注册对应的 BroadcastReceiver，并定义不同的优先级，用以接收推送消息。
2. 第三方 Push SDk 接收到推送消息，解析之后，发送一个优先级系统广播。
3. Android 系统将广播将投递给对应的 App。
4. App 组件的 BroadcastReceiver 按照预定义的优先级来接收消息广播，如图，广播会一层层穿透各个组件的 BroadcastReceiver。
如果广播在传递过程中，被某个组件拦截并消费了，就停止传播，如果被最后一个 BroadcastReceiver，就进行收尾操作。
比如，如果当前的 Activity 接收了广播，弹出一个对话框，然后告知系统广播已经被消费即可；
如果没有任何 Activity 消费广播，最后一个 BroadcastReceiver 就可以接收广播，然后弹出一个通知栏消息，这样就满足需求了。

集成过程中的几个问题：

第一个问题，由于第三方推送过来的消息数据通常都格式不一，所以就需要将接收到的推送消息进行一道抽象，将第三方的数据包装成我们的语义对象。
这样屏蔽细节，也不扯什么设计模式了，反正在计算机工程应用方面，就是分层，分层，再分层。

第二个问题，第三方推送面向开发者的接收方式也不一样，比如个推是要求开发者继承一个 BroadcastReceiver 来接收消息，但是友盟要求开发者实现一个 PushHandler 来接收消息。
为了统一处理，我个人建议使用 BroadcastReceiver 的接收方式，因为在最终的处理流程中，依旧逃不过 BroadcastReceiver 的使用。

因此，整个设计中涉及到两种 BroadcastReceiver，第一种是用来统一接收第三方 Push 消息的，第二种是用来子在应用中处理接收到的消息的。

示例代码如下：

定义抽象数据消息：

```java
    //每个消息都会有类型
    class Msg{
        public int type;
    }

    final class MsgType{
        public static final int TYPE_USER_REPLY = 1;
    }

    //示例 用户回复
    public class UserReply extends Msg implements Parcelable{
        public String title;
        public long time;
    }
    
    //实现 Parcelable
    ...

```

定义接收第三方 Push 消息的 BroadcastReceiver，我称之为“标准” Push 接收器：

```java
    public class PushMsgBroadcastReceiver extends BroadcastReceiver{
    
        public static final String ACTION_RECEIVE_MSG = "dev.xesam.push.action.msg";
        public static final String EXTRA_RECEIVE_MSG = "dev.xesam.push.extra.msg";
    
        @Override
        public final void onReceive(Context context, Intent intent) {
            String message = intent.getStringExtra(EXTRA_RECEIVE_MSG);
        }
        
        public Msg parsePushMsg(String message){
            return ...
        }
        
        public void dispatchPushMsg(String message ){
            Msg msg = parsePushMsg(message);
            if(msg.type == MsgType.TYPE_USER_REPLY){
                //投递消息到相应的应用内 PushHandleReceiver
                Intent intent = new Intent();
                intent.setAction(PushHandleReceiver.ACTION_RECEIVE_MSG);
                intent.putExtra(PushHandleReceiver.EXTRA_RECEIVE_MSG, message);
                //注意，这里发送的是优先级广播
                context.sendOrderedBroadcast(intent, null);
            }else ...
        }
    }

```

个推本身就是用的 BroadcastReceiver，直接使用即可。至于友盟的推送,可以将 Push 消息转发到我们定义的 PushMsgBroadcastReceiver 上，其他的 sdk 可以类似处理：

```java

public class UmengHandler extends UmengMessageHandler {
    @Override
    public void dealWithCustomMessage(Context context, UMessage msg) {
        //将友盟的推送转化为广播的形式
        Intent intent = new Intent();
        intent.setAction(PushMsgBroadcastReceiver.ACTION_RECEIVE_MSG);
        intent.putExtra(PushMsgBroadcastReceiver.EXTRA_RECEIVE_MSG, message);
        context.sendBroadcast(intent);
    }
}

```

定义应用内各个组件用来处理消息的 BroadcastReceiver ：

```java

public class PushHandleReceiver extends BroadcastReceiver {

    public static final String ACTION_RECEIVE_MSG = "dev.xesam.app.action.msg";
    public static final String EXTRA_RECEIVE_MSG = "dev.xesam.app.extra.msg";

    @Override
    public final void onReceive(Context context, Intent intent) {
        Msg msg = intent.getParcelableExtra(EXTRA_RECEIVE_MSG);
        boolean consumed = false;
        if(msg.type == MsgType.TYPE_USER_REPLY){
            consumed = onReceiveUserReply((UserReply) msg);
        }
        
        //如果广播被消耗，停止广播
        if(consumed){
            abortBroadcast();
        }
    }
    
    public boolean onReceiveUserReply(UserReply userReply){
        ...
    }

    ...
}

```

在上图的设计中，会有一个优先级最低，用来“兜底”的 BroadcastReceiver，用来在没人处理广播的情况下，将广播内容发送到通知栏消息。
我们可以将这个 BroadcastReceiver 注册到 AndroidManifest， 这样即使在用户没有启动的时候也可以接收并处理广播。

```java

public class LastHandleReceiver extends PushHandleReceiver {

    public boolean onReceiveUserReply(UserReply userReply){
        //这里将 UserReply 发送到通知栏
        return true;
    }

    ...
}

```

如果我们想在某个 Activity 处理广播，拦截即可，这样就可以在对应界面弹出一个对话框，而不会弹出通知栏：

```java

public class userActivity extends Activity {

    public PushHandleReceiver mUserHandleReceiver new PushHandleReceiver() {
    
        public boolean onReceiveUserReply(UserReply userReply){
            showDialog(userReply);
            return true;
        }
    
        ...
    }

    public void onResume(){
        IntentFilter intentFilter=new IntentFilter();
        intentFilter.addAction(PushConstant.INTENT_ACTION_PUSH_DEMISE_REMINDER);
        intentFilter.addAction(PushConstant.INTENT_ACTION_PUSH_FEED);
        //优先级较高
        intentFilter.setPriority(99);
        context.registerReceiver(mUserHandleReceiver, intentFilter);
    }
    
    public void onPause(){
        context.unregisterReceiver(mUserHandleReceiver);
    }
    
    public void showDialog(UserReply){
        ...
    }
}

```

## 注意点

1. 第三方通常的接收消息里面通常不仅仅是你的应用消息，还有 SDK 自身的 push id 什么的，这个需要区分处理。
2. SDK 自身的 push id 获取时机各不相同，需要区分对待，如果你自己的后台想知道 push id，处理方式与上图类似。
3. 由于通知栏随时可能出现，所以面临的一个问题是点击通知栏之后怎么办。
这一个“回退栈”的交互问题，我个人偏好的是，点击通知栏之后直接打开 MainActivity， 在 OnNewIntent 回调中根据点击通知消息携带的 Intent 再来跳转到对应的界面，
就像微信一样，这样既可以避免回退之后直接退出应用的尴尬，也可以避免繁琐的应用栈判断，各自爱好，唯与产品经理 PK 而已。

以上只是一种设计方式，其他设计方式欢迎讨论。



###### Q群：315658668

