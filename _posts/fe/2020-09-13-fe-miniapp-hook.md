---
layout: post
title: "小程序hook"
date: 2020-09-13 08:00:00 +0800
categories: fe
tag: [fe]
---

在开发一个客户端应用时，通常都需要按照框架定义的模式来编写代码，最常见的是覆盖框架定义好的生命周期方法。

以微信小程序为例，当我们定义一个页面的时候，模板代码如下：

<!-- more -->

```javascript
Page({
  data: {
    text: "This is page data."
  },
  onLoad(options) {
    // Do some initialize when page load.
  },
  onShow() {
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
但是这么做会面临一个问题，有的平台是禁止重新赋值内置函数的。比如微信小程序，如果重新赋值了 Page 函数，在使用插件了之后，就会报错。所以，尽量不要去重新赋值框架函数，所我们可以自定义一个框架包装函数 Page.js：
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


为了方便操作，我做了一个 hook 辅助函数 [https://github.com/xesam/miniapp-hook](https://github.com/xesam/miniapp-hook)，用来方便的定义自己的中间层：

package.json
```json
{
  "dependencies": {
    "miniapp-hook": "0.1.1"
  }
}
```

在入口函数 app.js 处：

```javascript
const {_Page, pageLogger} = require('miniapp-hook');

_Page.use(pageLogger);
_Page.use(...) //这里可以定义自己的拦截函数

App({
    onLaunch (options) {
    }
})
```

具体的页面 pages/sample/index.js

```javascript
const {_Page} = require('miniapp-hook');

_Page({
    onLoad(query) {
    }
})
```

同理，我们使用类似的方式可以拦截 App、Component以及其他任何方法。

### 问题

#### 问题一、如果我不想使用库里面的 _Page() 这种带下划线的方法怎么处理？
可以对 _Page 重新导出或者包装到一个新函数里面。

#### 问题二、如果应用中已经使用了自己包装过的 Page() 等方法怎么处理？
可以对自定义的 Page 再次包装，只要签名与框架原始的 Page() 保持一致就行：

```javascript
const {_Page, pageLogger} = require('miniapp-hook');

const NewApp = _Page.create(OldPage); // OldPage 是已经自定义的的包装函数
NewApp.use(...) //这里可以定义自己的拦截函数

export default NewApp;
```

具体的页面 pages/sample/index.js

```javascript
const {NewApp} = require('miniapp-hook');

NewApp({
    onLoad(query) {
    }
})
```

### 注意事项

1. 只有全局的操作或者数据才应该在中间层添加，比如解码参数、打印日志等等，不要在中间层中进行与某个页面相关的业务操作，页面相关的业务应该留在各自的页面内。
1. 需要小程序开启 npm 支持，所以对版本有一定的要求。当然，可以直接把源码复制到工程中，一样可以运行。
