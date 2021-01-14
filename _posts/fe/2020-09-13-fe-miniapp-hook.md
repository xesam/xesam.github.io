---
layout: post
title: "小程序hook"
date: 2020-09-13 08:00:00 +0800
categories: fe
tag: [fe]
---

以微信小程序为例，当我们定义一个页面的时候，模板代码如下：

<!-- more -->

```javascript
Page({
  data: {
    text: "This is page data."
  },
  onLoad: function(options) {
    // Do some initialize when page load.
  },
  onShow: function() {
    // Do something when page show.
  }
})
```

其中 Page() 是小程序提供的框架方法，而 onLoad、onShow 则是框架的生命周期方法。这是官方给出的使用方法，但是对于一个会长时间维护的项目来说，比较好的实践是尽量使用自定义的中间层来隔离原生框架的调用。所以可以这么做：


```javascript
const old = Page;
Page = function(options){
	old(options);
}
```
但是这么做会面临一个问题，有的平台是禁止重新赋值内置函数的。比如微信小程序，如果重新赋值了 Page 函数，在使用插件了之后，就会报错。所以，尽量不要去重新赋值框架函数，另一种方式就是自定义一个框架包装函数 Page.js：
```javascript
function _Page(options){
	Page(options);
}
export default _Page;
```
在具体的页面中可以使用 Page.js
```javascript
import Page from './Page';

Page({
  data: {
    text: "This is page data."
  },
  onLoad: function(options) {
    // Do some initialize when page load.
  },
  onShow: function() {
    // Do something when page show.
  }
})
```
如此一来，我们就可以在 Page.js 中进行各种操作，比如拦截 Page 的生命周期方法、添加一些全局数据等等之类的操作。


为了方便操作，我只做了一个 hook 辅助函数 [https://github.com/xesam/miniapp-hook](https://github.com/xesam/miniapp-hook)，用来方便的定义自己的中间层：


package.json
```json
{
  "dependencies": {
    "miniapp-hook": "0.0.2"
  }
}
```
在入口函数 app.js 处：
```javascript
const {Page, pageLogger} = require('miniapp-hook');

Page.add(pageLogger);
Page.add(...) //这里可以定义自己的拦截函数

App({
    onLaunch (options) {
    }
})
```
具体的页面 index.js
```javascript
const {Page} = require('miniapp-hook');

Page({
    onLoad(query) {
    }
})
```
同理，我们使用类似的方式可以拦截 App、Component以及其他任何方法。


### 注意事项

1. 只有全局的操作或者数据才应该在中间层添加，比如解码参数、打印日志等等，不要在中间层中进行与某个页面相关的业务操作，页面相关的业务应该留在各自的页面内。
1. 需要小程序开启 npm 支持，所以对版本有一定的要求。当然，可以直接把源码复制到工程中，一样可以运行。
