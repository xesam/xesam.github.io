---
layout: post
title:  "HTTP的请求头部是怎样从nginx传递到应用的"
date:   2027-12-31 08:00:00 +0800
categories: computer
tag: [computer]
---
These days almost all web development is done with frameworks. Whether you use rails, Sinatra, or Lotus, you don't really have to think about how cookies and other headers pass from nginx or apache, to the application server and into your app. They just do.

We're going to examine this journey in a little more depth. Because it turns out that the story of headers contains a lot of interesting information about the history of the web.

现在，我们在进行 Web 开发的时候，基本都会使用开发框架，不论你是使用 rails，Sinatra 或者 Lotus，你都不需要关心 cookies 以及其他头部信息是怎样从 nginx 或者 apache 这样的 Web 服务器传递到你的应用服务器然后再到你的应用中的。今天我们就来聊一聊这个过程。


What are HTTP headers anyway?
Whenever a web browser makes a requesnginxt, it sends along these things called HTTP headers. They contain cookies, information about the user agent, caching info — a whole lot of really useful stuff.

You can see what headers are being sent by looking at a request in your browser's development tools. Here's an example. As you can see, the headers aren't anything magical. They're just text formatted in a certain way.