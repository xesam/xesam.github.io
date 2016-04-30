---
layout: post
title:  "【Javascript】Prototype源码浅析—Date"
date:   2012-02-02 11:46:04 +0800
categories: Javascript
---

## Date

Date比较好理解，理解清楚了 Number 对象的 toPaddedString 方法就可以了。

只有两个方法（toJSON和toISOString），而且这两个方法还一样，就是将日期转换为 JSON 字符串（遵循 ISO 格式）。

代码很短，我直接贴上来：

```javascript
    (function(proto) {
      function toISOString() {
        return this.getUTCFullYear() + '-' +
          (this.getUTCMonth() + 1).toPaddedString(2) + '-' +
          this.getUTCDate().toPaddedString(2) + 'T' +
          this.getUTCHours().toPaddedString(2) + ':' +
          this.getUTCMinutes().toPaddedString(2) + ':' +
          this.getUTCSeconds().toPaddedString(2) + 'Z';
      }
      function toJSON() {
        return this.toISOString();
      }
      if (!proto.toISOString){
          proto.toISOString = toISOString;
      }
      if (!proto.toJSON){
          proto.toJSON = toJSON;
      }

    })(Date.prototype);
```

补充

ISO8601提供了一种标准的交叉国家方法：一种由全面到具体的表达方法形成了一个日期的表达式，这种方法表示的日期非常容易推导，首先是年，接着是月然后是天，每个部分用连字符“-”分割。加上零，数字均是小于10的，将年份1之前的年用“0”表示，而0年以后的年份就用“-1”表示。
因此，1998年3月30日就可以表示成：1998-03-30。

W3C参考：[http://www.w3.org/QA/Tips/iso-date](http://www.w3.org/QA/Tips/iso-date)

## 小结

到此为止，Prototype关于Javascript的语言核心扩展就算完了，Function,Object,Array,Hash,String,Number,Date,RegExp外加一个辅助对象Enumerable九个部分，这些部分内容（除了setTimeout以及setInterval外）不涉及任何DOM或者BOM的内容。

后面的分析部分开始涉及到DOM处理和BOM部分，但是前面的语言核心是关键，也是Prototype最典型的特点，需注意。
