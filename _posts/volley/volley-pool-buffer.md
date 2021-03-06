---
layout: post
title:  "Volley Pool"
date:   2017-03-20 13:46:04 +0800
categories: volley
tag: [volley]
---

就像 Volley 的口号一样：“a burst or emission of many things or a large amount at once”，Volley 只适合“数据量小，并发量大”的请求场景。造成这种原因的包含了很多原因，其中就有 Pool 的因素。

Volley 中使用到 Pool 的是 ByteArrayPool，并且每个请求队列（RequestQueue）的所有 Request 都共用一个 ByteArrayPool。而是使用了一个包装类 PoolingByteArrayOutputStream，在 BasicNetwork#entityToBytes(HttpEntity) 中使用 PoolingByteArrayOutputStream 来将网络响应的内容转换为 byte 数组，
PoolingByteArrayOutputStream 内部就是使用 ByteArrayPool 作为字节缓存池。至于 ByteArrayPool 的设计意图，在文档中已经说明了：

  ByteArrayPool is a source and repository of <code>byte[]</code> objects. Its purpose is to
  supply those buffers to consumers who need to use them for a short period of time and then
  dispose of them. Simply creating and disposing such buffers in the conventional manner can
  considerable heap churn and garbage collection delays on Android, which lacks good management of
  short-lived heap objects. It may be advantageous to trade off some memory in the form of a
  permanently allocated pool of buffers in order to gain heap performance improvements; that is
  what this class does.

核心意思就是说，为了减少在堆上反复分配和回收内存会造成垃圾回收延迟，导致内存开销上涨。所以开辟一小部分内存空间作为永久缓存池对于性能提升是利大于弊的。

整个流程如下：当网络请求得到返回数据以后，首先在内存开辟出一块区域来存放我们得到的网络数据，不论是 json 还是图片，都会存在于内存的某一块区域，然后拿到UI显示，然而客户端请求是相当频繁的操作，想一下我们平时使用知乎等一些客户端，几乎每一个操作都要进行网络请求（虽然知乎大部分是WebView）。那么问题来了：这么频繁的数据请求，获得数据以后我们先要在堆内存开辟存储空间，然后显示，等到时机成熟，GC回收这块区域，如此往复，那么GC的负担就相当的重，然而Android客户端处理能力有限，频繁GC对客户端的性能有直接影响。我们能不能减少GC和内存的分配呢？我想这个问题就是这个类的产生背景

原始代码简化：

初始化：

```java
    //Volley.java
    public class Volley {
        public static RequestQueue newRequestQueue(Context context, HttpStack stack) {
            Network network = new BasicNetwork(stack);
            RequestQueue queue = new RequestQueue(new DiskBasedCache(cacheDir), network);
            queue.start();
            return queue;
        }
    }

    //BasicNetwork.java
    public class BasicNetwork implements Network {
        private static int DEFAULT_POOL_SIZE = 4096;
        protected final ByteArrayPool mPool;

        public BasicNetwork(HttpStack httpStack) {
            this(httpStack, new ByteArrayPool(DEFAULT_POOL_SIZE));
        }
    }

```

可以看出，同一个请求队列里面的所有请求都会共用一个 ByteArrayPool，并且，如果不进行任何配置，ByteArrayPool 的默认总内存容量是 4096（4K）。

```java
    //BasicNetwork.java
    public NetworkResponse performRequest(Request<?> request) {
        HttpResponse httpResponse = mHttpStack.performRequest(request, headers);
        byte[] responseContents = entityToBytes(httpResponse.getEntity());
        return new NetworkResponse(..., responseContents, ...);
    }

    private byte[] entityToBytes(HttpEntity entity) throws IOException, ServerError {
        PoolingByteArrayOutputStream bytes = new PoolingByteArrayOutputStream(mPool, (int) entity.getContentLength());
        byte[] buffer = null;
        try {
            InputStream in = entity.getContent();
            buffer = mPool.getBuf(1024);
            int count;
            while ((count = in.read(buffer)) != -1) {
                bytes.write(buffer, 0, count);
            }
            return bytes.toByteArray();
        } finally {
            mPool.returnBuf(buffer);
            bytes.close();
        }
    }
```

```java
//PoolingByteArrayOutputStream.java
public class PoolingByteArrayOutputStream extends ByteArrayOutputStream {
    private static final int DEFAULT_SIZE = 256;
    public PoolingByteArrayOutputStream(ByteArrayPool pool) {
        this(pool, DEFAULT_SIZE);
    }

    private void expand(int i) {
        /* Can the buffer handle @i more bytes, if not expand it */
        if (count + i <= buf.length) {
            return;
        }
        byte[] newbuf = mPool.getBuf((count + i) * 2);
        System.arraycopy(buf, 0, newbuf, 0, count);
        mPool.returnBuf(buf);
        buf = newbuf;
    }
}
```
上面我们已经说明过，ByteArrayPool 的默认总内存容量是 4096（4K），而且 Volley 的工具方法中并没有提供完全的定制方法，需要自己手动扩展。那么默认的 4096 会不会造成问题呢？

注意，在 entityToBytes() 的时候，会使用到两个 buffer，一个是

```java
    buffer = mPool.getBuf(1024);
```

另一个是在 PoolingByteArrayOutputStream 实例化的时候隐式创建的：

```java
    PoolingByteArrayOutputStream bytes = new PoolingByteArrayOutputStream(mPool, (int) entity.getContentLength());
```
对应 buffer 的长度是响应 entity 的内容长度。如果我们的单个请求响应结果长度大于 4096，那么 ByteArrayPool#getBuf(int len) 返回的 buffer 其实是一个新的 byte[]，由于大小超出容量，在这个 byte[] 使用完成之后，是无法被重用的，只能等待系统垃圾回收。所以，对于响应比较大的请求，这存在一个权衡问题，如果我们提升缓存池的容量，可能存在一个浪费，如果我们不提升容量，又经常会在堆上分配/销毁，丢失了缓存池的优势。所以，我个人觉得开发者应该根据项目本身的接口情况来评估一下每个响应的平均长度来选取合适的缓存池容量。

现在假设响应长度都在容量范围之内，我们换一种写法来实例化 PoolingByteArrayOutputStream：

```java
    PoolingByteArrayOutputStream bytes = new PoolingByteArrayOutputStream(mPool);
```
也就是使用默认的 256 缓存尺寸，这个时候不会产生错误，但是会产生严重影响。因为一旦我们的请求响应结果长度大于 256（小于容量），就意味着 PoolingByteArrayOutputStream 肯定会调用 PoolingByteArrayOutputStream#expand(len) 来重新调整内部 buffer 的大小，同时还得将已经读取的数据复制一遍到新 buffer 里面。不仅仅是响应结果长度大于 256 的时候有问题，就算是长度小于 256 的情况，也意味着一开始分配的 1024 大小的 buffer 存在浪费。所以，代码作者的选择是最优选择了。

再看一下 PoolingByteArrayOutputStream#expand(len) 的实现：

```java
    // PoolingByteArrayOutputStream.java
    private void expand(int i) {
        if (count + i <= buf.length) {
            return;
        }
        byte[] newbuf = mPool.getBuf((count + i) * 2);
        System.arraycopy(buf, 0, newbuf, 0, count);
        mPool.returnBuf(buf);
        buf = newbuf;
    }
```
每次往 PoolingByteArrayOutputStream 里面写数据的时候，都会检查一遍 buffer 的长度是否足够，不够的话就重新再分配一个。策略就是常见的”当前所需长度 * 2“，这种分配在实际的 Volley 中其实没有用到，因为默认分配的 buffer 是足够的。不过作为一个更通用的设计，这种分配策略其实还有点问题的，因为并不能保证”当前所需长度 * 2“不超过最大容量，相当于又绕过了缓存池。所以其实可以先检查一下缓存池中的最大 buffer 能不能满足需求，不能的话再来新建并分配。

我们主要关注 ByteArrayPool 的几个点：

1. ByteArrayPool 同时使用了两个列表来记录池化对象的使用情况：

```java
    //用来实际保存可复用的缓存数组，
    private List<byte[]> mBuffersBySize = new ArrayList<byte[]>(64);
    //充当时间线的角色，用来实现 Least Recently Used 策略。即在需要缩减池对象的时候，优先移除最久未使用的 byte[] 对象。
    private List<byte[]> mBuffersByLastUse = new LinkedList<byte[]>();
```

所以在说到一个问题的时候，总会涉及到更多的背景知识。

2. 查找目标的时候用了遍历和 binarySearch 两种实现

```java
public synchronized byte[] getBuf(final int len) {
    int pos = Collections.binarySearch(mBuffersBySize, null, new Comparator<byte[]>() {
        @Override
        public int compare(byte[] o1, byte[] o2) {
            return o1.length - len;
        }
    });
    if (pos < 0) {
        pos = -pos - 1;
    }
    if (pos >= mBuffersBySize.size()) {
        return new byte[len];
    } else {
        byte[] buf = mBuffersBySize.get(pos);
        mCurrentSize -= buf.length;
        mBuffersBySize.remove(buf);
        mBuffersByLastUse.remove(buf);
        return buf;
    }
}
```

http://www.voidcn.com/blog/yuan514168845/article/p-4950324.html
