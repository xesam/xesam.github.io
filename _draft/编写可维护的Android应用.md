让一个程序可维护是多方面的。


模块之间的通信：

基于接口的通信，用方法来表明意图，而不是用参数来表明意图

比如发送消息

```java

    public static final int MSG_START = 0;
    public static final int MSG_STOP = 1;

    // start
    Message.obtain(handler, MSG_START).sendToTarget();
    
    // stop
    Message.obtain(handler, MSG_STOP).sendToTarget();
    
```
   
更容易维护的代码：

```

    private static final int MSG_START = 0;
    private static final int MSG_STOP = 1;

    // start
    public void start(){
        Message.obtain(handler, MSG_START).sendToTarget();
    }
    
    // stop
    public void stop(){
        Message.obtain(handler, MSG_STOP).sendToTarget();
    }

```

隐藏细节：

BroadcastReceiver 的例子

    
用层次来构建人与机器的桥梁



