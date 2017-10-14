---
layout: post
title:  "【Javascript】Prototype源码浅析—String部分(四)之补充"
date:   2012-01-13 11:36:04 +0800
categories: javascript
tag: [javascript]
---

    interpolate ： 将字符串看作一个模板，并使用 object 的属性填充它。
    sub ： 将字符串中前指定个个与 pattern 指定的模式匹配的子串用 replacement 替换
    scan ： 遍历字符串中与参数 pattern 指定的模式匹配的所有子串。返回原始字符串本身。 
    truncate ： 将字符串截短为指定的长度（包含后缀部分）， 并添加一个后缀。 
    gsub ：将字符串中所有与 pattern 指定的模式匹配的值全部用 replacement 替换掉

上面的方法中，最重要的一个方法是 gsub，具体说明参见《浅析Prototype的模板类--Template》

sub除了可以限定次数外，其他与gsub完全一致。

```javascript
    function sub(pattern, replacement, count) {
        replacement = prepareReplacement(replacement);
        count = Object.isUndefined(count) ? 1 : count;
    
        return this.gsub(pattern, function(match) {
            if (--count < 0) return match[0];
            return replacement(match);
        });
    }
```
scan 也是一样的，不过scan最后返回的是字符串本身而已。

interpolate 是将字符串当做模板来用，核心还是gsub

truncate 是唯一有点区别的（我现在依稀感觉我分错类了）。

以字符串'fuck the gfw'为例，truncate 的执行'fuck the gfw'.truncate(10,'****')的步骤是：

1. 获得前面10 - '****'.length个字符 'fuck t'
2. 拼上后缀'****'，得到 'fuck t****'，长度为10.

处理很简单，源码也简单：

```javascript
    function truncate(length, truncation) {
        length = length || 30;//默认长度30
        truncation = Object.isUndefined(truncation) ? '...' : truncation;//默认后缀...
        return this.length > length ?
            this.slice(0, length - truncation.length) + truncation : String(this);
    }
```

另：Prototype的一个方便之处就是随时可以抽取有用的代码作为单独的部分或者收为自己用。下面是单独提出来的模板方法。

```javascript
    function Template(template, pattern){
        this.template = template;
        this.pattern  = pattern || /(^|.|\r|\n)(#\{(.*?)\})/;
    }
    Template.prototype = (function(){
        function evaluate(obj){
            return gsub.call(this,function(match){
                if(obj == null){
                    return match[0] + '';
                }
                var before = match[1] || '';
                if(before == '\\'){
                    return match[2];
                }
                var ctx = obj;
                var expr = match[3];
                var pattern = /^([^.[]+|\[((?:.*?[^\\])?)\])(\.|\[|$)/;
    
                match = pattern.exec(expr);
                if (match == null){
                    return before;
                }
                while (match != null) {
                    var comp = match[1].search(/^\[/) != -1 ? match[2].replace(/\\\\]/g, ']') : match[1];
                    ctx = ctx[comp];
                    if (null == ctx || '' == match[3]) break;
                    expr = expr.substring('[' == match[3] ? match[1].length : match[0].length);
                    match = pattern.exec(expr);
                }
                return before + (ctx === null ? '' : String(ctx));
            });
        }
        function gsub(replacement){
            var pattern = this.pattern;
            var result  = '';
            var match   = null;
            var source  = this.template;
    
            if (!(pattern.length || pattern.source)) {
                replacement = replacement('');
                return replacement + source.split('').join(replacement) + replacement;
            }
            while (source.length > 0) {
    
                if (match = source.match(pattern)) {
                    result += source.slice(0, match.index);
                    result += replacement(match) === null ? '' : String(replacement(match));
                    source  = source.slice(match.index + match[0].length);
                }else {
                    result += source;
                    source = '';
                }
            }
            return result;
        }
        return {
            constructor : Template,
            evaluate : evaluate
        }
    })();
```

使用：
```javascript
    var template = new Template('my age is : #{name.age}');
    console.log(template.evaluate({name : {age : 24}}));//my age is : 24
```

String部分（完）
