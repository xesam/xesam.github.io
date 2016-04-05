---
layout: post
title:  "【Android】Handler（二）Message面面观"
date:   2016-04-01 00:00:00 +0800
categories: Android
---
# 【Android】Handler（二）——Message面面观

## Message 有几种？
Message 有两种：Data Message（数据消息） 与 Task Message（任务消息）

Data Message 是指有携带多个数据参数的 Message。比如：

```java
    public static Message obtain(Handler h, int what, int arg1, int arg2, Object obj)
```
其中 arg1， arg2，以及 obj 都是携带的数据。

Task Message 是指发送一个 Runnable 的 Message。比如：

```java
    public static Message obtain(Handler h, Runnable callback)
```
其中 callback 就是消息携带的任务。

注意，一个 Message 不可能同时为 Data Message 和 Task Message，而只能是其中之一。
当然，你可以强制给一个 Message 设置所有的属性，但是只会有一种类型起作用。

## Message 的特征属性是什么？即，如何区分 Message？

一个 Message 包含四个方面：

1. Handler # 必须——消息的接收者，同时也是消息的管理者。
2. Object # 非必须——消息的 token

3. Integer # 非必须——数据消息独有
4. Runnable # 非必须——任务消息独有

因此，对于所有的 Message 来说，只要其中任意一个属性不相同，就是不同的 Message。因此，像下面的情况，是不会发生冲突的 。

```java
    Message.obtain(handler1, 1).sendToTarget();
    Message.obtain(handler2, 1).sendToTarget();
```

## 如何创建 Message

第一种方式，可以直接 new 一个 Message 对象：

```java
    Message message = new Message();
    message.what = 1;
    message.setTarget(handler1);
    message.sendToTarget();
```
但是这种方式有两个缺点：

1. 只能创建 Data Message， 无法创建 Task Message
2. 每次都创建新的 Message 会增加系统资源。

第二种方式，从消息池里面重用取出。

系统内部维护了一个消息池，推荐的做法是每次需要的时候就从消息池里获取一个，然后系统会自动回收重用。
因此，上面的调用可以修改为：

```java
    Message.obtain(handler1, 1).sendToTarget();
```

而且这种方式也可以创建 Task Message：

```java
    Message.obtain(handler1, new Runnable() {
        @Override
        public void run() {
            
        }
    });
```

第三种方式，从另一个消息拷贝而来：

```java
    Message.obtain(message).sendToTarget();
```

## 如何发送 Message

消息最终的接受者肯定是一个 Handler，因此，Message 的四特征里面，Handler必不可少。
发送消息有两种方式，从 Message 发送：

```java
    Message.obtain(handler1, 1).sendToTarget();
```    

从 Handler 发送：

```java
    new Handler().post(new Runnable() {
        @Override
        public void run() {
    
        }
    });

    //或者

    new Handler().sendEmptyMessage()
```

有一个简单的区分：

send 前缀的方法用来发送 Data Message

post 前缀的方法用来发送 Task Message

本质上，以上两种方式是一样的，因为 Message.sendToTarget() 方法最终还是委托给内部的 Handler 来处理，这么做只是使用起来更方便而已。

而返回值（boolean）都是用来表明消息是否成功发送。

## Message 的处理

Task Message 会在指定的时间直接在 Handler 线程被执行，Handler 本身无法接收到任何回调。

而对于 Data Message 来说，处理方法就比较丰富一些了。Handler 通过 

```java
    Handler.handleMessage(Message msg)
```
来处理。

Handler 处理的方式也有两种：

第一种，通过继承的方式：

```java
    public static class CbkHandler extends Handler {
    
        @Override
        public void handleMessage(Message msg) {
            //handle message
        }
    }
```

第二种，通过回调的方式：

```java
    new Handler(new Handler.Callback() {
        @Override
        public boolean handleMessage(Message msg) {
            //handle message
            return true;
        }
    });
```
对于第二种方式的返回值，true 表示已经处理了消息， false 表示没有处理消息。如果没有处理消息，那么消息将会被投递到 Handler 本身的 handleMessage(Message msg) 方法，也就是第一种方式。

## 如何移除消息

移除 Message 同样要参考 Message 的四个特征。只要相应的特征符合，就可以移除对应的消息。

移除 Data Message 使用 removeMessages 方法：

```java
    Handler.removeMessages(int what) //移除所有 what 值匹配的 Message
    Handler.removeMessages(int what, Object token) //移除所有 what 值匹配并且 token 也相同的 Message
```

移除 Task Message 使用 removeCallbacks 方法：

```java
    Handler.removeCallbacks(Runnable r) //移除所有 r 相同的 Message
    Handler.removeCallbacks(Runnable r, Object token) //移除所有 r 相同并且 token 也相同的 Message
```

由于 token 是两类消息共有的，因此，可以通过 token 来同时移除两类消息：

```java
    removeCallbacksAndMessages(Object token) //移除所有 token 相同的 Message
```

如果 token 为 null，效果就是清空所有的消息队列。

## Message 的生命周期

![1]({{ site.baseurl }}/image/message_lifecycle.png)

注意，在正式的程序开发中，是没有手段来检测 Message 的生命周期状态的。而且，也不应该持续持有一个 Message，更不应该在一个 Message 发送之后，再对其进行修改。
因为，既无法确认 Message 的状态，而且 Message 有可能被重用，会直接影响到下一个处理逻辑。

## 观察 Message Queue

系统提供了两种方式来观察当前消息队列的情况：

第一种，在 Handler 上调用 Handler.dump(Printer pw, String prefix) 来输出当前的消息队列情况：

```java
    handler.dump(new LogPrinter(Log.DEBUG, "HandlerDemo"), "xesam");
```
示例结果如下；
    
    xesam  Looper (main, tid 1) {44bd1af0}
    xesam    Message 0: { when=-9ms barrier=62 }
    xesam    Message 1: { when=+10s0ms callback=dev.xesam.android.demo.system.handler.HandlerDemo$2 target=android.os.Handler callback=dev.xesam.android.demo.system.handler.HandlerDemo$2@44d5ae18 target=Handler (android.os.Handler) {44bd7758} }
    xesam    (Total messages: 2, idling=false, quitting=false)


第二种，可以使用 Looper#setMessageLogging(Printer printer) 来监控消息的处理过程。

```java
    Looper.myLooper().setMessageLogging(new LogPrinter(Log.DEBUG, "xesam"));
```
示例结果如下，展示了每一个 Message 的处理情况：

    D/xesam: >>>>> Dispatching to Handler (android.os.Handler) {44d27750} dev.xesam.android.demo.system.handler.HandlerDemo$2@44d27a20: 0
    D/xesam: <<<<< Finished to Handler (android.os.Handler) {44d27750} dev.xesam.android.demo.system.handler.HandlerDemo$2@44d27a20

这是主要的调试手段，而且比较实用。

### 推荐书籍

[《Efficient Android Threading》](https://book.douban.com/subject/25900200/)
