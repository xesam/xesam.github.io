---
layout: post
title:  "var & let & const"
date:   2019-07-02 08:00:00 +0800
categories: javascript
tag: [javascript]
---
关于这个话题，我想要讨论的问题只有一个：什么时候应该用var，什么时候应该用 let，什么时候应该用const？

我的观点是，对于现代前端项目，有三个原则：

1. 任何时候都不要用 var
2. 能用 const 的地方都用 const
3. 不能用 const 的地方，就用 let

<!-- more -->

如果你的代码风格不是函数式风格，那么一个应用代码中最复杂的问题就是状态管理。说得更具体一点，就是变量的使用（取值与赋值）。不论是前辈给我们的谆谆教导，还是我们自己的代码实践，都告诉我们一个道理——可变量是痛苦的根源，变量的作用域一定要越小越好。在大众编程语言中：

1. 块作用与优于方法作用域
2. 方法作用域优于类作用域
3. 类作用域优于模块作用域
4. 模块作用域优于全局作用域

可以看出，全局变量是魔鬼，我们的头号敌人就是全局作用域，于是，var 以及 不加修饰的变量声明，就是我们最应该限制的使用方式。现在就剩下 let 与 const 的抉择了，我们看一下 let 与 const 的语义与特性：

    let 可以作用在块级作用域上，所声明的变量可以再次赋值。
    const 也可以作用在块级作用域上，所声明的变量不可以再次赋值。

抛开可能存在的性能问题不说，两者其实只有能否再次赋值这一个区别。回到现实所面临的代码问题，我们从来不担心变量的读操作，我们从来只关心变量的写操作。比如对于一个方法来说，一个不经意的赋值，修改了距离很远处的一个初始变量，这是一个比逻辑错误更难发觉的bug。再或者对于一个类来说，一个能修改实例状态的方法，你永远不知道会在哪里被哪个外部类调用。类似的情况下，如果一个变量根本就不能被改变，所有这些问题就不存在了。

各位可以回头翻一翻自己写过的代码，一个方法中所声明过的变量里面，再次赋值的比例是多少？如果变量被声明定义之后再也没有修改过，那为何要用 let？一开始就声明为 const 才是最好的选择。

更强的约束，意味着更好的协作。不要在此谈性能、谈效率。软件开发不是一个短期事件，软件运作的每一天，都在软件的生命周期内。所以性能问题，效率问题，都应该放在软件的整个生命周期来讨论，而不是放在开发人员那区区的编码周期中讨论。再者，性能问题是一个技术问题，而维护问题是一个管理问题，维护的每一天，都是在还开发时期的债务。

如果不是 var 的既成事实以及广泛存在，js 根本就只需要 var（let）以及 const 两个关键字（保留字）就能满足设计需求，现在却拥有三个，只是对现实的妥协而已。

*备注*

如果是简单的页面，出于兼容或者代码量的考虑，用 var 也许是一个好的选择。比如，一个移动端的下载提示页面，访问量大，且页面很简单，如果用 ES6 语法开发之后再转码的话，会增加大量的模板代码，是不划算的。这个时候，用 var 就显得性价比更高了。