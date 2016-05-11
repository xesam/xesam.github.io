---
layout: post
title:  "【Android】使用MockWebServer来进行单元测试"
date:   2016-05-10 08:00:00 +0800
categories: Android
---
[MockWebServer](https://github.com/square/okhttp) 是 square 出品的跟随 okhttp 一起发布，用来 Mock 服务器行为的库，用来做单元测试挺好。

有一个单独的文档[https://github.com/square/okhttp/tree/master/mockwebserver](https://github.com/square/okhttp/tree/master/mockwebserver)

MockWebServer mock 了 http 协议栈，所以基本上可以用来调试所有的 http 请求。

## 基本使用

使用也比较简单：

```java
    @Test
    public void test() throws Exception{
        // 1. 创建服务器
        MockWebServer server = new MockWebServer();
    
        // 2. 添加预置的响应，响应会按照先进先出的顺序依次返回
        server.enqueue(new MockResponse().setResponseCode(503).setBody("hello, world!"));
        server.enqueue(new MockResponse().setBody("i am xesam"));
        server.enqueue(new MockResponse().setResponseCode(404).setBody("not found"));
    
        // 3. 启动服务器
        server.start();
    
        // 4. 获取请求 url，不能使用普通的 URL，一定要使用 server.url() 返回的 URL，不然没法进入 Mock 服务器
        HttpUrl baseUrl = server.url("/reg1");
        
        // 5. 发送请求
        HttpRequest.get(baseUrl.url()).body()
    
        // server.takeRequest() 是一个阻塞操作，直到接收到请求
        RecordedRequest request1 = server.takeRequest();
        
        // 这里可以查看服务器获取的请求信息，可以查看 http 报文头之类的协议信息
        assertEquals("/v1/chat/", request1.getPath());
    }
```

MockResponse 默认是状态码 200， body 为空，但是可以定制所有的协议内容：

```java 
MockResponse response = new MockResponse()
    .addHeader("Content-Type", "application/json; charset=utf-8")
    .addHeader("Cache-Control", "no-cache")
    .setBody("{}");
    
```

还可以模拟网速比较慢的情况：

```java
response.throttleBody(1024, 1, TimeUnit.SECONDS);  //每秒传递 1024 字节
```

按照最开始的描述，可以用 enqueue 来添加预置响应，其实可以做得更像服务器一些，即根据 url 来进行响应分发：

```java
final Dispatcher dispatcher = new Dispatcher() {

    @Override
    public MockResponse dispatch(RecordedRequest request) throws InterruptedException {

        if (request.getPath().equals("/v1/login/auth/")){
            return new MockResponse().setResponseCode(200);
        } else if (request.getPath().equals("v1/check/version/")){
            return new MockResponse().setResponseCode(200).setBody("version=9");
        } else if (request.getPath().equals("/v1/profile/info")) {
            return new MockResponse().setResponseCode(200).setBody("{\\\"info\\\":{\\\"name\":\"Lucas Albuquerque\",\"age\":\"21\",\"gender\":\"male\"}}");
        }
        return new MockResponse().setResponseCode(404);
    }
};
server.setDispatcher(dispatcher);
```

如此一来，其实就可以在通常的开发中将后台的接口提前 mock 出来，加快开发进度。

## 异步测试

在单元测试中，如果有异步调用，通常就比较麻烦，因为在异步回调还没回来的时候，测试已经完成了，所有这个时候就需要让进程等待或者挂起。
比如，使用 MockWebServer 来测试 Volley：

```java
public class Test1 extends InstrumentationTestCase {
    public void testVolley() throws Exception {
        MockWebServer server = new MockWebServer();
        server.enqueue(new MockResponse().setResponseCode(200).setBody("hello, world!"));
        server.start();

        HttpUrl baseUrl = server.url("/p1");
        final BlockingQueue<Object> queue = new ArrayBlockingQueue<>(10);

        Volley.newRequestQueue(getInstrumentation().getContext())
                .add(new StringRequest(baseUrl.url().toString(), new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        queue.add(response);
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        queue.add(error);
                    }
                }));

        RecordedRequest request1 = server.takeRequest();
        assertEquals("/p1", request1.getPath());

        Object obj = queue.take();
        if (obj instanceof String) {
            Assert.assertEquals("hello, world!", obj.toString());
        }

        server.shutdown();
    }
}
```

上面的例子中使用一个 BlockingQueue 来等待 Volley 的请求结束，然后验证结果。

当然，也可以用锁，但是其实都挺麻烦。
