---
layout: post
title:  "【Javascript】改造alert的引发的争论"
date:   2012-01-13 11:46:04 +0800
categories: javascript
tag: [javascript]
---
今天在群里讨论alert的问题，说到了alert的改造，虽然说改造原生方法不是好做法，但是既然提到了就可以讨论下，所以我按照他们的讨论给出了下面的一段代码：

```javascript
    var _alert = window.alert;
    window.alert = function(param,isDebug){
        if(isDebug){
            console.log(param);
        }else{
            _alert(param);
        }
    }
    alert('x');
    alert('x',true);
    alert('x');
    alert('x',true);
```
于是开始反驳我，大致的论点集中在下面的一段上面：

```javascript
    _alert = window.alert;
    window.alert = function(){}
```
反方论点：这么写之后，_alert与window.alert应该还是一致的，因为大家都知道函数名称保存的只是引用而已。

当时被弄糊涂了，难道价值观被颠覆了？后来仔细想了一会儿，发现貌似被忽悠了。函数变量名保存的是引用没错，可是这个例子和引用的关系不是这么讲的吧···

要说明函数的引用关系，应该是这个例子：

```javascript
    var a = [1,2,3];
    var b = a;
    a.push(4);
    console.log(a,b);//[1,2,3,4],[1,2,3,4]
```

后来回想一下，问题的最终原因还是值类型和引用类型被忽悠了，于是分析一下。先看下面的例子：

```javascript
    var a = 1;
    var b = a;
    console.log(a,b);
```
在这个例子中a，b完全只是一个名字而已，没有其他的作用。不论要不要，那个1都是真实存在的（假如可以无端产生一个变量1，那么1在被回收之前，无论有没有名字，都是存在的），此时的情况是：

![1](/image/javascript_alert_1.png)

继续上面的例子：

```javascript
    var a = 1;
    var b = a;
    a = 2;
    console.log(a,b);
```

![1](/image/javascript_alert_2.png)

上面是Number类型的情况，下面换做一个引用类型的，比如Array。

```javascript
    var a = [1,2,3];
    var b = a;
    console.log(a,b);
```

![1](/image/javascript_alert_3.png)
继续：

```javascript
    var a = [1,2,3];
    var b = a;
    a.push(4);
    console.log(a,b);
```

![1](/image/javascript_alert_4.png)

这就是引用传递，在整个过程中，变量名本身还是a，b没有变化，但是他们引用的东西发生了变化。

此时a与b之间没有半毛钱的关系，他们是通过[1,2,3,4]存在一丝形式上的相同性，而不是b与[1,2,3,4]通过a有联系，这一点才是引用传递要注意的。此时a===b为true。

下面换一个操作：

```javascript
    var a = [1,2,3];
    var b = a;
    a = [1,2,3];
    console.log(a,b);
```
此时，虽然a，b各自保存的还是引用类型数据，但是a与b本来就半毛钱的关系都没有，所以此时a换个内容，与b的关系就完全没有了，连通过最初[1,2,3]获得的相同性都没有了，此时a===b为false。对应下面的图：


![1](/image/javascript_alert_5.png)

继续操作a：

```javascript
    var a = [1,2,3];
    var b = a;
    a = [1,2,3];
    a.push(4);
    console.log(a,b);
```

![1](/image/javascript_alert_6.png)

所以，“引用”引用的内存中的值，而非那个变量名。

回到开头的例子中：

```javascript
    var _alert = window.alert;
    window.alert = function(param,isDebug){
        if(isDebug){
            console.log(param);
        }else{
            _alert(param);
        }
    }
```
在执行var _alert = window.alert;的时候，三者的关系是：

![1](/image/javascript_alert_7.png)

执行：

```javascript
    window.alert = function(param,isDebug){
       //
    }
```

![1](/image/javascript_alert_8.png)

所以最初讨论的时候，一开始就错了，因为_alert引用的不是window.alert，而是window.alert所引用的那个函数，不论是_alert还是window.alert，都只是一个名字而已，两者没有半毛钱的关系，最终的枢纽还是真实存在的内存中的那个变量。

然后另外一个问题就是关于才浏览器控制台测试代码的问题。

我们讨论的时候，先运行了一段测试代码：

```javascript
    var _alert = window.alert;
    window.alert = function(){};
    console.log(_alert === window.alert);
```
然后我们又在相同的控制台里面运行了我在开头给出的那一段代码，所以在同一个窗口里面，控制台的环境并没有刷新，测试代码的效果还在，所以alert已经混乱了。

要完全测试的话，最好还是每次都新开一个窗口测试。

错误之处请大牛指教~
