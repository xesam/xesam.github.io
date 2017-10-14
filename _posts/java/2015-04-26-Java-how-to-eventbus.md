---
layout: post
title:  "【Java】如何实现一个简单的事件总线"
date:   2015-04-26 12:46:04 +0800
categories: java
tag: [java]
---

# 【Java】如何实现一个简单的事件总线

[MicroBus](https://github.com/konmik/MicroBus)

##使用

注册

```java
    class Receiver implements MicroBus.BusEventReceiver {

        public onCreate() {
            bus.register(this, String.class);
        }

        public onDestroy() {
            bus.unregister(this, String.class);
        }

        @Override
        public void onBusEvent(Object event) {
            if (event instanceof String)
                System.out.println("Hello, " + event);
        }
    }
```

运行

    bus.post("World|");

运行结果

    Hello, World!

## 大致原理

使用一个队列来保存所有的注册对象，一旦有新事件产生，就遍历这个队列，找到对此事件感兴趣的注册对象，并执行相应的动作。

不过这个实现并不能适用于生产环境，也缺乏对多线程以及线程调度的支持，但是很适合理解设计原理。

## 后记

通常的观察者模式有个问题，就是业务对象依旧是直接通信，一旦通信数量骤增，那么相互的依赖关系就会陷入难以整理的网状结构。

“事件” 本身就是 “消息”，总线只不过是将业务对象之间的直接消息通信转移到总线统一调度的消息通信上而已，使用单点通信来取代网状通信，降低消息管理的复杂度。

同时，使用消息取代显式的接口，消息可以有统一的格式，统一的格式意味着可以方便的制定协议，也就意味这可以在更广泛的范围传递，这对分布式应用是大有裨益的。

另一个好处就是，可以更方便的实现异步处理，不论是发布事件还是接收事件，都可以等到有在所有的条件都准备完全之后，再由事件总线来调度，避免无谓的阻塞。







