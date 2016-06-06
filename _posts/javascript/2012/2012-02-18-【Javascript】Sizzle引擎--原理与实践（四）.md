---
layout: post
title:  "【Javascript】Sizzle引擎--原理与实践（四）"
date:   2012-02-18 11:46:04 +0800
categories: javascript
tag: [javascript]
---

元素过滤是Sizzle中最复杂的一部分

## 基本形式


```javascript
Sizzle.filter = function( expr, set, inplace, not ) {}
```

    expr    过滤表达式
    set      候选集合
    inplace 是否原地修改
    not      是否取补集

说明：set传递的是一个集合(数组)，如果inplace为true，set会被修改；not的作用是用来取补集。还是用个例子来说明下：

```html
<li id="a1" class="test"></li>
<li id="a2" class="test"></li>
<li id="a3" ></li>
```
原始集合

    set = [#a1,#a2,#a3]

(1)

    filter('.test',set,true,false)
    -->   result = [#a1,#a2]
    -->   set    = [#a1,#a2]

(2)

    filter('.test',set,false,false)
    -->   result = [#a1,#a2]
    -->   set    = [#a1,#a2,#a3]

(3)

    filter('.test',set,true,true)
    -->   result = [#a3]
    -->   set    = [#a1,#a2]

(4)

    filter('.test',set,false,true)
    -->   result = [#a3]
    -->   set    = [#a1,#a2,#a3]


## 基本流程

在前面的find中，我们获得了一个类似

```javascript
{
    expr : expr,
    set  : set
}
```

的结果。其中，expr是过滤表达式，set是候选集合

简要说一下Sizzle.filter的过程：

第一步：过程和find差不多，提取expr中的过滤类型，相比find的类型，filter的类型有7种，分别是：

    ID选择器，CLASS选择器，TAG选择器，ATTR属性选择器，CHILD子元素选择器，PSEUDO伪类选择器，POS位置选择器

```javascript
['ID','TAG','ATTR','CHILD','POS','PSEUDO']
```

由于filter的情况太过复杂，所以，在执行最终的过滤之前，都会先执行一步预过滤，来统一调用。对应到源码中就是Expr.preFilter和Expr.filter

第二步：预过滤

第三步：最终过滤，true表示结果符合条件，false表示不符合

第四步：去除expr中已经匹配的部分，重复上面的操作，知道expr全部完毕或者set为空

因此，Sizzle.filter的大致代码流程是：

```javascript
Sizzle.filter = function( expr, set, inplace, not ) {
    while ( expr && set.length ) {
        for ( type in Expr.filter ) {
            if ( (match = Expr.leftMatch[ type ].exec( expr )) != null && match[2] ) { //第一步
                match = Expr.preFilter[ type ]( ? ); //第二步
                if ( match ) {
                    found = filter( ? );//第三步
                }
            }
            if ( found !== undefined ) {//第四步
                expr = expr.replace( Expr.match[ type ], "" );
                break;
            }
        }
    }
    return curLoop;
}
```

实例说明

沿用find部分的例子：

```html 
<input type="radio" id="a" name="gender" value="man" class="default" /><label for="a" >男</label>
<input type="radio" id="b" name="gender" value="man" class="default" /><label for="b">女</label>
<input type="checkbox" id="c" name="gender" value="man" /><label for="c">人妖</label>
```
在第一步的find中，我们获得的返回值是

```javascript
{
    expr : '[class*="default"]',
    set  : Array.prototype.slice.call(document.getElementsByTagName('input'))
}
```
filter的情况很多，因此单独抠出例子中用到的部分：

```javascript
var Expr = {
        match : {
            ATTR : /(^(?:.|\r|\n)*?)\[\s*((?:[\w\u00c0-\uFFFF\-]|\\.)+)\s*(?:(\S?=)\s*(?:(['"])(.*?)\4|(#?(?:[\w\u00c0-\uFFFF\-]|\\.)*)|)|)\s*\](?![^\[]*\])(?![^\(]*\))/
        },
        attrMap: {  //见讨论部分
            "class": "className",
            "for": "htmlFor"
        },
        attrHandle: {//见讨论部分
            href: function( elem ) {
                return elem.getAttribute( "href" );
            },
            type: function( elem ) {
                return elem.getAttribute( "type" );
            }
        },
        preFilter : {//预过滤
            ATTR : function(match){
                //var name = match[1] = match[1].replace( rBackslash, "" );这里被我屏蔽了，暂不考虑有\的情况
                var name = match[1];
                if (Expr.attrMap[name] ) {
                    match[1] = Expr.attrMap[name];
                }
                //match[4] = ( match[4] || match[5] || "" ).replace( rBackslash, "" );这里被我屏蔽了，暂不考虑有\的情况
                if ( match[2] === "~=" ) {
                    match[4] = " " + match[4] + " ";
                }
                return match;
            }
        },
        filter : {//过滤
            ATTR : function(elem , match){
                var name = match[1],     //选择表达式的属性名
                    result = Expr.attrHandle[ name ] ? Expr.attrHandle[ name ] :
                                    elem[ name ] != null ? elem[ name ] : elem.getAttribute( name );
                var value = result + "", //元素的实际值
                    type = match[2],     //选择表达式的符号类型
                    check = match[4];    //选择表达式的目标值
                
                return  result == null ? type === "!=" :
                        !type && Sizzle.attr ? result != null :
                        type === "=" ?value === check :
                        type === "*=" ?value.indexOf(check) >= 0 :
                        type === "~=" ?(" " + value + " ").indexOf(check) >= 0 :
                        !check ? value && result !== false :   //待检测的属性值为空
                        type === "!=" ? value !== check :
                        type === "^=" ?value.indexOf(check) === 0 :
                        type === "$=" ?value.substr(value.length - check.length) === check : //indexOf(value.length - check.length) >= 0
                        type === "|=" ?value === check || value.substr(0, check.length + 1) === check + "-" :
                        false;
            }
        }
    };
    var expr = '[class*="default"]';
    var curLoop =Array.prototype.slice.call(document.getElementsByTagName('input'));

    function filter(expr, set){
        var match,item,i,found,left;
        var curLoop = set,result=[];
        while(expr && set.length){
            if((match = Expr.match.ATTR.exec(expr)) != null){
                left = match[1];
                match.splice(1,1);
                //预过滤，主要是处理形式和兼容性的问题
                match = Expr.preFilter[ 'ATTR' ]( match);   //注意这里与jquery的区别，多余的参数都去掉了

                if(match){
                    for ( i = 0; (item = curLoop[i]) != null; i++ ) {
                        if ( item ) {
                            found = Expr.filter['ATTR']( item, match, i, curLoop );//true代表满足条件
                            if(found){
                                result.push(item);
                            }
                        }
                    }
                    if ( found !== undefined ) {
                        expr = expr.replace( Expr.match[ 'ATTR' ], "" );
                    }
                }
            }
        }
        return curLoop;
    }
    var s = filter(expr, curLoop);
    console.log(s);  //[#a,#b]
```
对照上面的代码：

第一步、Expr.match.ATTR被匹配

第二步、预过滤，在这一步中，需要处理的问题是属性选择器的“属性值”，“属性操作符”，“属性值”的逻辑与兼容性问题，ATTR中return的结果可能不好理解，一行一行的看比较好。

第三步、通过Expr.filter.ATTR依次检测set中每一项，符合过滤条件的就保存，不符合的就丢弃。

第四步、选择表达式修剪，开始下一轮。


具体到源码中的实现，流程是一样的，只是多了两个参数，注意一下not就行，并没有显示的传递not为true或者false，而是经过了运算或者隐式转换：

    undefined --> false
    
    true^undefined -->1(true)
    
^异或操作符平时用的不多，这里可以复习下，源码中的逻辑就是：

```javascript
    if(not==true){
        pass = !found
    }else{
        pass = found
    }
```

因此设置not=true可以获得与默认情况下的原始集合互补的集合,就像文章开头一样。

## 讨论

### 1、a标签的 href 属性

关于这个的讨论网上有不少，可以参考：

1. [http://www.planabc.net/2008/11/06/ie-href-bug/](http://www.planabc.net/2008/11/06/ie-href-bug/)
2. [http://www.quirksmode.org/bugreports/archives/2005/02/getAttributeHREF_is_always_absolute.html](http://www.quirksmode.org/bugreports/archives/2005/02/getAttributeHREF_is_always_absolute.html)
3. [http://www.glennjones.net/2006/02/getattribute-href-bug/](http://www.glennjones.net/2006/02/getattribute-href-bug/)

源码中对于这个的处理是单独定义了Expr的一个属性：

```javascript
    attrHandle: {
        href: function( elem ) {
            return elem.getAttribute( "href" );
        },
        type: function( elem ) {
            return elem.getAttribute( "type" );
        }
    },
```

然后在源码的1130行，

```javascript
    div.innerHTML = "<a href='#'></a>";

    if ( div.firstChild && typeof div.firstChild.getAttribute !== "undefined" &&
            div.firstChild.getAttribute("href") !== "#" ) {
        Expr.attrHandle.href = function( elem ) {
            return elem.getAttribute( "href", 2 );
        };
    }
```

### 2、关于新增的type

上面的type在以前的源码中是没有的，这个是新加的，原因就是HTML5新增了许多type类型，但是老式浏览器直接获取elem.type并不能获取新的类型，所以采用getAttribute方法。

### 3、两个特殊属性class和for。

这两个应该都清楚，class是保留字，for是，都不能用属性操作符来获取属性，所以单独拎出来处理。


整个Sizzle.filter也是一个分发器的作用，相比find的三种情况，filter的情况就复杂多了，后面再一个个的分析实现，以及这么做的思想。
