---
layout: post
title:  "【Android】Cupboard非官方翻译"
date:   2017-02-07 13:46:04 +0800
categories: android
tag: [android]
---
Cupboard 是一个适用于 Android 的持久化存储方案，简单而且容易与现有代码集成。

更准确的说， Cupboard 只是一个存取对象方案。为了保简洁，它并不会去维护对象之间的关系，所以也并不是一个真正的ORM。

## 设计理念
设计 Cupboard 是因为现有的持久化框架并不能满足实际的需求，我们真正想要的是：

1. 非侵入的：不必要继承某个特殊的Activity，model 也不必要去实现某个特殊的接口，甚至都不必要实现 DAO 模式
2. 通用的选择：在整个应用中都可以使用所定义的 model 对象，而并不局限于数据库
3. 完美适应 Android 自有的类，比如 Cursor 以及 ContentValues，这样，可以在任何时候回退到 Android 框架本身的实现

## 官网

[Cupboard 官网(目测被墙了)](https://bitbucket.org/littlerobots/cupboard)

## 官方文档的非官方翻译

参见 [官方文档的非官方翻译 https://xesam.github.io/cupboard-cn/](https://xesam.github.io/cupboard-cn/)

### 使用

引入 Cupboard 依赖，然后静态导入 cupboard():

build.gradle:

```gradle
    compile 'nl.qbusict:cupboard:(insert latest version)'
    //最新是 2.2.0 所以可以这么写： compile 'nl.qbusict:cupboard:2.2.0'
```

java 类:

```java
    import static nl.qbusict.cupboard.CupboardFactory.cupboard;
```

在代码中可以这么调用：

```java
    public long storeBook(SQLiteDatabase database, Book book) {
        return cupboard().withDatabase(database).put(book);
    }
```

上面的代码将一个 Book entity 存入数据库中，然后返回记录的 id， 就这么简单！

更多参见 [Cupboard 非官方翻译](https://xesam.github.io/cupboard-cn/)