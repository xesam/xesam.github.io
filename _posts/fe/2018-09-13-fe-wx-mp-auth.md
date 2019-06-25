---
layout: post
title: "微信小程序授权"
date: 2018-09-13 08:00:00 +0800
categories: fe
tag: [fe]
---



微信小程序与授权相关的方法有以下几个：

1. wx.getSetting
2. wx.openSetting
3. wx.authorize

wx.getSetting 与 wx.openSetting 比较好理解，wx.getSetting 就是用来检查用户当前的授权状态，wx.openSetting 用来打开授权设置页面。


微信小程序的权限控制趋向于严格，很多授权操作都改为用户手动触发，不能像以前一样，直接从代码层面发起交互。

拿 wx.openSetting() 来说，以前可以直接在生命周期函数中直接调用，从而进入设置页面，调整之后，只能通过。


### 如何一次发起多个权限授权？

暂未发现微信有开放这样的接口。
