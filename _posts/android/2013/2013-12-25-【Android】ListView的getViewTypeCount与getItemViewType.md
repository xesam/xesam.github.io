---
layout: post
title:  "【Android】ListView的getViewTypeCount与getItemViewType"
date:   2013-12-25 12:46:04 +0800
categories: android
tag: [android]
---
# 【Android】ListView的getViewTypeCount与getItemViewType

对于Listiew来说，getViewTypeCount 和getItemViewType主要用于为不同的列表项目提供不同的视图view，
主要用法在有人已经在[《ListView 和 Adapter 的基础》](http://www.cnblogs.com/xiaowenji/archive/2010/12/08/1900579.html)中描述得比较清楚了，
但是文章有一点没说，就是下面这三行：

```java
private static final int TYPE_ITEM = 0;
private static final int TYPE_SEPARATOR = 1;
private static final int TYPE_MAX_COUNT = TYPE_SEPARATOR + 1;
```

这三行是非常重要的，因为TYPE_ITEM和TYPE_SEPARATOR的值最后是被当作一个数组的索引来使用的。

我们已经知道ListView的隐藏列表行开始被显示的时候，行View是被缓存在RecycleBin中的，那么RecycleBin缓存的顺序是什么样的呢？以上面的代码为例，大致过程如下（简化过程，并不代表实际有这些类）：

```java
mRecycler[RecycleBin]
1.mRecycler.setViewTypeCount(mAdapter.getViewTypeCount()); 
    --> int[] mRecycler.viewCache = new View[TYPE_MAX_COUNT] 
        --> int[] mRecycler.viewCache = new View[2];
2.mRecycler.addScrapView(child1); 
    --> mRecycler.viewCache[child.viewType] = child1.view 
        --> mRecycler.viewCache[TYPE_ITEM] = child1.view 
            --> mRecycler.viewCache[0] = child1.view
3.mRecycler.addScrapView(child2); 
    --> mRecycler.viewCache[child.viewType] = child2.view 
        --> mRecycler.viewCache[TYPE_SEPARATOR] = child2.view 
            --> mRecycler.viewCache[1] = child2.view
```

可以发现，一旦ITEM_N的定义不符合数组的规范，那么溢出是非常常见的。我一开始犯的错误就是TYPE_1和TYPE_2...TYPE_N都是随意定义的，
结果报的错误居然是数组溢出，查看了ListView源码之后才发现原来具体的执行过程，以前实在是忽略了。。。。

所以综合看来，google这么做实在是有些不好理解，为什么不直接使用map来存储呢？那样就容易理解得多。


