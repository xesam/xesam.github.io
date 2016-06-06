---
layout: post
title:  "【Javascript】从URL中提取参数与将对象转换为URL查询参数"
date:   2012-01-12 10:36:04 +0800
categories: javascript
tag: [javascript]
---
这两种主要是对《Prototype浅析》先前略过的String部分中toQueryParams和Object部分的toQueryString方法的补充

## 一、从URL中提取参数

有下列字符串：

```javascript
var linkURL = 'http://localhost:8080/String/string_6.html?昵称=小西山子&age=24#id1';
```
对于一个真实的URL地址，可以用js来读取location中的相关信息来获得某些信息，下面列举一些：

```javascript
location.origin : http://localhost【域】
location.pathname : /project_js/Javascript/js_basic/demo/String/string_6.html【URL路径】
location.host : localhost【主机+端口】
location.hostname : localhost【主机名】
location.port :【端口】
location.search : ?name=xesam【查询字符串】
location.hash : #age【锚点】
location.href : http://localhost/project_js/Javascript/js_basic/demo/String/string_6.html?name=xesam#age【完整形式】
location.protocol : http【协议】
```
其中，与从URL中提取参数主要是用到location.search。不过为了通用，我们不去读取location.search，直接处理字符串。

提取字符串查询字符串之后，转化为对象的形式。

先讨论几种查询字符串的情况：

1. ?昵称=小西山子&age=24#id1  -->{昵称:'小西山子',age:'24'}
2. ?昵称&age=24#id1';  -->{昵称:undefined,age:'24'}
3. ?=小西山子&age=24#id1  -->{age:'24'}
4. ?昵称=小西山子=又一个&age=24&age=24#id1   -->{昵称:'小西山子=又一个',age:['24','24']}

```javascript
    function toQueryParams(){
        var search = this.replace(/^\s+/,'').replace(/\s+$/,'').match(/([^?#]*)(#.*)?$/);//提取location.search中'?'后面的部分
        if(!search){
            return {};
        }
        var searchStr  = search[1];
        var searchHash = searchStr.split('&');

        var ret = {};
        for(var i = 0, len = searchHash.length; i < len; i++){ //这里可以调用each方法
            var pair = searchHash[i];
            if((pair = pair.split('='))[0]){
                var key   = decodeURIComponent(pair.shift());
                var value = pair.length > 1 ? pair.join('=') : pair[0];
                
                if(value != undefined){
                    value = decodeURIComponent(value);
                }
                if(key in ret){
                    if(ret[key].constructor != Array){
                        ret[key] = [ret[key]];
                    }
                    ret[key].push(value);
                }else{
                    ret[key] = value;
                }
            }
        }
        return ret;
    }
    console.dir(toQueryParams.call(linkURL));
````

上面基本就是Prototype中toQueryParams的实现，上面有一个步骤是用'='分割参数，然后在value中再拼接。另外可以用substring来实现：

```javascript
    function toQueryParams(){
        var search = this.replace(/^\s+/,'').replace(/\s+$/,'').match(/([^?#]*)(#.*)?$/);
        if(!search){
            return {};
        }
        var searchStr  = search[1];
        var searchHash = searchStr.split('&');

        var ret = {};
        searchHash.forEach(function(pair){
            var temp = '';
            if(temp = (pair.split('=',1))[0]){
                var key   = decodeURIComponent(temp);
                var value = pair.substring(key.length + 1);
                if(value != undefined){
                    value = decodeURIComponent(value);
                }
                if(key in ret){
                    if(ret[key].constructor != Array){
                        ret[key] = [ret[key]];
                    }
                    ret[key].push(value);
                }else{
                    ret[key] = value;
                }
            }
        });
        return ret;
    }
    console.dir(toQueryParams.call(linkURL));
```

## 二、对象转换为URL查询参数

对象转换为URL查询参数就麻烦一点。不过由于是转换成查询参数形式，因此只能处理单层嵌套的对象，子对象就不能处理了。其原理就是toQueryParams的反向操作。

```javascript
    function toQueryPair(key, value) {
        if (typeof value == 'undefined'){
            return key;
        }
        return key + '=' + encodeURIComponent(value === null ? '' : String(value));
    }
    function toQueryString(obj) {
        var ret = [];
        for(var key in obj){
            key = encodeURIComponent(key);
            var values = obj[key];
            if(values && values.constructor == Array){//数组
                var queryValues = [];
                for (var i = 0, len = values.length, value; i < len; i++) {
                    value = values[i];
                    queryValues.push(toQueryPair(key, value));
                }
                ret = ret.concat(queryValues);
            }else{ //字符串
                ret.push(toQueryPair(key, values));
            }
        }
        return ret.join('&');
    }
    console.log(toQueryString({
        name : 'xesam',
        age : 24
    })); //name=xesam&age=24
    console.log(toQueryString({
        name : 'xesam',
        age : [24,25,26]
    })); //name=xesam&age=24&age=25&age=26
```

真实源码中用的是inject方法，不过在Enumerable部分，因此上面作了替换。
