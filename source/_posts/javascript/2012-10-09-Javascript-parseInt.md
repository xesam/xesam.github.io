---
layout: post
title:  "【Javascript】有关parseInt的讨论"
date:   2012-10-09 13:46:04 +0800
categories: javascript
tag: [javascript]
---

问题由来，某群的一个讨论：

```javascript
parseInt(1/0, 19) = 18;
```

parseInt的用法：

```javascript
parseInt(string [, radix])
```
注意，第一个参数是String类型，当radix未指定的时候，那么默认基地是10。

转换规则：

1. 首先查看位置 0 处的字符，判断它是否是个有效数字；如果不是，该方法将返回 NaN，不再继续执行其他操作。
2. 位置 0 处的字符有效，该方法将查看位置 1 处的字符，依次向后进行同样的测试，直到发现非有效数字的字符或者到达字符串末尾为止，
3. 返回转换成功的数字

因此有比较熟悉的例子：

```javascript
parseInt('F') => 'NaN'
parseInt('F', 16) => 15
```

下面将Infinity作为第一参数，结果就是下面这样：

```javascript
parseInt(Infinity) => 'NaN'
parseInt(Infinity, 16) => 'NaN'
```

先将Infinity转换为String类型（Infinity.toString() => 'Infinity'），因为不论是十进制还是十六进制，第一个字符串都会失败，所以直接返回'NaN'。

但是'I'在19 ~ 36进制情况下，是可以转换为数字的，而且表示的数字就是18，所以：

```javascript
parseInt('I', 19) => 18
parseInt('I', 20) => 18
...
parseInt('I', 36) => 18
```

由于

```javascript
1/0 => Infinity;
```

所以

```javascript
parseInt(1/0, 19) => 18;
```

由于基数radix的范围介于2 ~ 36之间，所以0 ~ 9, a ~ z, A ~ Z在36进制下都可以转换成功，转换测试如下：

```javascript
    var arr = [], A_code = 65, Z_code = 65 + 25;
    for(var i = 0; i <= 9; ++i){
        arr.push(i);
    }
    for(var i = A_code; i <= Z_code; ++i){
        arr.push(String.fromCharCode(i));
    }
    //arr = [0, 1, 2, ... 9, 'A', 'B', ... 'Z']
    arr.forEach(function(item){
       // console.log(item, ':', parseInt(item, 36));
    })
    //output : 0:0, 1:1, 2:2, ... Z:35;
```

回到Infinity的例子：

第一个字符'I'在19 ~ 36基数的情况下都可以转换成功

第二个字符'N'在36进制中表示为23， 所以'N'在24 ~ 36基数的情况下都可以转换成功，

后面的字符类推
测试：

```javascript
    function ret_output(arr){
        var str_output = [];
        arr.reverse().forEach(function(el, index){
            str_output.push(el + ' * ' + i + '**' + index); //'**' 表示阶乘
//            str_output.push(el + ' * ' + 'Math.pow(' + i + ',' + index + ')');
        });
        console.log( i + '进制：',str_output.join(' + '), '=', parseInt(Infinity, i));
        throw new Error('trans abort');
    }
    for(var i = 19; i <= 36; ++i){
        var arr = [];
        try{
            Infinity.toString().split('').forEach(function(item, s_index){
                var r = parseInt(item, i);
                if(isNaN(r)){
                    ret_output(arr);
                }
               arr.push(r);
　　　　　　　　　if(s_index == Infinity.toString().length - 1){
                    ret_output(arr);
                }
                
            })
        }catch(e){
        }
    }
```

结果：

    19进制： 18 * 19**0 = 18 
    20进制： 18 * 20**0 = 18 
    21进制： 18 * 21**0 = 18 
    22进制： 18 * 22**0 = 18 
    23进制： 18 * 23**0 = 18 
    24进制： 18 * 24**5 + 23 * 24**4 + 15 * 24**3 + 18 * 24**2 + 23 * 24**1 + 18 * 24**0 = 151176378 
    25进制： 18 * 25**5 + 23 * 25**4 + 15 * 25**3 + 18 * 25**2 + 23 * 25**1 + 18 * 25**0 = 185011843 
    26进制： 18 * 26**5 + 23 * 26**4 + 15 * 26**3 + 18 * 26**2 + 23 * 26**1 + 18 * 26**0 = 224651640 
    27进制： 18 * 27**5 + 23 * 27**4 + 15 * 27**3 + 18 * 27**2 + 23 * 27**1 + 18 * 27**0 = 270812475 
    28进制： 18 * 28**5 + 23 * 28**4 + 15 * 28**3 + 18 * 28**2 + 23 * 28**1 + 18 * 28**0 = 324267766 
    29进制： 18 * 29**5 + 23 * 29**4 + 15 * 29**3 + 18 * 29**2 + 23 * 29**1 + 18 * 29**0 = 385849803 
    30进制： 18 * 30**6 + 23 * 30**5 + 15 * 30**4 + 18 * 30**3 + 23 * 30**2 + 18 * 30**1 + 29 * 30**0 = 13693557269 
    31进制： 18 * 31**6 + 23 * 31**5 + 15 * 31**4 + 18 * 31**3 + 23 * 31**2 + 18 * 31**1 + 29 * 31**0 = 16647948474 
    32进制： 18 * 32**6 + 23 * 32**5 + 15 * 32**4 + 18 * 32**3 + 23 * 32**2 + 18 * 32**1 + 29 * 32**0 = 20115447389 
    33进制： 18 * 33**6 + 23 * 33**5 + 15 * 33**4 + 18 * 33**3 + 23 * 33**2 + 18 * 33**1 + 29 * 33**0 = 24164998832 
    34进制： 18 * 34**6 + 23 * 34**5 + 15 * 34**4 + 18 * 34**3 + 23 * 34**2 + 18 * 34**1 + 29 * 34**0 = 28872273981 
    35进制： 18 * 35**7 + 23 * 35**6 + 15 * 35**5 + 18 * 35**4 + 23 * 35**3 + 18 * 35**2 + 29 * 35**1 + 34 * 35**0 = 1201203301724 
    36进制： 18 * 36**7 + 23 * 36**6 + 15 * 36**5 + 18 * 36**4 + 23 * 36**3 + 18 * 36**2 + 29 * 36**1 + 34 * 36**0 = 1461559270678