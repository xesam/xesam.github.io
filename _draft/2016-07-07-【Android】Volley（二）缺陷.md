---
layout: post
title:  "【Android】Volley（二）缺陷"
date:   2016-07-07 13:46:04 +0800
categories: android
tag: [android]
---

[https://medium.com/@BladeCoder/some-missing-info-in-your-article-that-developers-need-to-be-aware-of-when-choosing-one-of-those-dac99d067a27#.buncvzeec](https://medium.com/@BladeCoder/some-missing-info-in-your-article-that-developers-need-to-be-aware-of-when-choosing-one-of-those-dac99d067a27#.buncvzeec)

内部直接使用 memory buffers 来缓存响应，然后在解析。即使对待 Image 或者比较大的响应也是如此。

内部依赖 Apache HttpClient，即使在 Android 新版本里面已经废弃了。

Retry Policy 太粗暴



