---
layout: post
title:  "开发模式-框架隔离"
date:   2021-03-04 09:00:00 +0800
categories: computer
tag: [computer]
---

在做一般的应用产品开发时，通常会基于特定的平台（比如 Android、iOS）、框架（Vue、React）或者技术标准（Servlet）等等。
这些开发平台通常经过精心设计，给程序员提供一个受控环境和开发模板，程序员在这个特定的环境中按照开发平台的规范进行开发。

<!-- more -->

## 背景介绍

典型案例是开发平台提供一系列组件构造器，并预定义好组件的生命周期方法：

    onCreated
    onShow
    onHide
    onDestory

程序员无权忽略或者调整生命周期方法的调用时机以及调用顺序，只能配置指定的生命方法；
或者执行某个操作，由开发平台决定是否执行以及何时执行某个生命周期方法。

常见的组件构造器有两种实现方式：

1、组件类

```javascript

class Page(){
    onCreated(){
    },
    onShow(){
    },
    onHide(){
    },
    onDestory(){
    }
}

```

使用者需要继承此类，然后定义自己的业务操作。

```javascript

class HomePage extends Page(){
    onCreated(){
        this.loadData();
    },
    ...
}

```

2、组件方法

```javascript

function Page(option){
    option.onCreated();
    option.onShow();
}

```

使用者传入配置对象，然后定义自己的业务操作。

```javascript

Page({
    onCreated(){
        this.loadData();
    },
    ...
})

```

其中，第 2 种方式（组件方法）相较于第 1 种方式（组件类）更为灵活，因为任意数据都可以附加在参数对象上直接传入。
但第 2 种方式的缺点也比较明显，无法继承父类方法，不过对于层级比较简单的组件，缺点也不算太明显。

## 框架隔离

在实际开发中，我们通常不应该直接使用开发平台提供的原始组件构造器，原因如下：

1. 原始的组件类或者构造方法无法更改，如存在公共方法，只能在每个组件中各自添加。
2. 后续要引入第三方框架，就需要每个组件分别修改了。

所以，较好的选择是在原始组件构造器与具体的组件之间，插入一个全局的公共构造器中间层，作为后续改进的一个缓冲区。

中间层的基本原则是**渐进增强，平稳回退**，或者说，最好是**无感的**。具体表现就是：

1. **调用形式不变**。调用中间层的方式与调用原始构造器的方式没有区别，最好是连构造器的名称也不变。
2. **逻辑结果不变**。使用中间层的结果与直接原始构造器的结果没有业务逻辑上的差别，即不要在中间层添加专属于部分组件的业务逻辑。

## 实现方式

对于*组件方法*的方式，由于所有的配置都是通过参数传入的，因此，我们可以这样来定义中间层：*拦截配置参数然后对其进行操作（增强、修改等等）*。

```javascript
middleware = function(option){
    return option;
}
//具体组件
Page(middleware({
    onCreated(){
        this.loadData();
    },
    ...
}))

```
可以在 middleware 函数操作 option。不过这种调用繁琐而迷惑，可以选择同时修改构造器，把 middleware 融入其中：

1. 直接替换（屏蔽）原始的组件方法。

```javascript

oldPage = Page;

Page = function(option){
    return oldPage(middleware(option));
}

//具体组件
Page({
    onCreated(){
        this.loadData();
    },
    ...
})

```
这种方式的好处太明显了——基本什么都不用改，在应用启动的时候完成替换就行。
缺点也很明显，安全性太低，如果某个第三方偷偷修改了 Page ，就可能导致安全隐患。
所以，一般框架都会禁止替换原始构造器。

2. 包装原始的组件方法。

```javascript

_Page = function(option){
    return Page(middleware(option));
}

//具体组件
const {_Page} = require('_Page');
_Page({
    onCreated(){
        this.loadData();
    },
    ...
})

```

如果框架允许的话，可以进一步：

```javascript
//具体组件
const {_Page as Page} = require('_Page');
Page({
    onCreated(){
        this.loadData();
    },
    ...
})

```
以此减轻修改负担。


对于 *组件类* 的方式，我们可以这样来定义中间层：

```javascript

class BasePage extends Page(){
    onCreated(){
        this.before();
        super.onCreated();
        this.after();
    },
    ...
}

//具体组件
class PageA extends Page(){
    onCreated(){
        super.onCreated();
        this.loadData();
    },
    ...
}
```

对于那些类似 Java 约束较多的语言，这种方式比较直观。当然，通过注解也一定可以：

```java
//具体组件
@BasePage
class PageA extends Page(){
    onCreated(){
        super.onCreated();
        this.loadData();
    },
    ...
}
```

## 结语

以上是内部新人培训记录，实际上，相同功能的第三方框架很多，但是我都不太喜欢，不喜欢的原因主要可以概括为：

1. 侵入性太强。比如重新定义了一套构造方式，强迫开发者去适应第三方框架的思路。
2. 需要编译工具支持，特别是通过代码生成方式来实现的工具，调试起来相当麻烦。
3. 最重要的原因，第三方框架更新不及时，无法支持开发平台的新特性，而且第三方框架动不动就黄了！

我的意思也并不是鼓励造轮子，而是要谨慎选择一个框架。
在打算使用择框架之前，*先问目的*，在选择框架的时候，*谨慎取舍*。

