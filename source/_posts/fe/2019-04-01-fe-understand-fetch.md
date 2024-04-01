---
layout: post
title: "如何理解Fetch Api"
date: 2019-05-01 08:00:00 +0800
categories: fe
tag: [fe]
---

关于 Fetch Api，接受度越来越高了。网上很多文章在介绍 Fetch 的用法，在鼓吹 Fetch 的优势，也有人在撰文批评 Fetch 的难以使用。
但是，当我们在讨论 Fetch Api 的优点和缺点的时候，我们在讨论什么？如果不清楚一个接口的设计目的，又如何去评判这个设计？

<!-- more -->

从我个人看来，我觉得我们需要明确以下两点：

## 第一、Fetch Api 是一个“底层”接口

这个“底层”的意思并不是说这个 api 有操纵 OS 或者浏览器原生特性的能力，而是说这个接口是 Web 的底层。
Fetch Api 属于 WEB API，不是一个高度封装接口。竞争对手不是jquery，不是axios，也不是其他的 HTTP 库。

所以，fetch api 本身就不是给普通开发者用的，而是给库开发者用的。就像在 java 里面，你通常不会直接通过 socket 去执行 http 请求一样。所以，不要站在普通开发者的视角来看这些问题，如果你想像用 axios 一样来使用 fetch，你就掉坑里了。

## 第二、Fetch Api 是由 whatag （对比一下 W3C） 制定的。

随着 web 和 js 的领域扩张，如果 Web 想成为一个通用平台，如果 js 想成为一个成熟的平台语言，那么 API 的底层化和标准化是不可避免的，不跳出浏览器这个束缚，是达不到目的的。

1. 站在语言的角度，js 竞争的是 java，是 python，是其他的通用平台语言。

2. 站在平台的角度，Web 竞争的是其他平台，是 windows，是android，是ios。

3. 站在标准的角度，规范要统一的是浏览器，是Node，也是其他的 Web 运行宿主。

当前 XMLHttpRequest 面临的困境是，XMLHttpRequest 满足不了 web 的扩展（不论是横向扩展还是纵向扩展）。而不是因为 XMLHttpRequest 有什么内在缺陷。所以 Fetch 重新模块化了各个部分，

    Request
    Response

    Header
    Body

显然，这种架构根本就是对 Http 协议的复刻，因为 Http 才是 Web 的底层协议。

如果我们能记住以上两点，我们就能理解那些槽点：

1. fetch api 备受苛责点的“错误处理”。404、502之类的状态码被认为是 “resolved” 不是一目了然吗？因为对于一个底层接口来说，网络是正常的，只是你的服务不正常。
2. Request 默认是不带 cookie。这个在我看来是改进，而不是槽点，“如无必要,勿增实体”。
3. 不支持取消请求。说实话，这才真的是一个槽点。不过这只是一个暂时缺失的点，而不是接口设计如此。 AbortController 已经在实现中了，而且最新的浏览器已经实现了。不过，最后使用当然不会像 XMLHttpRequest 直接调用 abort() 这么简单。
4. 如果还有其他问题，请参照对比 Fetch 与 Socket。