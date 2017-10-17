---
layout: post
title:  最大公因数与最小公倍数
date:   2016-03-23 13:46:04 +0800
categories:
  - math
tag: 
  - math
---
#### 1.求正整数 a, b 的最大公因数
a,b 是两个正整数，其中 a > b，则 a 可以写成如下形式：

```html
  a = kb + r
```

其中 0 <= r < b

1. 如果 r 等于 0，则 a = kb，那么最大公因数即为 b
2. 如果 r 不等于 0，设 a, b 的一个因数为正整数 q，则有：

```html
  a = tq
  b = sq
```

其中 t s 为正整数，得到

```html
  => tq = ksq + r
  => r = (t - ks)q
```

因此 q 也是 r 的一个因数，所以，a，b 的公因数同时也是 b，r 的公因数。
同理可证 b，r 的公因数同时也是 a，b 的公因数，因此：

```html
  a，b 与 b，r 的公因数相同
```

如果用 gcd(a, b) 表示 a，b 的最大公因素，则 

```html
  gcd(a, b) == gcd(b, r)
```

程序实现：

```javascript
  function gcd(a, b) {
      if(a < b){
          var tmp = a;
          a = b;
          b = tmp;
      }
      var mod = a % b;
      if(mod === 0){
          return b;
      }else{
          return gcd(b, mod);
      }
  }
```

## 2.求正整数 a, b 的最小公倍数

a,b 是两个正整数，其中 a > b，则：

```html
  a = kb + r
```

其中 0 <= r < b

1. 如果 r 等于 0，则 a = kb，那么最小公倍数即为 a
2. 如果 r 不等于 0，设 a, b 的最小公倍数为正整数 q，则有：

```html
  q = sa
  q = tb
```
其中 t s 为正整数。

已知 a，b 的最大公因数为 g，则

```html
  q = sa = sug
  q = tb = tvg

  => sa = sug = tb = tvg
  => su = tv
  => s/t = v/u
```
其中 u v 为正整数，且 u v 互质（因为如果 u v 不互质，那么 g 就不是 a，b 的最大公因数）。

同理可知：s t 也一定互质，因为假设 s t 不互质，且有公因数 z，那么存在如下关系：

```html
  s = mz
  t = nz

  => q = sa = mza
     q = tb = nzb
```

因此，存在一个正整数 w = ma = nb，w也是 a b 的公倍数，显然 w < q，与 “q 是最小公倍数”相矛盾。
此时可以得出：

```html
  s/t = v/u
```
其中 u v 互质，s t 互质。可知：

```html
  s = vt/u
```
因此 t 必定可以整数 u，假设 t = xu，其中 x!=1，可以得到 s = xv。与 “s t 互质”相矛盾。因此 x 必定是 1，所以

```html
  s = v
  t = u
```
得到

```html
  q = sa = va = ab/q
```
程序实现：

```javascript
  function lcm(a, b){
      var _gcd = gcd(a, b);
      return a * b / _gcd;
  }
```



