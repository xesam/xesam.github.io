---
layout: post
title:  "【Android】理解Android的原理"
date:   2016-05-18 08:00:00 +0800
categories: Android
---

http://tieba.baidu.com/p/2035027162?see_lz=1

## 译者注

这是一篇 2011 年底的文章，最初发表在 [google+](https://plus.google.com/u/0/105051985738280261832/posts/XAZ4CeVP6DC)，
作者是 Google 的 Android Framework 开发工程师，她讲述了 Android 的部分设计渊源。
虽然过去了好些年，Android 也发生了翻天覆地的变化，但是这些理念依旧沿用了下来，依旧值得我们一览以窥 Android 之道。

## 原文正文翻译

A few days ago I wrote a post trying to correct a lot of the inaccurate statements I have seen repeatedly mentioned about how graphics on Android works.
This resulted in a lot of nice discussion,
but unfortunately has also lead some people to come up with new, novel, and often technically inaccurate complaints about how Android works.

几天前，我写了一篇文章试图纠正一些有关 Android 图形工作机制的错误观点，并引发了许多积极的讨论。
但不幸的是，这同样导致了一些人列举出新的奇异观点来错误的从技术上解释 Android 的运行机制。

These new topics have been more about some fundamental design decisions in Android, and why they are wrong.
I’d like to help people better understand (and judge) these discussions by giving some real background on why Android’s UI was designed the way it is and how it actually works.

这些新的观点更多的集中在 Android 的基础核心设计上，下面，我会告诉他们，为什么他们错了。
我希望通过阐述 Android UI 的设计意图以及工作机制的背景设计，来帮助人们更好的理解（或者判断）这些核心设计决策。

One issue that has been raised is that Android doesn’t use thread priorities to reduce how much background work interrupts the user interface.This is outright wrong. It actually uses a number of priorities,
which you can even find defined right here http://developer.android.com/reference/android/os/Process.html#THREAD_PRIORITY_AUDIO in the SDK.

有种观点认为，Android 没有使用线程优先级调度来降低后台任务对用户交互的影响。这个观点大错特错，实际上，Android 使用了一系列的优先级策略，官方文档有许多优先级描述：[http://developer.android.com/reference/android/os/Process.html#THREAD_PRIORITY_AUDIO](http://developer.android.com/reference/android/os/Process.html#THREAD_PRIORITY_AUDIO)

The most important of these are the background and default priorities.
User interface threads normally run at the default priority; background threads run in the background priority.
Application processes that are in the background have all of their threads forced to the background priority.

这里面最重要的就是后台（background）优先级与默认（default）优先级。用户界面线程通常以默认优先级运行，后台线程以后台优先级运行。当一个应用运行在后台是，应用内的所有线程都被强制转入后台优先级。

Android’s background priority is actually pretty interesting.
It uses a Linux facility called cgroups to put all background threads into a special scheduling group which, all together,
can’t use more than 10% of the CPU.
That is, if you have 10 processes in the background all trying to run at the same time,
when combined they can't take away more than 10% of the time needed by foreground threads.

This is enough to allow background threads to make some forward progress,
without having enough of an impact on the foreground threads to be generally visible to the user.

Android 的后台优先级实际上相当有趣，它使用了 Linux 上的 cgroup 机制，将所有的后台线程都集中到一个特定的调度组中，
这个调度组里面的所有线程加在一起都不会占用超过 CPU 资源的 10% 。也就是说，就算你有 10 个后台进程同时在运行，它们加在一起的运行时间都不会超过前台线程的 10% 。这种实现已经足够让后台任务得到执行，同时又不会对前台线程造成用户可感知的干扰。

(You may have noticed that a “foreground” priority is also defined. This is not used in current Android; it was in the original implementation, but we found that the Linux scheduler does not give enough preference to threads based on pure priority, so switched to cgroups in Android 1.6.)

（你可能会发现有一个 foreground 的优先级定义，这个定义只在最初的版本得到实现，现在已经没什么作用了。因为在后来的 android 版本中，我们发现 Linux 调度器并不会单纯的因为设置了优先级就对某些线程特别关注，所以，我们在 Android 1.6 切换为 cgroup 机制。）

I have also seen a number of claims that the basic Android design is fundamentally flawed and archaic because it doesn’t use a rendering thread like iOS. There are certainly some advantages to how iOS work, but this view is too focused on one specific detail to be useful, and glosses over actual similarities in how they behave.

我也听到过许多吐槽说 Android 的基础架构设计是过时而且有缺陷的，因为 Android 没有像 iOS 那样的渲染线程。iOS 的这种工作方式固然有它的好处，但是这种观点过度关注于某些特定的细节而忽视了两者之间的相似点。

Android had a number of very different original design goals than iOS did. A key goal of Android was to provide an open application platform, using application sandboxes to create a much more secure environment that doesn’t rely on a central authority to verify that applications do what they claim. To achieve this, it uses Linux process isolation and user IDs to prevent each application from being able to access the system or other application in ways that are not controlled and secure.

Android 与 iOS 的原始设计目标有非常大的不同。Android 的核心目标之一是提供一个开放应用平台，让应用运行在各自的应用沙盒里面，不需要某个特定的机构去认证应用的行为是否合乎应用自身的行为准则。为了实现这个目标，Android 使用了 Linux 的进程隔离以及用户 ID 来限制应用对系统或者其他应用的非受控或者有风险的操作。

This is very different from iOS’s original design constraints, which remember didn’t allow any third party applications at all.

这与 iOS 的最初约束性设计完全不同，因为你知道，iOS 刚出来的时候，是不允许安装任何第三方应用的 。

An important part of achieving this security is having a way for (EDIT: It has been pointed out to me that iOS does in fact use multiple windows and multiple GL contexts.  Lesson to me, just don't talk about anything I haven't directly verified. :)  That still doesn't change things for Android, though, where as I mention later we simply did not have hardware and drivers that could do multiple GL contexts until fairly recently.)
individual UI elements to share the screen in a secure way.

实现这种安全特性的一个重要部分就是使用单独的 UI 元素，然后通过一种安全的方式共享屏幕。(附：有人向我指出 iOS 实际上使用了多窗口和多 GL 上下文。给我的教训就是不要对不熟悉的事物妄加评论。不过这对 Android 没有什么意义，就像我待会儿要提到的一样，直到最近，我们都没有硬件和驱动来支持多 GL 上下文)

This is why there are windows on Android. The status bar and its notification shade are windows owned and drawn by the system. These are separate from the application’s window, so the application can not touch anything about the status bar, such as to scrape the text of SMS messages as they are displayed there. Likewise the soft keyboard is a separate window, owned by a separate application, and it and the application can only interact with each other through a well defined and controlled interface. (This is also why Android can safely support third party input methods.)

这也是为什么 Android 要有 Window 的原因。StatusBar 以及 Notification 面板都属于系统的 Window，由系统负责绘制。因此，应用就无法访问或者修改 StatusBar 的任何内容，比如，无法读取通知栏显示的短信内容。同样，软键盘也是一个单独的 Window，属于另一个独立的应用。当前应用只能通过一种严格定义的受限接口与输入法应用相交互。（这也是为什么 Android 可以安全的支持第三方输入法的原因）

Another objective of Android was to allow close collaboration between applications, so that for example it is easy to implement a share API that launches a part of another application integrated with the original application’s flow. As part of this, Android applications traditionally are split into pieces (called “Activities”) that handle a single specific part of the UI of the application. For example, the contacts lists is one activity, the details of a contact is another, and editing a contact is a third. Moving between those parts of the contacts UI means switching between these activities, and each of these activities is its own separate window.

Android 的另一个目标是支持应用间的无缝协作，比如，可以很方便的实现一个分享 API，在不中断工作流的情况下，从原始的应用平滑的启动另一个应用的相应部分。作为实现的一部分，Android 通常划分为片（也就是 Activity）来分别处理特定的 UI 任务。
比如，联系人列表是一个 Activity，联系人详情是另一个 Activity，联系人编辑页面也是一个 Activity。在这些界面间的移动也就是在这些 Activity 之间的切换，每个 Activity 都就是它们自己的 Window。

Now we can see something interesting: in almost all of the places in the original Android UI where you see animations, you are actually seeing windows animate. Launching Contacts is an animation of the home screen window and the contacts list window. Tapping on a contact to see its details is an animation of the contacts list window and the contacts details window. Displaying the soft keyboard is an animation of the keyboard window. Showing the dialog where you pick an app to share with is an animation of a window displaying that dialog.

现在，你会发现一些有趣的地方，几乎所有你看到的 UI 动画，实际上都是 Window 动画。启动通讯录的时候，看到的是 Home Window 动画以及联系人列表 Window 动画，点击联系人查看详情的时候看到的是联系人列表 Window 动画以及详情页 Window 动画，显示输入法面板的时候，展示的是输入法 Window 动画，显示对话框的时候是对话框的 Window 动画。

When you see a window on screen, what you are seeing is actually something called a “surface”. This is a separate piece of shared memory that the window draws its UI in, and is composited with the other windows to the screen by a separate system service (in a separate thread, running at a higher than normal priority) called the “surface flinger” Does this sound familiar? In fact this is very much like what iOS is doing with its views being composited by a separate thread, just at a less fine-grained but significantly more secure level. (And this window composition has been hardware accelerated in Android from the beginning.)

你在屏幕上看到的一个个 Window，实际都是一个个的 “surface”。这是窗口渲染ui使用的共享内存的一个特殊片段，由一个被称为"surface flinger"的系统服务（一个独立的进程，运行在高于普通的优先级）来混合各个窗口的表层以显示在屏幕上。。（这个系统服务运行在一个单独的线程里面，并拥有一个更高的优先级）
是不是听起来很熟悉，这种机制与 iOS 使用单独的线程来组合View 界面是类似的。并且 window 是从一开始就支持硬件加速。

The other main interesting interaction in the UI is tracking your finger -- scrolling and flinging a list, swiping a gallery, etc. These interactions involve updating the contents inside of a window, so require re-rendering that window for each movement. However, being able to do this rendering off the main thread probably doesn’t gain you much. These are not simple “move this part of the UI from X to Y, and maybe tell me when you are done” animations -- each movement is based on events received about the finger on the screen, which need to be processed by the application on its main thread.

另一个有趣的 UI 交互是手指追踪：滚动或者快速滑动列表，切换 Gallery 等等。这些交互都涉及到窗口内容的更新，所以每一个动作都需要重新渲染窗口。然而，就算关掉主线程来进行这种渲染，可能都达不到你的期望。这些都不是“将 UI 的这一部分从X 移动到 Y，以及可能完成时告诉我一下”的简单动画 - 每一个动作是基于收到有关屏幕上手指，都需要由应用程序的主线程来处理。

That said, being able to avoid redrawing all of the contents of the parts of the UI that are moving can help performance. And this is also a technique that Android has employed since before 1.0; UI elements like a ListView that want to scroll their content can call http://developer.android.com/reference/android/view/View.html#setDrawingCacheEnabled(boolean) to have that content rendered into a cache so that only the bitmap needs to be drawn as it moves.

也就是说，如果我们能够避免重绘正在移动的内容，能够提升系统性能。这也是 Android 在 1.0 版本之前就已经采用的技术;
类似 ListView 的UI元素，在滑动的时候，可以调用[View#setDrawingCacheEnabled(boolean）](http://developer.android.com/reference/android/view/View.html#setDrawingCacheEnabled(boolean）)将内容渲染到缓存中，如此一来就只有 bitmap 需要重绘。

Traditionally on Android, views only have their drawing cache enabled as a transient state, such as while scrolling or tracking a finger. This is because they introduce a fair amount more overhead: extra memory for the bitmap (which can easily total to multiple times larger than the actual frame buffer if there are a number of visual layers), and when the contents inside of a cached view need to be redrawn it is more expensive because there is an additional step required to draw the cached bitmap back to the window.

通常，在Android上的 View 仅启用作为过渡状态的绘图缓存，如在滚动或跟踪手指。这是因为他们引入了相当多的开销：bitmap 带来的额外储器（其可以容易地总多次比实际帧缓冲器较大，如果有许多视觉层），而当一个高速缓存视图需要里面的内容重绘它是较昂贵的，因为有绘制缓存的位图回窗口所需的附加步骤。

So, all those things considered, in Android 1.0 having each view drawn into a texture and those textures composited to the window in another thread is just not that much of a gain, with a lot of cost. The cost is also in engineering time -- our time was better spent working on other things like a layout-based view hierarchy (to provide flexibility in adjusting for different screen sizes) and “remote views” for notifications and widgets, which have significantly benefited the platform as it develops.

因此，基于所有这些考虑，在 Android 1.0 中，使用一个单独的线程将每个 View 都绘制到单个纹理中，然后再将这些纹理组合在一起提供给 window 实际上是得不偿失的。与其把时间花在这上面，我们更宁愿将时间花在其他类似布局层级（为不同尺寸的屏幕提供弹性布局），notifications 和 widgets 使用到的 “remote views”上，这些内容对平台开发有显著的好处。

In fact it was just not feasible to implement hardware accelerated drawing inside windows until recently. Because Android is designed around having multiple windows on the screen, to have the drawing inside each window be hardware accelerated means requiring that the GPU and driver support multiple active GL contexts in different processes running at the same time. The hardware at that time just didn’t support this, even ignoring the additional memory needed for it that was not available. Even today we are in the early stages of this -- most mobile GPUs still have fairly expensive GL context switching.

其实直到最近，在 window 中实现硬件加速绘图还都是不可行的。由于 Android 本身的设计，一个屏幕上面存在多个 window，如果要在每个 window 中都使用硬件加速，就意味着GPU 需要支持多个进程中的同时运行活动的 GL 上下文。当时的硬件无法满足这一条件，甚至都不谈要实现这种特性额外需要的内存都无法满足。即使在今天，我们都处在革命的早期阶段 - 大多数移动设备的 GPU 在进行 GL 上下文切换的时候，还是相当昂贵的。

I hope this helps people better understand how Android works. And just to be clear again from my last point -- I am not writing this to make excuses for whatever things people don’t like about Android, I just get tired of seeing people write egregiously wrong explanations about how Android works and worse present themselves as authorities on the topic.

我希望这有助于人们更好地了解Android的工作机制。再次申明我的观点 - 我不是替那些人们不喜欢的 Android 特性辩解，我只是厌倦了看某些人“专家”般的关于 Android 工作机制的高谈阔论，然而他们只是不懂装懂而已。

There are of course many things that can be improved in Android today, just as there are many things that have been improved since 1.0. As other more pressing issues are addressed, and hardware capabilities improve and change, we continue to push the platform forward and make it better.

当然，直到今天，Android 也有很多可以改善的地方，就像 1.0 版本以来已经改善了很多很多一样。至于其他更紧迫的问题得到解决，以及硬件能力提升和变化，我们将继续推进平台，使其更好。

One final thought. I saw an interesting comment from Brent Royal-Gordon on what developers sometimes need to do to achieve 60fps scrolling in iOS lists: “Getting it up to sixty is more difficult—you may have to simplify the cell's view hierarchy, or delay adding some of the content, or remove text formatting that would otherwise require a more expensive text rendering API, or even rip the subviews out of the cell altogether and draw everything by hand.”

最后，我看到 Brent Royal-Gordon 发表的关于“怎样才能在 iOS 上实现 60fps 的列表滚动”的一个有趣评论：“实现 60fps 是相当困难的，你可能需要精简一下 view 的视图层次结构，或者延迟加一些的内容，或删除一些昂贵的文本格式化操作，甚至可能需要移除子 View 然后完全手工绘制它们。“

I am no expert on iOS, so I’ll take that as as true. These are the exact same recommendations that we have given to Android’s app developers, and based on this statement I don't see any indication that there is something intrinsically flawed about Android in making lists scroll at 60fps, any more than there is in iOS.﻿

我并不精通iOS，因此我认为上述说法是符合实际的。这些同样也是我们给 Android 应用开发人员的建议。而且从这句话看来，没有任何迹象表明相比 iOS， Android 存在内在缺陷在让 ListView 以 60 fps 滑动
