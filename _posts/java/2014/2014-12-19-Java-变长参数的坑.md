---
layout: post
title:  "【Java】变长参数的坑"
date:   2014-12-19 12:46:04 +0800
categories: java
tag: [java]
---
# 【Java】变长参数的坑

# VarArgs

## VarArgs简述
只需要明确一点即可，java方法的变长参数只是语法糖，其本质上还是将变长的实际参数 varargs 包装为一个数组。

所以

    Object[] objs
    
与

    Object... objs

被看作是相同的签名，在源码级别是不能同时存在的，因此，无法编译通过

## VarArgs包装

包装方式（注意，下面的代码不是实际的实现，而是一个比喻说明）:

1. 如果实参是唯一且匹配形参varargs要求的数组（就是实参独占形参varargs），那么可以认为你已经替编译器干了这个活，所以可以看作不包装，直接使用这个数组

```java
        public void invoke(String...varargs){}

        invoke(new String[]{"a", "b", "c"});
        那么大致的调用过程如下：
        public void invoke(String...varargs){
            innerVarArgs = varargs;
        }
```

2. 如果实参是多个单独的变量（就是多个实参分享varargs），那么会将这多个参数包装成一个相应的类型数组

```java
        public void invoke(String...varargs){}

        invoke("a", "b", "c");

        那么大致的调用过程如下：
        public void invoke(String...varargs){
            innerVarArgs = new String[varargs.length];
            for(int i = 0, size = varargs; i < size; i++){
                innerVarArgs[i] = varargs[i];
            }
        }
```

## 那么问题来了

### 问题一：当变长参数是Object... objs的情况

要知道，数组也是一个对象，所以会产生下面的情况：

```java
        public static void test1(Object... varargs) {
            System.out.println(varargs.length);
        }

        [1] test1(new String[]{"a", "b", "c"});   //3
        [2] test1(1, new String[]{"a", "b", "c"});//2

        [3] test1(new Integer[]{2, 3, 4});        //3
        [4] test1(1, new Integer[]{2, 3, 4});     //2
        [5] test1(1, new Integer[]{2, 3, 4}, new Integer[]{2, 3, 4});//3

        [6] test1(2, 3, 4);              //3
        [7] test1(new int[]{2, 3, 4});   //1
        [8] test1(1, new int[]{2, 3, 4});//2
```

结果分析：

1. [1]test1的实参是唯一的数组new String[]{"a", "b", "c"}，因此直接使用
2. [2]test1的实参有两项，而且这两项都符合varargs的要求，实参数组无法独占形参varargs，编译器看到的是test1(1, ArrayObject)，
因此包装侯结果为Object[]{1, ArrayObject}
**[注意，ArrayObject只是为了在本文中说明这个对像是一个数组，实际并不存在这种类型]**
3. 其他同理


### 问题二：int[] 与 Integer[]

注意问题一里面的[3]和[7]，两者的结果是不一样的，原因：

int[]是没有办法直接转型成Object[]的，基本类型与Object也是无法匹配上的，因此，退而求其次，int[]被当作一个单纯的数组对象ArrayObject，包装结果为Object[]{ArrayObject}，因此数组长度为1。

Integer[]本身就可以看作是Object[]，因此参照包装方式一，可以直接使用这个数组，因此数组长度不变。

## VarArgs在反射中的注意点

首先需要明确的一点是，反射是在运行时才能产生作用的，因此，下面两个方法的效果是一样的：

```java
        public void fn(String[] args) {}

        public void fn(String... args) {}
```

在运行时看来，此方法的签名就是：

```java
    public void fn([java.lang.String args) // public void fn(String[] args)
```

注意，此时方法形参只有一个，就是那个 *String[] args*

一个示例：

```java
    public class Reflect {

        public static void main(String[] args) throws Exception {

            String[] mArgs = new String[]{"a", "b", "c"};

            Method mFn1 = Reflect.class.getMethod("fn1", mArgs.getClass());
            /*[调用1]*/mFn1.invoke(null, new Object[]{mArgs}); // 3
            /*[调用2]*/mFn1.invoke(null, (Object) mArgs);      // 3
            /*[调用3]*/mFn1.invoke(null, mArgs);               // error
        }

        public static void fn1(String... args) {
            System.out.println("fn1:" + args.length);
        }
    }
```

现在看一下Method的invoke方法：

```java
    public Object invoke(Object obj, Object... args)
```

转化为对应的方法调用为：

    fn1(args) //fn1签名 public void fn([java.lang.String args)

1. [调用1]mFn1.invoke(null, new Object[]{mArgs});

        相当与调用fn1(mArgs)，即fn1(new String[]{"a", "b", "c"})

2. [调用2]mFn1.invoke(null, (Object) mArgs);

        mArgs被包装 -> mFn1.invoke(null, new Object[]{mArgs}) 转化为[调用1]

3. [调用3]mFn1.invoke(null, mArgs);

    不包装，直接使用。
    即调用fn1("a", "b", "c")，但是fn1只接受一个参数，即String[] args，所以会报"wrong number of arguments"错误，即参数数量不对

**个人观点，欢迎指正**

