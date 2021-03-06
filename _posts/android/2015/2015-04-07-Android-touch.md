---
layout: post
title:  "Android 触屏事件传递简述"
date:   2015-04-07 12:46:04 +0800
categories: android
tag: [android]
---
ActivityA包含ViewGroupB，ViewGroupB包含ViewC，这里选取ViewGroupB（中间节点）作为当前节点视角

![在此输入图片描述][1]

## 过程一：当前节点与父节点的事件关系

ActivityA只关心ViewGroupB.onDispatchTouchEvent返回值，只要在ACTION_DOWN分发过程中B.onDispatchTouchEvent()返回为true，那么后续的事件都会向B分发。至于ViewGroupB在onDispatchTouchEvent方法中是怎么处理的，父节点ActivityA并不会过问。

换句话说，父节点向***直接子节点ViewGroupB***兜售ACTION_DOWN事件，子节点使用onDispatchTouchEvent方法的返回值进行应答，只要子节点表示能够处理ACTION_DOWN，那么父节点就会将后续事件持续交给子节点。

## 过程二：当前节点与子节点的事件关系

ViewGroupB从上一级收到ACTION_DOWN事件之后，会调用onInterceptTouchEvent判断是否进行拦截。如果不拦截，那么流程与上面的“过程一”一致，如果拦截，那么ViewGroupB就吃掉事件，直接忽略ViewC。

不过onInterceptTouchEvent属于内部方法，这个方法本身并不会影响当前节点的onDispatchTouchEvent返回值。

## onDispatchTouchEvent返回值的判断

通常情况下，一个节点的onDispatchTouchEvent返回值只与当前节点的onTouchEvent返回值和子节点的onDispatchTouchEvent返回值有关：

```java
    this.onDispatchTouchEventValue = child.onDispatchTouchEventValue || this.onTouchEvent
```

当然，也可以强制给onDispatchTouchEvent赋一个返回值，尽管如此，也不应该强制抛弃原有的事件机制，因为原有的事件机制会进行一些状态清理等操作。

ACTION_DOWN示例图：
![在此输入图片描述][2]

  [1]: http://static.oschina.net/uploads/space/2015/0407/015042_pxbX_93688.png
  [2]: http://static.oschina.net/uploads/space/2015/0411/120049_AoiN_93688.png
