---
layout: post
title: "小程序生命周期"
date: 2020-09-12 08:00:00 +0800
categories: fe
tag: [fe]
---

微信小程序大致可以认为是“微信 - App - Page”这样的三层结构，微信是 App 的宿主，App 是 Page 的宿主，宿主的状态会影响旗下子元素不同生命周期方法的调用。微信自身维护 Android、iOS等操作系统要求的生命周期方法，至于微信怎么定义小程序的生命周期，那全都是微信说了算。

<!-- more -->
#### 小程序 Page 间的跳转
Page 间的跳转，是先 unLoad 了旧的 Page，再创建新的Page，这样有个问题就是，旧的 Page 没有了，新的 Page 还没创建，Page 与 Page 间就会有一段时间的空白。Page 生命周期方法挺少的，应该也是微信团队综合考虑之后的精简方案，毕竟简单稳定：

![1]({{ site.baseurl }}/assets/product/miniapp/lifecycle-page-navigate.svg)

#### 小程序的启动与 reLaunch 方法
个人觉得这个 reLaunch 方法名字取得不是很贴切，因为 onLaunch 是 App 的一个生命周期方法，但是 reLaunch 却与 App 毫无关系。单纯从名字看，难道不应该是先销毁 App，然后重建 App，再打开指定 Page 吗？当然，实际并不是这样的：

![2]({{ site.baseurl }}/assets/product/miniapp/lifecycle-launch-relaunch.svg)

#### 小程序退到后台与恢复
在微信里面，小程序退到后台的途径比较少：

1. 关闭小程序。
2. 操作系统的“返回Home”或者 “切换应用程序” 操作。

在这些情况下，并不会触发 Page 的 onUnload 生命周期方法，如果一直留在后台，那么“是否会触发 onUnload？”以及“何时触发 onUnload？”都是不确定的。

至于恢复小程序的方式，就非常多了，看看小程序开发文档里面的场景值就知道了。不过大致可以分为两类：

1. 直接把小程序调回到前台。
2. 先把小程序调回到前台，然后打开指定页面。

第一种方式遵循文档的描述，就是普通的 hide / show。但是第二种的具体机制没有文档阐述，不过初步看可以认为行为与 reLaunch 类似，同时，并不管新打开的指定页面是不是与原本的页面相同：

![3]({{ site.baseurl }}/assets/product/miniapp/lifecycle-back-frant.svg)