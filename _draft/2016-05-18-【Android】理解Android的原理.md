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

Android’s background priority is actually pretty interesting. 
It uses a Linux facility called cgroups to put all background threads into a special scheduling group which, all together, 
can’t use more than 10% of the CPU. 
That is, if you have 10 processes in the background all trying to run at the same time, 
when combined they can't take away more than 10% of the time needed by foreground threads. 

This is enough to allow background threads to make some forward progress, 
without having enough of an impact on the foreground threads to be generally visible to the user.

Android 的后台优先级实际上相当有趣，它使用了 Linux 上的 cgroup 机制，将所有的后台线程都集中到一个特定的后台调度组中，
这个调度组里面的所有线程加在一起都不会超过 CPU 资源的 10% 。也就是说，如果你有 10 个后台进程同时在运行，他们加在一起的运行时间都不会超过前台线程的 10% 。
这种实现既可以让后台任务得到执行，有可以保证不对前台线程造成太大的干扰。


（你会发现有一个 foreground 的优先级定义，这个定义现在已经没有用了，
只在最初的版本得到实现。后来我们发现 Linux 调度器，
因此，我们在 Android 1.6 切换为 cgroup 机制。）

我也听到过许多抱怨认为 Android 的基础架构设计过时而且有缺陷，
因为 Android 没有像 iOS 一样的渲染线程。
iOS 的这种工作方式当然有一定的好处，但是这种观点台关注于某些特定的细节，
容易一叶障目不见泰山。

Android 与 iOS 的设计目标有非常大的不同。Android 的一个关键目标是提供一个开放应用平台，
让应用运行在各自的应用沙盒里面，不需要某个机构去认证应用的行为是否合乎应用自身的行为准则，
从而实现一个去中心化的运行平台。
为了实现这个目标，Android 使用了 Linux 的进程隔离以及用户 ID 来限制应用对系统或者
其他应用的不受控或者有风险的操作。

这与 iOS 的最初设计完全不同，因为你知道，iOS 刚出来的时候，是不允许安装任何第三方应用的 。

实现这个目标的一个重要方面是通过一种安全的方式将屏幕元素进行分离。
































