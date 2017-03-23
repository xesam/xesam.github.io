---
layout: post
title:  "【Android】Pool"
date:   2017-03-21 13:46:04 +0800
categories: android
tag: [android]
---
在应用开发中，经常需要重复创建某些对象来传递消息或者执行操作，在使用完之后又随即废弃。这在某些情况下，会对系统性能造成一定的影响，特别是存在以下特征时：

1. 对象频繁创建但是只需要短暂使用
2. 对象的创建代价比较高。

比较典型的例子比如 Android 里面的 MotionEvent， 每次屏幕移动事件都会产生一个新的 MotionEvent，但是这个 MotionEvent 却只使用一次就废弃了。在比如数据库连接，连接数据库是非常耗时的，如果每次查询都创建一个连接，会产生显著的响应延迟。这个时候使用对象池化就是比较合适的选择。特别是在移动设备这种硬件资源紧张的系统中，池化技术更是无处不在。

对象池是一个保存可复用对象的容器，用户可以从池子中取得对象，对其进行操作处理，并在不需要时的时候将这个对象归还给池子，而不是让系统销毁它。我们区分一下，Java 对象的生命周期大致包括三个部分：

1. 对象的创建
2. 对象的使用
3. 对象的销毁

池化通过减少“对象的创建”和”对象的销毁”这两步的开销，进而降低资源消耗同时减少了响应时间。

不过同时，池化也引入了新的风险，既然池中的对象是复用的，那么这些对象先前的状态如何处理。此时，又需要将池化对象分两种：

1. 无状态对象。这种对象可以直接复用，因为每次使用的状态都是一样的。
2. 有状态对象。这种对象在取出（或者归还）的时候，都应该先将所有的对象重置，所以你在很多对象上能看到 recycle() 方法，这个对象很大程度上有可能就使用了池化技术。

## 对象池的实现
对象池的实现有很多，只需要实现最基本的“取出”和“归还”功能即可：

```java
interface Pool<T> {
  T	acquire()
  boolean	release(T instance)
}
```
一个简单的实现：

```java
public static class SimplePool<T> implements Pool<T> {
        private final Object[] mPool;

        private int mPoolSize;

        public SimplePool(int maxPoolSize) {
            mPool = new Object[maxPoolSize];
        }

        @Override
        @SuppressWarnings("unchecked")
        public T acquire() {
            if (mPoolSize > 0) {
                final int lastPooledIndex = mPoolSize - 1;
                T instance = (T) mPool[lastPooledIndex];
                mPool[lastPooledIndex] = null;
                mPoolSize--;
                return instance;
            }
            return null;
        }

        @Override
        public boolean release(T instance) {
            if (isInPool(instance)) {
                throw new IllegalStateException("Already in the pool!");
            }
            if (mPoolSize < mPool.length) {
                mPool[mPoolSize] = instance;
                mPoolSize++;
                return true;
            }
            return false;
        }

        private boolean isInPool(T instance) {
            for (int i = 0; i < mPoolSize; i++) {
                if (mPool[i] == instance) {
                    return true;
                }
            }
            return false;
        }
    }
```

上面其实是 Android v4 包里面的实现，整体就是用一个数组来保存复用对象，然后依次轮询。

## 什么时候不适合池化

1. 过于轻量级对象不适合池化，因为创建的开销可能比在池中取出归还的消耗还低。不过这是一个很主观的标准，在 android 这种移动系统中，每一次创建对象都要在堆上进行分配，每一次销毁都要等待垃圾回收处理，就算单次创建的消耗低，次数多了一样会拖累系统。
2. 对象创建之后，每次使用都会持有较长时间，此时相比“对象的使用”的时间来说，“对象的创建”和“对象的销毁”的开销基本可以忽略了，创建一次对象也算是物超所值了。同时，长时间的持有对象能造成两种结果：1. 对象池越来越大 2. 客户无法从对象池获取到对象了，因为都在使用中。不过这同样也是一个很主观的标准，比如，线程池就是一个很好的例子。你可以对每一个用户请求都新开一个线程来处理，但是当负载峰值时，根本就不可能为每一个用户请求创建一个线程，因为，用户请求只能排队等候了。
3. 对象的状态难以重置，不然下一次使用的时候会引入上次使用的干扰。

## 池化需要注意的问题
1. 对象池也是一种缓存，缓存不宜过大，需要根据具体的情况来设定合适的池大小。
2. 对象池为空的时候要有适当的处理，此时可以新建一个对象返回给客户，不能让客户无限等待。
3. 多线程控制，这个时候可以选择线程同步，不过更适合的是 ThreadLocal，直接规避多线程问题。
