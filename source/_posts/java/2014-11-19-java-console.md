---
layout: post
title:  "控制台输入小节"
date:   2014-11-19 12:46:04 +0800
categories: java
tag: [java]
---
## BufferedReader

最基础的方法，从System.in输入流中获取数据

```java
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    try {
        System.out.println(br.readLine());
    } catch (IOException e) {
        e.printStackTrace();
    }
```

## Scanner

```java
    Scanner sc = new Scanner(System.in);
    System.out.println(sc.nextLine());
```

## Console
java6新增

```java
    Console console = System.console();
    if(console != null){
        System.out.println(console.readLine());
    }
```

## 说明

1. Console主要是为了方便程序与用户交互，但是有一个限制就是需要使用系统自带的控制台来运行程序，如果在IDE中使用的话，就有很大的可能获取不到Console。

2. Console的另一个特点就是可以隐藏密码：

```java
        Console console = System.console();
        if(console != null){
            System.out.println(console.readPassword());
        }
```
    这样就看不到用户输入的密码了，但是没有办法将用户的输入显示成“*”或者别的字符

3. Scanner方便将用户的输入转换成对应的java类型，另外，Scanner的输入源不限于System.in，还可以是其他的输入源。
