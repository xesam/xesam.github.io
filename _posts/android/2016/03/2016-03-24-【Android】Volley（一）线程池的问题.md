---
layout: post
title:  "【Android】Volley（一）线程池的问题"
date:   2016-03-24 13:46:04 +0800
categories: Android
---
# Volley（一）线程池的问题

Volley 中有一个专门负责处理网络请求的线程池。
虽说是线程池，但是实际上是一个默认长度为 4 的线程数组，然后使用一个 BlockingQueue 来保存请求列表，是一个典型的生产-消费者模式应用。

```java

DEFAULT_NETWORK_THREAD_POOL_SIZE = 4;
NetworkDispatcher[] mDispatchers = new NetworkDispatcher[DEFAULT_NETWORK_THREAD_POOL_SIZE];

// Create network dispatchers (and corresponding threads) up to the pool size.
for (int i = 0; i < mDispatchers.length; i++) {
    NetworkDispatcher networkDispatcher = new NetworkDispatcher(mNetworkQueue, mNetwork,
            mCache, mDelivery);
    mDispatchers[i] = networkDispatcher;
    networkDispatcher.start();
}
```

我阅读源码的一个问题是：为什么不直接使用 java 并发包里面的 Executor 来处理线程池的问题？
这个问题并没有官方的正式回复，所以，也没有一个具体的答案。所以我只能对比一下两种实现方式的优缺点，来谈一下自己的看法。

首先需要明确的就是：Volley 的设计意图是适用于“小而频繁”的网络请求场景。

## 使用线程数组的优点

1. 这样实现的代码比较简单，可以有完全的控制，可以比较方便的对任务线程进行定制。
2. 由于一开始就保证会有 4 个（默认数量）线程贯穿整个生命周期，因此免除了动态创建或者回收线程的开销。
如果对应用的网络请求有一个比较好的评估，那么具体的线程数量还可以再斟酌。

其他，我找不到比较好的理由，因为，相同的功能使用 Executor 也完全可以实现。

## 使用线程数组的缺点

我们在使用过程中，通常是在 app 启动的时候进行 Volley 请求队列初始化，在应用结束的时候销毁 Volley 请求队列。那么，在使用的生命周期过程中，可能出现下面几个问题：

1. 当请求数量持续超负荷的时候，无法自动调整线程数量。由于使用的数组形式，并且也没有提供动态容量控制机制，无法根据实际情况伸缩应对。
这个时候就有可能导致请求的超预期延迟，特别是在网络状况不是很好（会触发 retry 机制，占用线程资源）而用户刷新比较频繁的场景下，表现会比较突出。
2. 如果某个线程由于某种异常被终止，将无法再次恢复，这个问题在 Volley 中并没有处理过。
一个极端情况是，如果默认的线程全部死掉，那么网络请求将崩溃。

另外，Volley 内置了对网络图片的请求处理，但是需要注意的是，
如果图片比较大或者比较多的情况下，需要在主要的 Volley 业务请求队列之外，重新开一个新的图片请求队列来处理,不然，极有可能阻塞了正常的业务请求。
其实个人觉得，Volley 没必要增加对图片的处理，既没有处理好，又不够强大。还是使用专业的 Glide 或者 Fresco 来处理。

可能这些情况比较极端，但是都是可能出现问题的地方。所以，个人觉得，Volley 还是有很大的改进空间的。
