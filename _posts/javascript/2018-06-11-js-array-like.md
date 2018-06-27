---
layout: post
title:  "javascript array like"
date:   2018-06-11 08:00:00 +0800
categories: javascript
tag: [javascript]
---

“array like”（类数组） 这类数据对象见得挺多的，典型的如“NodeList”、argument对象以及字符串，它们的共同点是（非官方定义）：

1. 拥有一个值为自然数的 length 属性 
2. 可以按索引顺序访问
3. prototype 不是 Array

<!-- more -->

#### 将类数组转为数组的方法

1. call

    call 算是典型用法了，唯一的缺陷就是代码不直观。

    ```javascript

        let str_a = "abcdefg";
        let b = [].slice.call(str_a, 0);//["a", "b", "c", "d", "e", "f", "g"]
    ```

2. Array.from()

    ES2015 的新方法，Array 倒是新增了几个便捷方法。

    ```javascript

        let str_a = "abcdefg";
        let c = Array.from(str_a);//["a", "b", "c", "d", "e", "f", "g"]
    ```

3. ...展开

    ES2015 的新特性，用在这种地方也挺别扭的，还是不如用 Array.from() 直观。

    ```javascript

        let str_a = "abcdefg";
        let d = [...str_a];//["a", "b", "c", "d", "e", "f", "g"]
    ```

4. Object.values()

    ES2015 的方法，这个方法有风险，因为获得的是所有 value 的数组，不过对于类数组而言，大部分是没问题的，慎用。

    ```javascript

        let str_a = "abcdefg";
        let c = Object.values(str_a);//["a", "b", "c", "d", "e", "f", "g"]
    ```

#### 一些小应用
转为数组之后，能够使用原生数组的很多方法，这个是转换的主要动机。
几个简单的例子：

1. 翻转字符串

可以不使用 split。

```javascript

Array.from('123').reverse().join('')//"321"

```

#### 类数组

要构建一个类数组也直观：

```javascript
let obj2 = {
    length: 3,
    0:10,
    1:11,
    2:12
};

console.log([...obj2]);//error obj2 is not iterable
console.log(Array.from(obj2));//[10,11,12]
console.log([].slice.call(obj2, 0));//[10,11,12]
Object.values(obj2);// risk！！ [10, 11, 12, 3]

```

上面的 obj2 对象不能使用扩展运算符，因为实现 iterator 接口，才是运用扩展运算符的先决条件。

```javascript
let obj = {
    [Symbol.iterator]: function() {
        var index = 0;
        return {
            next() {
                if (index < 3) {
                    let val = index + 1;
                    index++;
                    return { value: val, done: false };
                } else {
                    return { value: undefined, done: true };
                }
            }
        };
    }
};

console.log([...obj]);//[1,2,3]
console.log(Array.from(obj));//[1,2,3]
console.log([].slice.call(obj, 0));//[1,2,3]
Object.values(obj);//risk []
```

再回头看看，或许把能顺序访问的数据对象都当做类数组来处理，也许更好理解。参考其他语言的概念，要是能够重载 [] 运算符，貌似更容易理解点。遗憾的是， js 并不提供重载操作符的能力。


