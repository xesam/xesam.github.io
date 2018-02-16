---
layout: post
title:  "Android Service生命周期回顾"
date:   2016-03-20 13:46:04 +0800
categories: android
tag: [android]
---

Service 经历的生命周期较少，可以分三种情况记录。

## 第一种，startService / stopService

![1]({{ site.baseurl }}/image/service_lifecycle_1_and_2.png)

注意点：

1. 第一次 startService 会触发 onCreate 和 onStartCommand，以后在服务运行过程中，每次 startService 都只会触发 onStartCommand
2. 不论 startService 多少次，stopService 一次就会停止服务

## 第二种，bindService / unbindService

图示同上。

注意点：

1. 第一次 bindService 会触发 onCreate 和 onBind，以后在服务运行过程中，每次 bindService 都不会触发任何回调
2. bindService 多少次，就对应多少次的 unbindService， bindService / unbindService 操作顺序以及次数对应的话， 就会停止当前服务

## 第三种，前面两种交错

![1]({{ site.baseurl }}/image/service_lifecycle_3.png)

注意点：

1. 只有当 startService / stopService 与 bindService / unbindService 都满足条件时，才会停止服务

### onBind 的作用

如果我们将 “开始有 client 发起 bindService”到“所有 client 都调用 unbindService”中间的过程视为一个“轮回”，
那么同一个服务的同一个运行生命周期（从 onCrete 到 onDestroy 之间）内，就有可能发生多次“轮回”。

onBind 主要用来产生一个 Binder，只需要知道同一个服务的 Binder 只会有一个，onBind 只会在第一个“轮回”调用一次，主要负责则 “Create Binder”。

### onRebind

onBind 与 onRebind 不会在一个“轮回”中同时被调用。

如果 bindService 操作触发了 onCreate 回调，那么，同时也会触发 onBind。

### onUnbind 的返回值

onUnbind 的返回值只会在服务运行期间从第二个“轮回”开始发生作用。
那如何才能出现第二个“轮回”？肯定只有在调用了 startService 的情况下，服务保持运行期间，才会有第二，第三个“轮回”。
否则，每一个“轮回”就都是第二种情况了。举个例子说明下：

第一个例子，onUnbind 返回 false

1. 调用 startService。触发 onCreate 与 onStartCommand
2. 调用 bindService。触发 onBind
3. 调用 unbindService 触发 unbindService
4. 调用 bindService。无回调
5. 调用 unbindService 无回调
6. 调用 stopService。触发 onDestroy 

第二种例子，onUnbind 返回 true

1. 调用 startService。触发 onCreate 与 onStartCommand
2. 调用 bindService。触发 onBind
3. 调用 unbindService 触发 unbindService
4. 调用 bindService。触发 onRebind
5. 调用 unbindService 触发 onUnbind
6. 调用 stopService。触发 onDestroy 


## 几个问题

### bindService 与什么有关？
ServiceConnection 对象是 bind 操作的标识符。

bindService / unbindService 都需要与同一个 ServiceConnection 对象配对。
同一个 ServiceConnection 对象只会触发一次绑定。只有在 unbindService 后才能重新绑定。

### 如何知道绑定了多少个 client

Service 本身不能知道有多少个 client，可以在每次触发 ServiceConnection 的时候增加一次静态计数。

### Service 如何指导是否有新的 client 绑定？

如果不是在“轮回”的开始，Service 无法知道有新的 client 绑定，只能 client 主动通知给 Service。

