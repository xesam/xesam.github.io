---
layout: post
title:  "【Javascript】关于Chrome的sort()优化"
date:   2012-02-01 11:46:04 +0800
categories: Javascript
---

今天看Sizzle代码的时候，里面有这么一段：

```javascript
// Here we check if the JavaScript engine is using some sort of
// optimization where it does not always call our comparision
// function. If that is the case, discard the hasDuplicate value.
//   Thus far that includes Google Chrome.
[0, 0].sort(function() {
    baseHasDuplicate = false;
    return 0;
});
```
然后google一番，发现这篇文章：[《Chrome V8 引擎对 sort 的优化》](http://www.udpwork.com/item/629.html)，简单的拷贝过来：

```javascript
var a = 0, b = 0;
[0, 0].sort(function() {
    a = 1;
    return 0;
});
[0, 1].sort(function() {
    b = 1;
    return 0;
});

alert(a === b); // true or false ?
```
上面的代码，除了 Chrome 输出 false, 其它浏览器皆为 true.

原因是 Chrome 对数组的 sort 方法进行了优化：

```javascript
function sort(comparefn) {
  var custom_compare = (typeof(comparefn) === 'function');
  function Compare(x,y) {
    if (x === y) return 0;
    if (custom_compare) {
      return comparefn.call(null, x, y);
    }
    ...
}
```

不过测试了一下，发现这个并不成立，在Chrome 16.0.912.77 m中，并没有执行什么优化，alert出来的同样是true，与FF等浏览器无异。

因此，这个应该不是存在所有的Chrome版本中，因此并不能作为定论。

测试结果没有覆盖所有Chrome版本，错误之处请指出。
