---
layout: post
title:  "【computer】chrome缓存设置"
date:   2016-12-18 08:00:00 +0800
categories: computer
tag: [computer]
---

使用浏览器调试 http 缓存头的时候，有一些需要注意的地方。一个显著的问题是刷新（F5）或者地址栏输入网址方式（Enter）访问页面，所有请求都会自动设置 Cache-Control:max-age=0。
如果是强制刷新（SHIFT + F5）的方式，所有请求都会自动设置 Cache-Control:no-cache。

另外，控制台（Network）也有一个 “disable cache” 的选项，需要注意。 

启用 stale-while-revalidate 扩展，这个需要通过 chrome://flags 设置，将 stale-while-revalidate 设置为 enable。

### 参考

1. [https://www.fedepot.com/she-zhi-flask-xiang-ying-qing-qiu-tou-shi-xian-jing-tai-zi-yuan-chang-shi-huan-cun/](https://www.fedepot.com/she-zhi-flask-xiang-ying-qing-qiu-tou-shi-xian-jing-tai-zi-yuan-chang-shi-huan-cun/)
2. [https://superuser.com/questions/313131/how-do-i-stop-chrome-sending-cache-control-max-age-0-when-i-hit-enter](https://superuser.com/questions/313131/how-do-i-stop-chrome-sending-cache-control-max-age-0-when-i-hit-enter)
3. [http://techblog.tilllate.com/2008/11/14/clientside-cache-control/](http://techblog.tilllate.com/2008/11/14/clientside-cache-control/)