---
layout: post
title: "小程序路由"
date: 2021-01-01 08:00:00 +0800
categories: fe
tag: [fe]
---
对于一个客户端应用来说，页面之间的关系主要有三种：

1. 打开新页面，保留当前页面。对应 xx.navigateTo();
2. 打开新页面，替换当前页面。对应 xx.redirectTo();
3. 关闭当前页面，回到上一个页面。对应 xx.navigateBack();

<!-- more -->

还有一个方法 xx.switchTab()，这个方法限制太多，通常没什么用。

以微信小程序为例，打开新页面page1的方式:

```javascript
wx.navigateTo({
    url:'/pages/page1/index?a=1&b=2'
});
```
这种使用方法存在两个不方便的地方：

1. 硬编码 url 被分散到各个不同的文件中，重构之后每个相关的文件都需要改动；
2. 传递参数需要手动拼接；

所以在开发小程序的过程中，我封装了一个小程序的路由辅助库，用以简化页面之间的跳转。

## Demo

参考地址 [miniapp-router](https://github.com/xesam/miniapp-router)

## 基本使用

添加依赖：

```json
  "dependencies": {
    "miniapp-router": "0.1.1"
  },
```

配置路由 router.js ：

```javascript

// router.js 定义路由
const router = new Router();
router.use({
    name:'page1',
    path:'/pages/page1/index'
});
router.use({
    name:'page2',
    path:'/pages/page2/index'
});
```

执行跳转 /page2/main/index.js：

```javascript

// 跳转到 page1 页面
router.push({name:'page1', params:{a:1, b:2}});
```

以上是配置 Router 的标准方法，这么定义其实挺麻烦，所以提供了一些简化手段：

一、 指定 basePath。还是以上面的代码举例，两个页面都在 /pages 目录下面，所以可以这么配置：

```javascript

// 定义路由
const router = new Router({basePath:'/pages'});
router.use({
    name:'page1',
    path:'page1/index' // 注意相对地址不要加前缀斜杠 '/'。
});
router.use({
    name:'page2',
    path:'page2/index' // 注意相对地址不要加前缀斜杠 '/'。
});

// 跳转到 page1 页面
router.push({name:'page1', params:{a:1, b:2}});
```

二、上面的方式中，虽然不用再指定目录，但还是有重复。如果我们遵循相同的 /pages/${name}/index 命名方式，就可以使用默认配置：

```javascript

// 定义路由
const router = new Router({basePath:'/pages'});
router.use({
    name:'page1'
});
router.use({
    name:'page2'
});

// 跳转到 page1 页面
router.push({name:'page1', params:{a:1, b:2}});
```

三、如果 name 与目录名始终保持一致，也可以使用约定配置：


```javascript

// 定义路由
const router = new Router({basePath:'/pages'});
// 跳转到 page1 页面
router.push({name:'page1', params:{a:1, b:2}});
```
推荐尽量采用约定配置的形式，避免维护太多的配置，也可以保持代码结构一致。


大致原理就是 router 获取页面的名称 name，然后结合 basePath 获得最终的路径 ${basePath}/${name}/index，然后拼接参数 params ，得到最终的 url。

如果当前工程不是 ${basePath}/${pageName}/index 的形式，解决办法有两种：

一、自定义Router，覆盖 Router 的 getPathByName() 方法。比如，如果你的页面命名方式是 /pages/${name}/${name} 的形式，那么可以这么定义：

```javascript   
class CustomRouter extends Router {
    getPathByName(name) {
        return `${this.basePath}/${name}/${name}`;
    }
}

const router = new CustomRouter({basePath:'/pages'});
router.push({name:'page1', params:{a:1, b:2}}); // 这样就会跳转到 /pages/page1/page1?a=1&b=2

```

二、配置 name 对应的 path。这种处理方式适用于只有部分几个页面命名比较特异的情况，比如已经分发给第三方的页面，无法随意修改页面路径的情况。

```javascript
// 定义路由
const router = new Router({basePath:'/pages'});
router.use({
    name:'page1',
    path:'/another/pages/page1/special'
});
router.push({name:'page1', params:{a:1, b:2}}); // 跳转到 /another/pages/page1/special?a=1&b=2
router.push({name:'page2', params:{a:1, b:2}}); // 跳转到 /pages/page2/index?a=1&b=2
```

## 子路由

小程序应用分为几个模块，可以分别为每一个模块创建一个路由，最后在父路由中进行装配。

目录结构：

```
/pages
    --shop
        --router.js
        --index
            --index.wxml
        --product
            --index.wxml
    --user
        --router.js
        --index
            --index.wxml
        --friends
            --index.wxml
app.js
```

定义 shop 模块的路由。

```javascript
    const router = new Router({basePath:'/pages/shop/'});
    module.exports = router;
```

定义 user 模块的路由。

```javascript
    const router = new Router();
    module.exports = router;
```

在 app.js 中进行组装：

```javascript
    const shopRouter = require('./pages/shop/router.js');
    const userRouter = require('./pages/user/router.js');
    const appRouter = new Router();
    appRouter.use('shop', shopRouter); // 直接使用 shopRouter 的 basePath 
    appRouter.use('user', shopRouter, {basePath:'/pages/user/'});// 覆盖 userRouter 的 basePath
```

使用 shopRouter 执行跳转：

```javascript
    shopRouter.router.push({name:'product'}); // 或者 shopRouter.router.push({name:['product']});
```

使用 appRouter： 执行跳转：

```javascript
    appRouter.router.push({name:['shop', 'product']});// 这里是数组的形式
```

通常，在模块内部，推荐使用各个模块自身的路由。只有在模块之间跳转的时候，才考虑使用父路由。

## 相关问题

### 为何需要 basePath?

因为小程序在运行过程中没法自动确定当前脚本的目录，可以在常见 Router 实例的时候配置默认 basePath，也可以在挂载根路由的时候配置 basePath，跟路由的配置优先级更高，会覆盖各个路由默认的 basePath。

## 更多
更多方法与配置，可以参考 demo、 test 以及源码。