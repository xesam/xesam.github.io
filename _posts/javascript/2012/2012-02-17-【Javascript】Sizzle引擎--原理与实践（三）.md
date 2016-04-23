---
layout: post
title:  "【Javascript】Sizzle引擎--原理与实践（三）"
date:   2012-02-17 11:46:04 +0800
categories: Javascript
---

查找的入口对应的是Sizzle.find方法:

```javascript
Sizzle.find = function( expr, context) {}
```
    expr      ：查找的表达式
    context ：查找的范围

### find的步骤

1. 判断主要集合，方法说过了，依次匹配，顺序就是ID --> NAME --> TAG
2. （1）当有类型被匹配时，调用相应的方法，获取集合set。（2）当ID,NAME,TAG全部不匹配时，获取context范围内的全部元素集合set
3. 去除expr中已经匹配的部分，返回结果{expr : expr,set : set}

因此，Sizzle.find的大致代码流程是

```javascript
Sizzle.find = function( expr, context, isXML ) {
    for ( i = 0, len = Expr.order.length; i < len; i++ ) {
        var type = Expr.order[i];
        if((match = Expr.leftMatch[ type ].exec( expr ))){             //    对应第一步
            if((set = Expr.find[ type ]( match, context ))!=null){   //对应第二步（1）
                expr = expr.replace( Expr.match[ 'ID' ], "" );       //对应第三步
                break;
            }
        }
    }
    if(!set){//对应第二步（2）
        set = context.getElementsByTagName( "*" );
    }
    return {expr : expr,set  : set}
}
```
实例说明：

```html
<input type="radio" id="a" name="gender" value="man" class="default" /><label for="a" >男</label>
<input type="radio" id="b" name="gender" value="man" class="default" /><label for="b">女</label>
<input type="checkbox" id="c" name="gender" value="man" /><label for="c">人妖</label>
```

```javascript
var set;
var expr = 'input[class*="default"]';

var match = Expr.leftMatch[ 'ID' ].exec( expr )
var left = match[1];
match.splice( 1, 1 );

set = Expr.find[ 'ID' ]( match, document);
if ( set != null ) {
    expr = expr.replace( Expr.match[ 'ID' ], "" );
}
if ( !set ) {
    set = typeof document.getElementsByTagName !== "undefined" ?document.getElementsByTagName( "*" ) :[];
}
Expr.find['ID'] = function( match, context ) {
    if ( typeof context.getElementById !== "undefined") {
        var m = context.getElementById(match[1]);
        return m && m.parentNode ? [m] : [];
    }
}
console.log({ set: set, expr: expr });
```
因此从上面的实例来看，Sizzle.find并不是执行查找功能的部分，而是主要起了一个分发器的作用:

将不同的选择表达式分发到不同的更专一的查找器上面。上面的例子中就是将具体查找分发给 Expr.find[ 'ID' ]

具体代码分析：

```javascript
Sizzle.find = function( expr, context, isXML ) {
    var set, i, len, match, type, left;

    if ( !expr ) {  //如果没有选择表达式，直接返回空集合
        return [];
    }

    for ( i = 0, len = Expr.order.length; i < len; i++ ) {//用来判断应该选用哪个查找器，对应的顺序是[ "ID", "NAME", "TAG" ];
        type = Expr.order[i];

        if ( (match = Expr.leftMatch[ type ].exec( expr )) ) { //碰到符合条件的匹配
            left = match[1];
            match.splice( 1, 1 ); //因为leftMatch在match的头部添加了一个新的分组，所以现在提取第一个分组到left里面，然后删除这个分组

            if ( left.substr( left.length - 1 ) !== "\\" ) { //参见讨论部分
                match[1] = (match[1] || "").replace( rBackslash, "" ); //检测，替换回车而已
                set = Expr.find[ type ]( match, context, isXML ); //转到相应的查找器执行查找程序

                if ( set != null ) { //找到相应的结果，修剪expr
                    expr = expr.replace( Expr.match[ type ], "" );
                    break;
                }
            }
        }
    }

    if ( !set ) {    //[ "ID", "NAME", "TAG" ]中没有匹配的类型时候，直接返回context范围内的所有标签。
        set = typeof context.getElementsByTagName !== "undefined" ? context.getElementsByTagName( "*" ) :[];
    }

    return { set: set, expr: expr };
};

Expr.order = [ "ID", "NAME", "TAG" ];
Expr.find  = {
    ID: function( match, context, isXML ) {
        if ( typeof context.getElementById !== "undefined" && !isXML ) {
            var m = context.getElementById(match[1]);
            return m && m.parentNode ? [m] : []; //这里注意优先级的问题。&&的优先级高于?:的优先级
        }
    },

    NAME: function( match, context ) {
        if ( typeof context.getElementsByName !== "undefined" ) {
            var ret = [],
                results = context.getElementsByName( match[1] );

            for ( var i = 0, l = results.length; i < l; i++ ) {
                if ( results[i].getAttribute("name") === match[1] ) {
                    ret.push( results[i] );
                }
            }
            return ret.length === 0 ? null : ret;
        }
    },

    TAG: function( match, context ) {
        if ( typeof context.getElementsByTagName !== "undefined" ) {
            return context.getElementsByTagName( match[1] );
        }
    }
};
```

## 讨论

### 关于检测'\'的讨论【这个不知道对不对】

实例表达式expr = '\.className',CLASS匹配结果['\.className','.className'], 此时原本的意图是'.'被转义，因此不应该作为class匹配，中止。


### 关于getElementById方法bug的讨论（源码1056行）,

在某些浏览器里面，getElementById('test')会返回name值为test的a节点，因此会对查询结果产生干扰。比如：

<a name="test"></a><div id="test"></div>此时a节点在div前面，getElementById('test')回返回<a name="test"></a>而非预期中的<div id="test"></div>。

Sizzle也对此做了检测：

```javascript
(function(){
    // 先创建一个测试环境<div><a name="script20120215"></a></div>
    var form = document.createElement("div"),
        id = "script" + (new Date()).getTime(),
        root = document.documentElement;

    form.innerHTML = "<a name='" + id + "'/>";
    root.insertBefore( form, root.firstChild );

    //检测getElementById的返回值，现获取了相应的节点之后，添加一步检测id属性，如果吻合就保存，不吻合就丢弃
    if ( document.getElementById( id ) ) {
        Expr.find.ID = function( match, context, isXML ) {
            if ( typeof context.getElementById !== "undefined" && !isXML ) {
                var m = context.getElementById(match[1]);

                return m ?
                    m.id === match[1] || typeof m.getAttributeNode !== "undefined" && m.getAttributeNode("id").nodeValue === match[1] ?
                        [m] :
                        undefined :
                    [];
            }
        };
        Expr.filter.ID = function( elem, match ) {
            var node = typeof elem.getAttributeNode !== "undefined" && elem.getAttributeNode("id");

            return elem.nodeType === 1 && node && node.nodeValue === match;
        };
    }

    root.removeChild( form );

    // 对于IE，需要释放刚才添加的DIV过程中各变量的缓存，便于垃圾回收
    root = form = null;
})();
```

接下来是Sizzle.filter流程分析：《Sizzle引擎--原理与实践（四）》

