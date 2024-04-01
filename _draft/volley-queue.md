---
layout: post
title:  "Volley 容器说明"
date:   2017-03-21 13:46:04 +0800
categories: volley
tag: [volley]
---
当我们发起一个请求时，就是向 RequestQueue 中添加一个 Request：

```java
    //RequestQueue.java
    public <T> Request<T> add(Request<T> request) {
        
    }
```
在 RequestQueue 内部，使用多个容器来管理和调度 Request 的流向。就是下列：

```java 
    //RequestQueue.java

    //mCurrentRequests 持有所有已经添加（add）但是没有完成（finish）的请求。
    Set<Request<?>> mCurrentRequests = new HashSet<Request<?>>();

    //mCacheQueue 持有所有需要先检查缓存是否命中的请求。缓存调度器（CacheDispatcher）不断从 mCacheQueue 中取出 Request 来处理。 
    PriorityBlockingQueue<Request<?>> mCacheQueue = new PriorityBlockingQueue<Request<?>>();

    //mNetworkQueue 持有所有需要发起网络访问的请求。网络调度器（NetworkDispatcher）不断从 mNetworkQueue 中取出 Request 来处理。 
    PriorityBlockingQueue<Request<?>> mNetworkQueue = new PriorityBlockingQueue<Request<?>>();

    //相同 cache key 的临时等待区
    Map<String, Queue<Request<?>>> mWaitingRequests = new HashMap<String, Queue<Request<?>>>();
```

前三个比较好理解，大致逻辑就是：

```java
    //RequestQueue.java
    public <T> Request<T> add(Request<T> request) {
        //mCurrentRequests 是纯粹的记录和管理容器，只在最后清理 Requ 的时候有用
        synchronized (mCurrentRequests) {
            mCurrentRequests.add(request);
        }

        if (!request.shouldCache()) {//如果 Request 禁止缓存，就直接走网络调度
            mNetworkQueue.add(request);
            return request;
        }else{//如果 Request 允许缓存，就先走缓存调度进行缓存检查
            mCacheQueue.add(request);
            return request;
        }
    }

```

最后一个 mWaitingRequests 需要说明下：

    某些时候，我们会重复或者定时发送相同的请求，并且这些请求的响应都是允许缓存的，那么其实并没有必要完完全全按照调用的次数去发起网络调用，我们只需要从这些相同的请求中选取其中一个（这里选取第一个）去进行真实的网络请求，等这个被选中的 Request 执行完毕，刷新本地缓存之后，然后剩下其他的请求可以直接从缓存中去获取响应即可，这样就省下了多余的网络请求。

所以这里对缓存情况进行了一定的优化扩充，对应 mWaitingRequests 的简化逻辑就应该是：

```java
    //RequestQueue.java
    public <T> Request<T> add(Request<T> request) {
        if (!request.shouldCache()) {
            //other codeRequest
        }else{
            String cacheKey = request.getCacheKey();
            if (mWaitingRequests.containRequestsKey(cacheKey)) {
                // 检查是否已经存在对应的临时等待区，如果存在，说明已经有一个相同的请求在处理中
                Queue<Request<?>> stagedRequests = mWaitingRequests.get(cacheKey);
                if (stagedRequests == null) {
                    stagedRequests = new LinkedList<Request<?>>();
                }
                stagedQueueRequests.add(request);
                mWaitingRequests.put(cacheKey, stagedRequests);
            } else {
                // 这里增加一个 key，表明这个 key 已经有一个请求在处理中。主要是为了 mWaitingRequests.containsKey(cacheKey) 判断，至于初始 value 并不重要，null 即可。
                mWaitingRequests.put(cacheKey, null);
                mCacheQueue.add(request);
            }
            return request;
        }
    }
```

那么 mWaitingRequests 中临时等待的请求何时得到执行呢？就像刚才说的一样，在被选中的 Request “执行完毕，刷新本地缓存之后”。Request 执行完毕之后会触发 finish():

```java
    //Request.java
    void finish(final String tag) {
        if (mRequestQueue != null) {
            mRequestQueue.finish(this);mNetworkQueue
        }
    }

    //RequestQueue.java
    <T> void finish(Request<T> request) {
        if (request.shouldCache()) {
            String cacheKey = request.getCacheKey();
            Queue<Request<?>> waitingRequests = mWaitingRequests.remove(cacheKey);
            if (waitingRequests != null) {
                // 等待的请求直接交由缓存调度器（CacheDispatcher）处理
                mCacheQueue.addAll(waitingRequests);
            }
        }
    }
```

可以看到，Volley 对 Request 的调度，都是直接将某个 Request 添加或者转移到不同的 Queue 中实现的。如果要将某个 Request 加入缓存调度，将其加入 mCacheQueue 即可，如果想将某个 Request 加入网络调度，将其加入 mNetworkQueue 即可。

mCacheQueue 与 mNetworkQueue 都是优先级阻塞队列（PriorityBlockingQueue），所以这两个队列都是线程安全并且支持优先级排序的，那么 Request 的优先级是什么呢？

```java
    //Request.java
    @Override
    public int compareTo(Request<T> other) {
        Priority left = this.getPriority();
        Priority right = other.getPriority();

        return left == right ?
                this.mSequence - other.mSequence :
                right.ordinal() - left.ordinal();
    }
```

每个 Request 都有一个优先级和一个序列号：

```java
    //Request.java
    public enum Priority {
        LOW,
        NORMAL,
        HIGH,
        IMMEDIATE
    }

    //RequestQueue.java
    public <T> Request<T> add(Request<T> request) {
        //这里给 Request 设置一个序列号，默认的序列号是自增整数。
        request.setSequence(getSequenceNumber());
    }
```

所以在调度器处理 Request 的时候， Request 优先级的权重更高，随后才按照序列号来排列。

