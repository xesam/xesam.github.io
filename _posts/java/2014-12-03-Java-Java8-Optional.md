---
layout: post
title:  "Java8 Optional"
date:   2014-12-03 12:46:04 +0800
categories: java
tag: [java]
---
按照字面意思的理解，应该可选的意思。一开始我还以为是类似python里面的默认参数用法呢，结果语义是指某个值可能有也可能没有（null）。
感觉名字取得不是很直观。。我觉得叫Nullable不是更好？

python： 

```python
    def fn(a='default_value'):
        print(a)
        pass
```

## Optional方法

Optional没有公开的构造方法，只有静态工厂方法：

```java
    Optional<String> optional_2 = Optional.of(str); // 如果str == null，抛出错误NullPointerException
    Optional<String> optional = Optional.ofNullable(str); // 如果str == null，返回一个空Optional<String>
    Optional.<String>empty(); // 返回一个空Optional<String>


    String s = optional.get(); //获取被包装的值
    optional.ifPresent((value) -> System.out.println("hello")); // 如果optional的value不是null，则执行函数表达式

    optional.orElse("elseValue"); // 如果optional的value为null，则返回"elseValue"
    optional.orElseGet(() -> "orElseGet"); // 如果optional的value不是null，则返回函数表达式的执行结果
    optional.orElseThrow(RuntimeException::new); // 如果optional的value不是null，则抛出错误
    
    
    optional.filter((value) -> value.length() == 5); // 过滤得到长度等于5的value
    
     optional.map((value) -> {
        System.out.println("map:" + value);
        return value;
    });

    optional.flatMap((value) -> {
        System.out.println("flatMap:" + value);
        return Optional.ofNullable(value);
    });
```    

### map 与 flatMap 的区别

map(mapper) 与 flatMap(mapper) 功能上基本是一样的，只是最后的返回值不一样。map(mapper)方法里面的mapper可以返回任意类型，但是flatMap(mapper)方法里面的只能返回Optional类型。

如果mapper返回结果result的不是null，那么map就会返回一个Optional<Object>,但是 flatMap 不会对result进行任何包装。一个常见的例子：

```java
    Optional<String> os;
    os.map((value)->Optional.of(value)) //返回的类型是Optional<Optional<String>>
    os.flatMap((value)->Optional.of(value)) //返回的类型是Optional<String>
```

## Optional的好处

1. 显式的提醒你需要关注null的情况，对程序员是一种字面上的约束

2. 将平时的一些显式的防御性检测给标准化了，并提供一些可串联操作

3. 解决一下null会导致疑惑的概念，比如Map里面的key==null的情况，以及value==null的情况

## 小节
不过Optional一下子有这么多方法，Optional的初衷是什么？而且Optional也是一个对象，所以它本身也有可能是null，这可如何是好。

所以，有个观点认为，Optional比较适用的地方是作为返回值，这样可以给使用者一个善意的提醒。

## 参考

1. [http://www.javacodegeeks.com/2013/09/deep-dive-into-optional-class-api-in-java-8.html](http://www.javacodegeeks.com/2013/09/deep-dive-into-optional-class-api-in-java-8.html)
2. [What's the point of Guava's Optional class](http://stackoverflow.com/questions/9561295/whats-the-point-of-guavas-optional-class)
3. [http://www.nurkiewicz.com/2013/08/optional-in-java-8-cheat-sheet.html](http://www.nurkiewicz.com/2013/08/optional-in-java-8-cheat-sheet.html)
