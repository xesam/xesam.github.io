---
layout: post
title: "finalhandler.js"
date: 2019-07-03 08:00:00 +0800
categories: javascript
tag: [javascript]
---

很多 Node 的 Web 框架中用到了这个 finalhandler.js 模块，它的作用按照官方文档描述如下：

> Node.js function to invoke as the final step to respond to HTTP request.

主要是在 req 的处理中作为最后的兜底处理器——错误处理。

<!-- more -->

比如我们可以这么使用：

```javascript
http
  .createServer(function (req, res) {
    if (req.url === "/") {
      res.end("<h1>Hello World</h1>");
    } else {
      var done = finalhandler(req, res);
      done();
    }
  })
  .listen(3000);
```

如果用户访问的不是 '/'，就会返回对应的错误提示。

finalhandler 接收 3 个参数：

    finalhandler(req, res, [options])

req 和 res 是 HttpServer 的 req 和 res，option 当前只有 2 个选项：

    env // 设置运行环境
    onerror // 设置错误回调，可以在此回调内记录错误日志

上面代码中的 done 可以接收一个 err 对象参数，用来定制对应的错误输出，规格如下：

1. 如果 err 为空，会返回默认的 404 相应。
2. err.status 或者 err.statusCode 会设置 res.statusCode，如果取值范围不在 4xx 和 5xx 之内或者没有设置，会强制设置为 500。
3. 如果 env （可以通过 options 参数来设置）是 production，res.statusMessage 的内容会根据 statusCode 的值被设置为对应的 HTML 格式输出。如果 env 不是 production，则会直接输出 err.stack 的值。
4. err.headers 会被添加到 res 的 headers 中。

典型示例：

```javascript
http
  .createServer(function (req, res) {
    var done = finalhandler(req, res, { onerror: logerror });

    fs.readFile("index.html", function (err, buf) {
      if (err) {
        return done(err);
      }
      res.setHeader("Content-Type", "text/html");
      res.end(buf);
    });
  })
  .listen(3000);

function logerror(err) {
  console.error(err.stack || err.toString());
}
```

如果 index.html 读取失败，会返回页面：

> Error: ENOENT: no such file or directory, open 'D:\work-fe\finalhandler\index.html'

同时在控制台打印粗错误日志。当然，也可以设置错误代码：

```javascript
if (err) {
  return done({
    status: 500,
    stack: err,
  });
}
```

如果设置了 env : 'production'，返回的页面就变为：

> Internal Server Error

这个模块就做了这些事，没有其他的内容了，不能定制错误页面，也就只能用在一些中间框架或者测试环境中。
对于通常的产品来说，还是太简略了。
