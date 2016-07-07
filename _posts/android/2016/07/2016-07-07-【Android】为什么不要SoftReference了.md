---
layout: post
title:  "【Android】为什么不要SoftReference了"
date:   2016-07-07 18:20:04 +0800
categories: android
tag: [android]
---

Android 的官方关于 [SoftReference](https://developer.android.com/reference/java/lang/ref/SoftReference.html) 的文档中，明确指出 

    Avoid Soft References for Caching
    
而给出的原因是：

    The runtime doesn't have enough information on which references to clear and which to keep. 
    Most fatally, it doesn't know what to do when given the choice between clearing a soft reference and growing the heap.
    
即：
    
    Runtime 没有足够的信息来判别应该清除哪个 SoftReference(持有的对象)，
    更无法判定当 App 要求更多内存的时候，是应该清除 SoftReference，还是增大 App 的Heap。
     
听着是不是很合理，但是这个根本说不过去啊。

因为在正常的 JVM 中，只要不会触发 OOM（达到系统内存上限或者到达 JVM 设定的内存上限），JVM 就应该毫不留情的增大 Heap 来维持应用的正常运行。
而没有必要考虑是先清理 SoftReference，还是增大 Heap 这种无聊的问题。

唯一与 JVM 不一样的是：用户 App 通常没有权限来设定自己的最大可用内存，这个是由系统全权把握， 单个 App 使用的最大内存容量是固定的：

```java
    Runtime.getRuntime().maxMemory()
```

其他就是跟 JVM 差不多了，Android 在启动每一个 App 的时候，也并不是一开始就给每个 App 分配固定的上限内存，也是按需动态分配，所以，这应该不是技术问题。

所以，我个人觉得，这只是用户体验上的取舍问题，Android 与 PC 系统最大的区别就是：
通常情况下，PC 系统不会杀死任何一个用户应用来运行另一个应用，而 Android 会在任意时刻杀掉哪些优先级比较低的 App 来释放内存，从而给优先级高的 App 提供资源。

在 Android 上面，App 的优先级通常是用户的交互行为赋予的。
当一个 App 被用户调到前台，Android 会尽量满足这个 App 的一切非特权要求，如果此 App 占用的内存比较大，
那么，会挤压其他后台运行 App 的生存空间，使得 Android 能够缓存的应用数目减少，同时减缓应用被再次调起的速度；
另一方面，如果后台 App 占用的内存比较大，那么自身被杀死的几率也会相应增大。
考虑到这些情况，假如在有内存需求的情况下，Android Runtime 总是一味增大对应 App 的 Heap，那么，最终损害的只是用户的整体体验，这他妈就很尴尬了。

因此，Android 对 SoftReference 这个“墙头草”采取了比较激进的措施，即尽可能的多的找机会来清除它们，结果还不如使用 WeakReference，起码效果和语义都是可预期的。
同时，Android Runtime 也将内存控制的一部分内容让渡给开发者，这里面就包括 SoftReference。
开发者可以采取各自的策略来处理类似的内存问题，换句话说，就是用“开发者智能”替换“运行时策略”。如果开发者置之不理，那么结果就是要么是没有缓存，要么是内存暴涨。
Android 官方推荐的是 [LruCache](https://developer.android.com/reference/android/util/LruCache.html)来进行缓存，LruCache 的

# SoftReference 与 LruCache

LruCache 虽然挺有用，但是有些问题还是需要了解的。

1. LruCache 需要设置容量大小，不同的机型可用内存不一样，因此，不同手机上这个大小使应该动态调整的，自古“一刀切”都是没有好结果的。
2. LruCache 是面向开发者的，也就是只有明确使用 LruCache，缓存策略才有效。如果在 LruCache 之外想缓存或者分配大对象，没有办法自动来释放 LruCache 的空间以容纳新的对象。
在这一点上，SoftReference 是符合预期的，因为 SoftReference 是被 Runtime 控制的，可以在全局进程来动态调整回收。

