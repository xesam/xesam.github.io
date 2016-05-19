---
layout: post
title:  "【Android】理解Android的原理"
date:   2016-05-18 08:00:00 +0800
categories: Android
---


## 译者注

这是一篇 2011 年底的文章，最初发表在 [google+](https://plus.google.com/u/0/105051985738280261832/posts/XAZ4CeVP6DC)，
作者是 Google 的 Android Framework 开发工程师，她讲述了 Android 的部分设计渊源。
虽然过去了好些年，Android 也发生了翻天覆地的变化，但是这些理念依旧沿用了下来，依旧值得我们一览以窥 Android 之道。

## 正文

A few days ago I wrote a post trying to correct a lot of the inaccurate statements I have seen repeatedly mentioned about how graphics on Android works. 
This resulted in a lot of nice discussion, 
but unfortunately has also lead some people to come up with new, novel, and often technically inaccurate complaints about how Android works.

几天前，我写了一篇文章用来纠正许多有关 Android 图形工作机制的错误言论，并引发了许多积极的讨论。
但不幸的是，同时也导致了部分人产生一些新鲜奇怪但是往往不准确的抱怨，有关 Android 的工作机制。


These new topics have been more about some fundamental design decisions in Android, and why they are wrong. 
I’d like to help people better understand (and judge) these discussions by giving some real background on why Android’s UI was designed the way it is and how it actually works.

这些新的点更多的集中在 Android 的基础核心设计，我会告诉他们，为什么他们错了。
我希望通过介绍 Android UI 的设计意图和工作机制的背景故事， 来帮助人们更好的理解（或者聘雇）这些核心设计决策。

One issue that has been raised is that Android doesn’t use thread priorities to reduce how much background work interrupts the user interface. 

This is outright wrong. It actually uses a number of priorities, 
which you can even find defined right here http://developer.android.com/reference/android/os/Process.html#THREAD_PRIORITY_AUDIO in the SDK.

一个观点认为，Android 并没有使用线程优先级控制来确保后台任务不会影响到用户交互。
这个观点大错特错，Android 使用了一系列的优先级策略，可以在这里发现更多：[http://developer.android.com/reference/android/os/Process.html#THREAD_PRIORITY_AUDIO](http://developer.android.com/reference/android/os/Process.html#THREAD_PRIORITY_AUDIO)

The most important of these are the background and default priorities.
User interface threads normally run at the default priority; background threads run in the background priority. 
Application processes that are in the background have all of their threads forced to the background priority.

这里面最重要的就是 background 优先级 与 默认优先级。
用户界面线程通常以默认优先级运行，后台线程以后台优先级运行。应用将在后台运行的线程都置为 background 优先级。



































