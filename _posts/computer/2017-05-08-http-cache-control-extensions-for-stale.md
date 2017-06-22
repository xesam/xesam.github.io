---
layout: post
title:  "【http】Cache-Control扩展"
date:   2017-05-08 08:00:00 +0800
categories: computer
tag: [computer]
---
rfc5861 定义了两个 Cache-Control 的扩展：

1. stale-while-revalidate
2. stale-if-error

这是两个扩展都是用来定义缓存过期（stale）后的处理策略，旨在提高用户体验，不过两者是独立使用，并无关联的。

## stale-while-revalidate
我们在 http 里已经使用缓存很多年了，不过有个问题很常见：如果缓存过期了会发生什么？
如果从缓存中可以立即取得响应，但是从服务器获取响应需要几百毫秒或者更久，那用户会很容易注意到这个细节差异。

一个理所当然的解决方案是“在缓存过期之前预拉取最新的内容”，这个听上去很合理，不过这引发了另外一个头疼的问题：“如何决定何时预拉取呢？”。如果没有正确实现预拉取策略，那就有可能加重缓存，网络以及后台服务器等等的负载。

退而求其次，另一个可以采取的方案是，对于那些”稍微“过期的缓存，允许先直接使用，然后在后台静默的更新缓存内容。

![1]({{ site.baseurl }}/image/http_cache_stale_1.png)

如上图所示，请求 #1 发出的时候，缓存内容还是新鲜的，所以直接从缓存中获取响应。
不过当请求 #2 发起的时候，本地缓存刚刚过期，此时 stale-while-revalidate 就开始发挥作用了，请求 #2 先直接从缓存中获取响应返回给调用者，然后在静默的在后台向原始服务器发起一次异步请求。
请求 #3 也一样，因为它们都在 ”stale-while-revalidate“ 时间窗口内。

所以，stale-while-revalidate 通过新鲜度的自由裁量，对客户端屏蔽了请求后台响应的等待时延。

一个响应的例子：

```
    Cache-Control: max-age=600, stale-while-revalidate=30
```

这个响应表明当前响应内容新鲜时间为 600 秒，以及额外的 30 秒可以用来容忍过期缓存，同时去验证（以及更新）当前缓存是否继续有效。
如果验证无效或者在这 30 秒内没有请求来触发验证，那么在这 30 之后，缓存内容就真正过期了。后续再发送过来的请求，都会像没有缓存一样，阻塞执行。

通常来说，服务器会将 max-age 和 stale-while-revalidate 的时间加在一起作为潜在最长可容忍的新鲜度时间。比如，如果两者都是设置的 600 秒，那么服务器就应该容许在 20 分钟内（1200 秒），所有的响应都由缓存提供。

另一点需要注意的是，异步验证只有处在缓存过期之后以及 stale-while-revalidate 时间窗口结束之前才会执行，时间窗口的大小以及实际请求的疏密程度都会影响到是否所有的请求都能够避免延时。
如果时间窗口太小，或者请求太稀疏，部分请求就就会落在时间窗口之后，这部分请求就会阻塞直到服务器有响应。

## stale-if-error

另一种要面对的问题是：后台服务宕机。在许多情况下，不应该给用户一个不友好的错误页面，而应该是给用户一个可用，哪怕是“稍微”过期的响应也行。stale-if-error 就是出于这种考虑，让你可以配置这种策略。

一个响应的例子：

```
    HTTP/1.1 200 OK
    Cache-Control: max-age=600, stale-if-error=1200
    Content-Type: text/plain

    success
```

上述响应的新鲜时间为 600s，如果后续请求碰到某种错误，那么在（这 600s）随后的 1200s 时间内，可以继续使用这个缓存响应。
注意这里与 stale-while-revalidate 的区别，两者在新鲜时间之后的表现是不一样的，stale-while-revalidate 会先返回缓存，同时再静默的在后台进行缓存验证。而 stale-if-error 是先去向服务器进行缓存验证，如果遇到服务器错误之后才使用这个缓存。

对于上述响应中的 stale-if-error，假如缓存验证发生在缓存过期后的 900s，此时还在 stale-if-error 指明的 1200s 范围内，所以服务器返回的结果会类似这种：

```
    HTTP/1.1 500 Internal Server Error
    Content-Type: text/plain

    failure
```
但是请求得到的实际响应依旧是成功的，同时为了指明这是个缓存结果，附带了一个 “Age: 900” 头部：

```
    HTTP/1.1 200 OK
    Cache-Control: max-age=600, stale-if-error=1200
    Age: 900
    Content-Type: text/plain

    success
```
如果缓存验证发生在 1800s（600 + 1200） 之后，那么缓存就直接返回错误信息：

```
    HTTP/1.1 500 Internal Server Error
    Content-Type: text/plain

    failure
```

## 实验

为了验证 stale-while-revalidate 的效果，我们可以构建一个新鲜时间 10s，stale 时间 30s 的响应，然后在第 15s 发送一个请求。
如果 stale-while-revalidate 没有生效，那么我们会看到服务器的最新响应，反之，我们还是会看到缓存中的响应。

服务器 node：

```javascript
var http = require('http');
var util = require('util');
var fs = require("fs");

var server = http.createServer(function(req, res){   
    console.log(req.url);
    if(req.url == '/favicon.ico'){
        res.end();
    }if(req.url == '/getData'){
         res.writeHead(200, {
            'Cache-Control' : 'max-age=10,stale-while-revalidate=30'
        });
        var data = new Date().toGMTString();
        res.end(data);
    }else{
        console.log(req.headers); 
        fs.readFile('cache.html', function(err, data){
            res.end(data);
        });
    }

}).listen(3000, function(){
    console.log('start');
});
```

前段界面 cache.html：

```html
<html>
    <head>
        <title>stale-while-revalidate</title>
    </head>
    <body>
        <button id="getData">getDate</button>
        <script type="text/javascript" src="https://cdn.bootcss.com/jquery/3.2.1/jquery.js"></script>
        <script type="text/javascript">
            function getData(){
                $.ajax({
                    url : 'getData',
                    cache :true,
                    success :function(data){
                        console.log(data);
                    }
                });
            }
            $('#getData').on('click', function(){
                getData();
                setTimeout(function(){
                   getData();
                }, 15000);
            });
        </script>
    </body>
</html>
```

响应结果：
    
    Thu, 22 Jun 2017 08:23:44 GMT # Thu, 22 Jun 2017 08:23:44 GMT
    Thu, 22 Jun 2017 08:23:59 GMT # Thu, 22 Jun 2017 08:23:44 GMT

相隔 15s 的两个请求响应结果是一样的，虽然响应缓存的新鲜时间只有 10s，但是依旧可用。

## 参考资料

1. [https://tools.ietf.org/html/rfc5861](https://tools.ietf.org/html/rfc5861)
2. [https://www.mnot.net/blog/2007/12/12/stale](https://www.mnot.net/blog/2007/12/12/stale)
3. [https://www.fastly.com/blog/stale-while-revalidate-stale-if-error-available-today](https://www.fastly.com/blog/stale-while-revalidate-stale-if-error-available-today)
4. [https://docs.fastly.com/guides/performance-tuning/serving-stale-content](https://docs.fastly.com/guides/performance-tuning/serving-stale-content)


