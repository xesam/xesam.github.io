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



This is why there are windows on Android. The status bar and its notification shade are windows owned and drawn by the system. These are separate from the application’s window, so the application can not touch anything about the status bar, such as to scrape the text of SMS messages as they are displayed there. Likewise the soft keyboard is a separate window, owned by a separate application, and it and the application can only interact with each other through a well defined and controlled interface. (This is also why Android can safely support third party input methods.)

这也是为什么 Android 要有 Window 的原因。StatusBar 以及 Notification 面板都属于系统的 Window，由系统负责绘制。因此，应用就无法访问或者修改 StatusBar 的任何内容，比如，无法读取通知栏显示的短信内容。同样，软键盘也是一个单独的 Window，属于另一个应用。当前应用只能通过一种定义良好的受限接口与输入法应用相交互。（这也是为什么 Android 可以安全的支持第三方输入法的原因）

Another objective of Android was to allow close collaboration between applications, so that for example it is easy to implement a share API that launches a part of another application integrated with the original application’s flow. As part of this, Android applications traditionally are split into pieces (called “Activities”) that handle a single specific part of the UI of the application. For example, the contacts lists is one activity, the details of a contact is another, and editing a contact is a third. Moving between those parts of the contacts UI means switching between these activities, and each of these activities is its own separate window.

Android 的另一个目标是支持应用间的无缝合作，比如，可以很方便的实现一个分享 API，从原始的应用平滑的启动另一个应用的相应部分，而不中断工作流。作为实现的一部分，Android 通常划分为片（也就是 Activity）来分别处理特定的 UI 任务。
比如，联系人列表是一个 Activity，联系人详情是另一个 Activity，联系人编辑页面也是一个 Activity。在这些界面间的移动也就是在这些 Activity 之间的切换，每个 Activity 都有自己的 Window。

Now we can see something interesting: in almost all of the places in the original Android UI where you see animations, you are actually seeing windows animate. Launching Contacts is an animation of the home screen window and the contacts list window. Tapping on a contact to see its details is an animation of the contacts list window and the contacts details window. Displaying the soft keyboard is an animation of the keyboard window. Showing the dialog where you pick an app to share with is an animation of a window displaying that dialog.

现在，你会发现有趣的地方，几乎所有你看到的 UI 动画，实际上都是 Window 动画。启动通讯录的时候，看到的是 Home Window 动画以及联系人列表 Window 动画，点击联系人查看详情的时候看到的是联系人列表 Window 动画以及详情页 Window 动画，显示输入法面板的时候，展示的是输入法 Window 动画，显示对话框的时候是对话框的 Window 动画。

When you see a window on screen, what you are seeing is actually something called a “surface”. This is a separate piece of shared memory that the window draws its UI in, and is composited with the other windows to the screen by a separate system service (in a separate thread, running at a higher than normal priority) called the “surface flinger.” Does this sound familiar? In fact this is very much like what iOS is doing with its views being composited by a separate thread, just at a less fine-grained but significantly more secure level. (And this window composition has been hardware accelerated in Android from the beginning.)

你在屏幕上看到的 Window，实际都是一个 “surface”。这是一段内存，window 使用它来绘制自己的 UI，通过一个称为“surface flinger.”的系统服务来与其他的 window 来组合。（这个系统服务运行在一个单独的线程里面，并拥有一个更高的优先级）
是不是听起来很熟悉，这种机制与 iOS 使用单独的线程来组合View 界面是类似的。并且 window 是从一开始就支持硬件加速。

The other main interesting interaction in the UI is tracking your finger -- scrolling and flinging a list, swiping a gallery, etc. These interactions involve updating the contents inside of a window, so require re-rendering that window for each movement. However, being able to do this rendering off the main thread probably doesn’t gain you much. These are not simple “move this part of the UI from X to Y, and maybe tell me when you are done” animations -- each movement is based on events received about the finger on the screen, which need to be processed by the application on its main thread.

另一个 UI 交互是追踪手指：滑动或者 flinging 列表，切换 Gallery 等等。这些交互都涉及到更新 Window 里面的内容，所以每一个动作都需要重新渲染窗口。然而，能够做到这一点呈现出主线程可能不会获得你多少。这些都不是简单的“移动从X到Y UI的这一部分，也许告诉我，当你完成”动画 - 每一个动作是基于收到有关屏幕上手指，每一个事件需要由应用程序的主线程来处理。

That said, being able to avoid redrawing all of the contents of the parts of the UI that are moving can help performance. And this is also a technique that Android has employed since before 1.0; UI elements like a ListView that want to scroll their content can call http://developer.android.com/reference/android/view/View.html#setDrawingCacheEnabled(boolean) to have that content rendered into a cache so that only the bitmap needs to be drawn as it moves.

也就是说，对于正在移动的 View，如果我们能够不用重绘所有的内容，那么会对性能产生好处。这也是 Android 在 1.0 版本之前就已经采用的技术;
类似 ListView 希望滚动其内容的 View 可以调用http://developer.android.com/reference/android/view/View.html#setDrawingCacheEnabled(boolean）将内容元素渲染到缓存中，如此依赖只有 bitmap 需要，因为它移动要绘制。

Traditionally on Android, views only have their drawing cache enabled as a transient state, such as while scrolling or tracking a finger. This is because they introduce a fair amount more overhead: extra memory for the bitmap (which can easily total to multiple times larger than the actual frame buffer if there are a number of visual layers), and when the contents inside of a cached view need to be redrawn it is more expensive because there is an additional step required to draw the cached bitmap back to the window.

传统上，在Android上的观点仅启用作为过渡状态的绘图缓存，如在滚动或跟踪手指。这是因为他们引入了相当多的开销：为位图额外存储器（其可以容易地总多次比实际帧缓冲器较大，如果有许多视觉层），而当一个高速缓存视图需要里面的内容重绘它是较昂贵的，因为有绘制缓存的位图回窗口所需的附加步骤。

So, all those things considered, in Android 1.0 having each view drawn into a texture and those textures composited to the window in another thread is just not that much of a gain, with a lot of cost. The cost is also in engineering time -- our time was better spent working on other things like a layout-based view hierarchy (to provide flexibility in adjusting for different screen sizes) and “remote views” for notifications and widgets, which have significantly benefited the platform as it develops.

因此，所有这些事情考虑，在Android中有被拉入纹理每个视图1.0和合成到另一个线程窗口的纹理只是没有那么多的增益，用了大量的成本。成本也是工程时间 - 我们的时间更好地用在像基于布局的视图层次其他的事情（提供灵活调节不同的屏幕大小），并通知和小工具“远程视图”，这已显著工作受益该平台因为它的发展。

In fact it was just not feasible to implement hardware accelerated drawing inside windows until recently. Because Android is designed around having multiple windows on the screen, to have the drawing inside each window be hardware accelerated means requiring that the GPU and driver support multiple active GL contexts in different processes running at the same time. The hardware at that time just didn’t support this, even ignoring the additional memory needed for it that was not available. Even today we are in the early stages of this -- most mobile GPUs still have fairly expensive GL context switching.

其实这只是不可行实现硬件里面的窗户加速绘图，直到最近。由于Android是围绕具有在画面上的多个窗口，让每个窗口是要求在不同的过程GPU和驱动器支承多个活动的GL上下文同时运行的硬件加速装置内的图。当时的硬件只是不支持这一点，甚至忽略了必要为它附加的内存，这是不可用。即使在今天，我们在这个早期阶段 - 大多数移动GPU还是相当昂贵的GL上下文切换。


I hope this helps people better understand how Android works. And just to be clear again from my last point -- I am not writing this to make excuses for whatever things people don’t like about Android, I just get tired of seeing people write egregiously wrong explanations about how Android works and worse present themselves as authorities on the topic.

我希望这有助于人们更好地了解Android的工作机制。再次申明我的观点 - 我不是替那些人们不喜欢的 Android 特性，我只是厌倦了看某些人关于 Android 工作机制的高谈阔论，然后他们只是不懂装懂而已。

There are of course many things that can be improved in Android today, just as there are many things that have been improved since 1.0. As other more pressing issues are addressed, and hardware capabilities improve and change, we continue to push the platform forward and make it better.

当然也有可以在Android的今天得到改善，就像有1.0以来已经改善了很多事情很多东西。至于其他更紧迫的问题得到解决，以及硬件能力提升和变化，我们将继续推进平台，使其更好。

One final thought. I saw an interesting comment from Brent Royal-Gordon on what developers sometimes need to do to achieve 60fps scrolling in iOS lists: “Getting it up to sixty is more difficult—you may have to simplify the cell's view hierarchy, or delay adding some of the content, or remove text formatting that would otherwise require a more expensive text rendering API, or even rip the subviews out of the cell altogether and draw everything by hand.”

最后，我看到 Brent Royal-Gordon 发表的关于“怎样才能在 iOS 上实现60fps的列表滚动”的一个有趣评论：“实现 60fps 是相当困难的，你可能需要精简一下 view 的视图层次结构，或者延迟加一些的内容，或删除一些昂贵的文本格式化操作，甚至可能需要移除子 View 然后完全手工绘制它们。“

I am no expert on iOS, so I’ll take that as as true. These are the exact same recommendations that we have given to Android’s app developers, and based on this statement I don't see any indication that there is something intrinsically flawed about Android in making lists scroll at 60fps, any more than there is in iOS.﻿

我并不精通iOS，因此我认为上述说法是符合实际的。这些同样也是我们给 Android 应用开发人员的建议。而且从这句话看来，没有任何迹象表明先比 iOS， Android 存在内在缺陷在让 ListView 以 60 fps 滑动
