---
layout: post
title:  "【Javascript】Prototype源码浅析—Enumerable部分(三)"
date:   2012-01-19 11:46:04 +0800
categories: javascript
tag: [javascript]
---
现在来看Enumerable剩下的方法

    toArray | size | inspect
    inject | invoke | sortBy | eachSlice | inGroupsOf | plunk | zip

前面说过map的原理，不管原来的集合是什么，调用map之后返回的结果就是一个数组，其中数组的每一项都是经过interator处理了的，如果不提供interator那么默认使用Prototype.K，此时的作用很明显，返回的结果就是原来集合的数组形式。原来的集合中length属性为多少，返回结果数组的length就是多少。

这个特殊情况被作为一个方法独立出来，叫做toArray:

```javascript
  function toArray() {
    return this.map();
  }
```
另一个size方法是返回上面那个数组的长度：

```javascript
  function size() {
    return this.length;
  }
```
至于inspect，前面在Object和Strng部分见过好几次了，这里调用Array的inspect方法[Array部分后面分析，不过inspect这个方法太熟悉了，也没必要说了]。

```javascript
  function inspect() {
    return '[' + this.map(Object.inspect).join(', ') + ']';
  }
```
另外，对于集合来说，另一个操作是分组。Enumerable中对应的方法是eachSlice 和 inGroupsOf。

先抛开源码，单独来实现这个方法，需要的一个参数是每一个分组的长度（叫做number），如果最后一组长度不够，就保留最后一组的实际长度。

具体实现步骤：

1. 检测number的值，如果number小于1，那么肯定是非法字符，直接返回原来的集合。
2. 将所操作集合转变为数组A，转变方法就是在原来的集合上面调toArray方法。
3. 数组A分组有原生的方法slice，循环调用即可。

按照上面的步骤，可得到下面的实现：

```javascript
    Enumerable.eachSlice = function(number){
        if(number < 1){ //第一步
            return this;
        }
        var array = this.toArray();//第二步
        var index = 0;
        var results = [];
        while(index < array.length){//第三步
            results.push(array.slice(index,index + number));
            index += number;
        }
        return results;
    };
```


对应到具体的源码实现中，index += number;这一步被挪到while的条件中，因此，为了保证循环从0开始，index的初始值被设为-number；另外，和其他的方法一样，eachSlice也提供了iterator, context两个参数，作用依旧不变，所以最后的结果变成：

```javascript
  function eachSlice(number, iterator, context) {
    var index = -number, slices = [], array = this.toArray();
    if (number < 1) return array;
    while ((index += number) < array.length)
      slices.push(array.slice(index, index+number));
    return slices.collect(iterator, context);   //collect就是map
  }
````

例子：

```javascript
console.log([1,2,3,4,5].eachSlice(2));//[[1,2],[3,4],[5,6]]
```

至于inGroupsOf方法，则是对eachSlice的一个补充而已。eachSlice最后一组长度不够，就保留最后一组的实际长度，在inGroupsOf最后一组长度不够，会用指定的填充符填充(默认填充为null)。因此只要提供iterator函数就可以了：

```javascript
    Enumerable.inGroupsOf = function(number, fillWith) {
      fillWith = typeof fillWith == 'undefined' ? null : fillWith;//源码中这里使用的是Object.isUndefined
      return this.eachSlice(number, function(slice) {
        while(slice.length < number){
            slice.push(fillWith);
        }
        return slice;
      });
    }
```

下面看inject，先看手册说明：

```javascript
inject(accumulator, iterator[, context]) -> accumulatedValue
```
根据参数 iterator 中定义的规则来累计值。首次迭代时，参数 accumulator 为初始值，迭代过程中，iterator 将处理过的值存放在 accumulator 中，并作为下次迭代的起始值，迭代完成后，返回处理过的 accumulator。

这个操作其实前面也遇到过，可以单独用each来实现，看一个数组求和的例子：

```javascript
    console.dir([1,2,3,4].inject(0,function(sum,n){
        return sum + n;
    }));//10
```

如果换做each实现，就是：

```javascript
    var sum = 0;
    [1,2,3,4].each(function(value){
        sum += value;
    })
    console.dir(sum);//10
```

对比上面的实现和源码中的实现，上面的实现中有一个缺陷：sum全局变量，这是不合理的。

所以变形上面的形式，抛弃那个全局变量sum，由于each方法是固定死的，没有办法再改变，所以我们在外层再包装一个方法，并将叠加部分填进去：

```javascript
    function fn(accumulator,interator,context){
        [1,2,3,4].each(function(value,index){
            accumulator = interator.call(context,accumulator,value,index);
        })
        return accumulator;
    }
    console.dir(fn(0,function(accumulator,value,index){
        accumulator += value;
        return accumulator;
    }));//10
```

看上面的实现，需要注意的一点是，fn中第一个传入的是一个引用类型的变量，由于这一个实现方式：

```javascript
accumulator = interator.call(context,accumulator,value,index);
```

那么最后返回的结果是同一个变量，是对最初传入变量的一个引用，这一点是出于性能和效率的考虑，不过有时候可能导致问题，需警惕。

接下来是invoke方法，这个方法和each（map）的作用基本一致，唯一的区别是each（map）执行的是外部提供的一个方法，而invoke执行的是集合对象自身本来就存在的方法。因此，invoke的参数有且只需要有一个，就是集合对象的方法名。举个例子，我们将一个数字数组的每一项都转化为字符串：

对比两种实现：

```javascript
    var array_1 = [1,2,3,4].map(function(value){
        return value.toString();
    });
    console.log('array_1:',array_1);//["1", "2", "3", "4"]
    var array_2 = [1,2,3,4].invoke('toString');
    console.log('array_2:',array_2);//["1", "2", "3", "4"]
```

由于少了一次闭包的消耗，因此invoke在效率上稍高，而且形式也简洁不少。

具体实现：

```javascript
  function invoke(method) {
    //var args = $A(arguments).slice(1); //源码实现
    var args  = Array.prototype.slice.call(arguments,1);
    return this.map(function(value) {
      return value[method].apply(value, args);
    });
  }
```

plunk方法比较简单，获取所有元素的同一个属性的值，并返回相应的数组。这个方法显然是针对普通对象来的，数组的话没有什么属性好取的：

```javascript
  function pluck(property) {
    var results = [];
    this.each(function(value) {
      results.push(value[property]);
    });
    return results;
  }
```

源码好理解，给个例子就行：

```javascript
['hello', 'world', 'my', 'is', 'xesam'].pluck('length')// [5, 5, 2, 3, 5]
```

另一个在其他脚本里面常见的方法是zip，这个方法不是很好理解：

```javascript
zip(Sequence...[, iterator = Prototype.K]) -> Array
```
将多个（两个及以上）序列按照顺序配对合并（想像一下拉链拉上的情形）为一个包含一序列元组的数组。 
元组由每个原始序列的具有相同索引的元素组合而成。如果指定了可选的 iterator 参数，则元组由 iterator 指定的函数生成。 

我们先不考虑iterator ，来第一个实现：

```javascript
    function zip(){
        var array_1 = [1,2,3];
        var array_2 = ['a','b','c'];
        var array_3 = ['x','y','z'];
        var result = [array_1].concat([array_2,array_3]);//[[1,2,3],['a','b','c'],['x','y','z']]
        return array_1.map(function(value,index){
            return result.pluck(index);
        })
    }
    console.log(zip());//[[1,'a','x'],[2,'b','y'],[3,'c','z']]
```
改为Enumerable方法的形式就是：

```javascript
    function zip(){
        var result = [this].concat(Array.prototype.slice.call(arguments,1));
        return this.map(function(value,index){
            return result.pluck(index);
        })
    }
    console.log([1,2,3].zip(['a','b','c'],['x','y','z']));////[[1,'a','x'],[2,'b','y'],[3,'c','z']]
```
加上interator处理之后就是：

```javascript
    function zip(){
        var args = Array.prototype.slice.call(arguments,0);
        var interator = function(x){ return x;} //Prototype.K
        if(args[args.length - 1].constructor == Function){
            interator = args.pop();
        }
        var result = [this].concat(Array.prototype.slice.call(arguments,1));
        return this.map(function(value,index){
            return interator.call(result.pluck(index));
        })
    }
```
