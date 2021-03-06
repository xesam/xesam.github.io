---
layout: post
title:  "传值调用与传引用调用"
date:   2016-10-21 16:51:38 +0800
categories: computer
tag: [computer]
---
这个问题的关键是明确“传值调用（Call by value）”与“传引用调用（Call by reference）”的定义。

简单来说：

    “传值调用”是将值（values）作为函数参数传入；
    “传引用调用”是将变量（variables）本身作为函数参数传入；

一个隐喻：

    “传值调用”是我在纸片上写下一些内容并把纸片交给你， 内容可以是一个URL，也可能是一份完整的《战争与和平》副本。
    不管是什么，现在都在我给你的那张纸上，所以它实际上是你的纸。你可以在那张纸上随便涂鸦，也可以通过那张纸找到别的什么东西。
    
    “传引用调用”是当我在我的笔记本上写了一些内容然后把笔记本递给你。
    你可以在我的笔记本上涂鸦（也许我想要你这么做，也许我没料到你会这么做），然后我保留我的笔记本，你的任何涂鸦也一并保留在笔记本里。
    此外，如果你或我写的是有关如何找到其他内容的信息，无论你或我可以去那里，更改这些信息。

<!-- more -->

## 常见误解

注意，这两个概念与“引用类型（reference types）”或者“指针类型（pointer types）”的概念是完全独立和正交的，所谓“引用类型”，就是 Java 中 Object 的子类型，C＃ 中的所有 class 类型；所谓“指针类型”类似 C 语言中指针的概念，在语义上等同于 Java 的“引用类型”。

“引用类型”的概念对应于一个 URL ：它本身是一条信息，一个到其他信息的引用（或者一个指针）。你可以在不同的地方拥有多个网址副本，而且他们不会更改他们所有链接到的网站; 如果网站被更新，则每个 URL 副本将指向更新后的信息。 相反的，在任何一个 URL副本的更改不会影响到任何其他的 URL 副本。

注意 C++ 有一个概念叫“引用（references）”（例如 &int），它不像 Java 和 C＃ 的“引用类型”，而是像“传引用调用”。 Java 和 C＃ 中的“引用类型”以及 Python 中的所有类型都更像是 C 和 C ++ 中的“指针类型（pointer types）”（例如int *）。

## 术语定义

首先，需要强调一些重要的术语，并确保我们对所用词汇的理解都达成一致。在实践中，词不达意的词汇，是导致绝大多数概念混淆的一个重要原因。

首先，定义一个函数：

```c
void foo(int param) {  // line 1
    param += 1;
}
```

然后调用此函数：

```c
void bar(){
    int arg = 1; // line 2
    foo(arg);    // line 3
}}
```

通过这个例子，我想定义一些重要的术语：

1. foo 是在第1行声明的函数（ C 和 C ++ 区分声明和定义，在 Java 中，函数声明和定义是合二为一的，但是概念是相同的，这里不作深入讨论）
2. param 是 foo 的形式参数（formal parameter，后文简称“形参”），也在第1行声明
3. arg 是一个变量（variable），在第2行上声明和初始化，是函数 bar 的局部变量（ local variable）
4. arg 也是第3行上 foo 调用（invocation）的参数（argument）

这里有两组非常重要的概念要区分。

#### 第一组概念是“值（value）”与“变量（variable）”：

值（value）是对语言中表达式进行求值的结果。例如，在上面的 bar 函数中， int arg = 1 ; 执行之后，表达式 arg 的值（value）为 1。

变量（variable）是“值（value）”的容器。变量可以是“可变的（mutable）”，这是大多数类似C语言的默认值，或者“只读的（read-only）”，例如使用 Java 的 final 或 C＃ 的 readonly 声明，又或者完全不可变的，例如使用 C++ 的 const。

#### 另一组概念是“形参（parameter）”与“实参（argument）”：

形参（formal parameter）是调用函数时必须由调用者（caller）提供的“变量（variable）”。

实参（argument）是由函数的调用者提供以满足该函数形参的特定形式参数的“值（value）”。

## 传值调用

在“传值调用”中，函数的形参是为了调用函数所新创建，并使用实参值初始化的变量。
这与用值来初始化任何其他类型变量的方式完全相同。例如：

```c
    int arg = 1;
    int another_variable = arg;
```

这里 arg 和 another_variable 是完全独立的变量 - 它们的值可以彼此独立地变化。因为，在声明 another_variable 的时候，它就被初始化为保持与arg所保持的相同的值：也就是数值 1。

由于它们是独立变量，对 another_variable 的更改不会影响 arg：

```c
    int arg = 1;
    int another_variable = arg;
    another_variable = 2;

    assert arg == 1; // true
    assert another_variable == 2; // true
```

这与上例中 arg 和 param 之间的关系完全相同，对比一下：

```c
    void foo(int param) {
      param += 1;
    }

    void bar() {
      int arg = 1;
      foo(arg);
    }
```

它就好像我们这样编写代码：

```c
    //在这里进入函数“bar”
    int arg = 1;
      //这里进入函数“foo”
      int param = arg;
      param += 1;
      //在这里退出函数“foo”
    //在这里退出函数“bar”
```

也就是说，“传值调用”的定义特征是“被调用者（callee）”（即foo）接收值（values）作为参数（ arguments），对于这些传入的值，相对于“调用者（caller）”（即bar）的变量，“被调用者”具有其自己的独立变量（variables）。

回到上面的隐喻，如果我是 bar，你是foo，当我调用你的时候，我给你一张纸上写着一个值（value）。你称这张纸为 param，该值是我写在笔记本（本地变量）上，被称为 arg 的变量的副本。

（另外：一个函数调用一个函数的各种调用约定（ calling conventions），取决于所用的硬件和操作系统。所谓“调用约定”，就像我们共同来约定是我将值写在一张纸上，然后交给你，还是你本身就有一张纸，我直接把值写在上面，又还是我把值写在我们都能看到的墙上。这是一个有趣的话题，但与本话题无关）

## 传引用调用

在“传引用调用”中，函数的形参仅仅是调用者提供的实参的新名称（new names）。

回到上面的例子，它等同于：

```c
    //在这里进入函数 “bar”
    int arg = 1;
      //这里进入函数 “foo”
      //啊哈！我注意到 “param” 只是另一个名字 “arg”
      arg /* param */ += 1;
      //在这里退出函数 “foo”
    //在这里退出函数 “bar”
```

由于 param 只是 arg 的另一个名称，也就是说，它们是同一个变量（the same variable），param 的更改反映到 arg 上。这是“传引用调用”不同于“传值调用”的根本之处。

很少有语言支持传引用调用，但 C++ 可以这样做：

```c
    void foo(int& param) {
      param += 1;
    }

    void bar() {
      int arg = 1;
      foo(arg);
    }
```

在这种情况下，param 不仅具有与 arg 相同的值（value），它实际上就是 arg（只是名称不同而已），因此 bar 可以观察到 arg 已经增加。

注意，这不是 Java，JavaScript，C，Objective-C，Python 或任何其他流行语言的执行方式，也就意味着这些语言不是“传引用调用”的，它们是“传值调用”的。

## 附录：对象共享调用（call by object sharing）

如果在“传值调用”中，实际的值是一个引用类型（reference type）或指针类型（pointer type），那么“值”本身不是什么特别的（例如在 C 语言里面，它只是一个平台特定大小的整数），特别的是”值”所指向的内容。

如果引用类型（或者说指针）指向的是可变值（mutable）的，那么一个可能的效果是：你可以修改被指向的值，并且调用者可以观察到被指向值的变化，即使调用者不能观察到这个引用类型本身的更改。

再次借用URL的隐喻：

    我给你一个网站 URL的副本，我们关心的是网站，而不是URL。
    无论你如何更改你的 URL 副本，都不影响我的 URL 内容
    （实际上，在 Java 或者 Python 这样的语言中，“URL”或引用类型值，他们本身的值根本就不能被修改，只有它指向的东西可以被修改）。

当 Barbara Liskov 发明 CLU 编程语言时，她意识到现有的术语“传值调用”和“传引用调用”对描述这种新语言的语义并不是特别有用。所以她发明了一个新的术语：共享对象调用（call by object sharing）。

对于通过“传值调用”，但实际使用中的常用类型是引用或指针类型（即：几乎每一种现代命令式，面向对象或多范式编程语言）的语言，只需要避免谈论“传值调用”或“传引用调用”，而坚持通过“共享对象调用”（或简单地“传对象调用”），就没有人会困惑了。

参考 [http://stackoverflow.com/questions/373419/whats-the-difference-between-passing-by-reference-vs-passing-by-value/34971934#34971934](http://stackoverflow.com/questions/373419/whats-the-difference-between-passing-by-reference-vs-passing-by-value/34971934#34971934)
