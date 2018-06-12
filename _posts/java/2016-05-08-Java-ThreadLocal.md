---
layout: post
title:  "ThreadLocal设计意图"
date:   2016-05-08 13:46:04 +0800
categories: java
tag: [java]
---
核心原理

1. ThreadLocal 处理的是线程的专属对象，各个线程的对象都是独立的。
2. ThreadLocal 用来辅助平衡效率与资源分配。
3. ThreadLocal 不是同步机制，也不解决共享对象的多线程竞态条件问题。

## 基本设计

首先看一个熟悉的场景：排队买票。

从理论上看，针对“排队买票”这个场景，我们可以有以下几种方案设计：

第一种. 固定设置一个售票窗口，每新来一个购票者就排在队伍的最后面。如图：


![1]({{ site.baseurl }}/image/java_threadlocal_1.png)

第二种. 动态设置售票窗口数量，每新来一个购票者就新开一个窗口来进行接待。如图：


![1]({{ site.baseurl }}/image/java_threadlocal_2.png)

第三种. 固定设置 N 个售票窗口，每新来一个购票者就选择一个售票窗口。如图：


![1]({{ site.baseurl }}/image/java_threadlocal_3.png)

比较一下上面的三种方案，很明显现实社会中使用的是第三种，那么各自有什么优势与缺点呢？

<!-- more -->

首先，整个卖票过程中，售票员是稀缺资源，售票窗口也是要消耗资源的。而且卖票的瓶颈也在售票窗口，因为售票员与购票者的交流需要花费很多时间，购票者多是在等待而已。

第一种：

优势是资源消耗低，只需要一个售票窗口就可以了，另一个好处就是不用处理不同售票窗口卖出了同一张票的问题（即竞态条件处理），
因为任一时刻只会有一个售票窗口，一次只会卖一张票，后台数据中心按顺序出票就行了。
但是劣势更明显，就是排队的效率低，如果购票者人数比较多，那么购票者的队伍会非常长。

第二种：

优势是排队效率高（根本就不用排队）。
劣势也很明显，不可能提供无限的售票窗口来满足大量的购票需求，另外，新建售票窗口也是需要时间的。
另一个问题就是，如果不同售票窗口都想卖出同一张票，这时后台数据中心就需要进行协调处理了（即竞态条件处理）。

第三种：

这种方式与上面两种并无绝对优势，只是一种平衡而已。
相比第一种方式，购票者需要排的队短很多；相比第二种方式，在售票窗口的资源投入上会少很多。

**本文不讨论竞态条件的问题，因为为了防止卖出同一张票，你也可以让所有的售票窗口自己协商（比如任一时刻只能有一个售票窗口卖票，等等）。**

那么，这个场景怎样对应到具体的程序中呢？

    后台数据中心 —— 数据库
    售票窗口 —— 数据库连接
    购票者 —— 单个消息（也就是具体的单个任务，此处我称之为“消息”）
    购票队列 —— 消息队列

其中：

    一组 售票窗口 + 购票队列 + 购票者

属于同一个线程的内部变量。

注意，本文的核心是关注点是售票窗口资源消耗。这个时候就是 ThreadLocal 出场的时候，看一个演示程序：

```java
public class ThreadLocalTest {
    public static void main(String[] args) {
        new Thread() {
            @Override
            public void run() {
                TicketWindow ticketWindow = TicketWindow.prepare();
                IntStream.range(0, 5).forEach(i -> new Buyer("buyer_" + i).enqueue());
                ticketWindow.open();
            }
        }.start();

        new Thread() {
            @Override
            public void run() {
                TicketWindow ticketWindow = TicketWindow.prepare();
                IntStream.range(5, 10).forEach(i -> new Buyer("buyer_" + i).enqueue());
                ticketWindow.open();
            }
        }.start();
    }
}

class TicketWindow {

    private static ThreadLocal<TicketWindow> sTicketWindow = new ThreadLocal<TicketWindow>() {
        public TicketWindow initialValue() {
            return new TicketWindow(Thread.currentThread().getName());
        }
    };

    public static TicketWindow prepare() {
        return sTicketWindow.get();
    }

    private String name;
    private BuyerQueue buyerQueue;

    public TicketWindow(String name) {
        this.name = name;
        this.buyerQueue = new BuyerQueue();
    }

    public String getName() {
        return name;
    }

    public void enqueue(Buyer buyer) {
        buyerQueue.enqueue(buyer);
        System.out.println("enqueue:" + buyer.getName());
    }

    public void open() {
        while (true) {
            Buyer buyer = buyerQueue.poll();
            if (buyer != null) {
                System.out.println(getName() + " turn:" + buyer.getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                buyer.buy();
                System.out.println(getName() + " sold:" + buyer.getName());
            }
        }
    }
}

class BuyerQueue {
    private Queue<Buyer> queue = new LinkedBlockingDeque<>();

    public void enqueue(Buyer buyer) {
        queue.add(buyer);
    }

    public Buyer poll() {
        return queue.poll();
    }

}

class Buyer {

    private String name;

    public Buyer(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void enqueue() {
        TicketWindow ticketWindow = TicketWindow.prepare();
        ticketWindow.enqueue(this);
    }

    public void buy() {
    }
}
```

其中，TicketWindow 在每个 Thread 只会有一个，每个 Thread 的 TicketWindow 都不同。

在使用的过程中，既不需要显示的给线程设置 TicketWindow，其他线程也访问不了当前线程的 TicketWindow，也起到了排除干扰的效果。

**当然，不用 ThreadLocal，直接用 Map 也可以，ThreadLocal 也是用 Map 实现的**

## 一个实际的应用

SimpleDateFormat 是线程不安全的，如果每次调用都 new 一个新的 SimpleDateFormat 对象，实在浪费。所以这个时候就可以用 ThreadLocal
来让每个线程都持有一个 SimpleDateFormat 的实例，避免创建无用的对象。

## ThreadLocal 与 clone

到这里，似乎不需要 ThreadLocal，直接用 clone() 也可以达到相同的效果。
这当然没错，不过使用 clone() 的话，就需要处理更多的细节，而且与 ThreadLocal#initialValue() 的作用是一致的。

## 存在问题

通常来讲，ThreadLocal 不会造成什么大问题，因为在 Thread 执行完毕的时候，所有的资源都会被自动释放掉。

唯一的问题就是——线程池。

如果我们在线程池中使用了 ThreadLocal ，由于我们通常无法直接控制线程池线程的创建与释放，也就意味着除非手动清除掉 ThreadLocal 中的资源，
否则，ThreadLocal 持有的资源可能永远无法释放，内存泄漏的隐患由此而生。

## 结束语
ThreadLocal 把对象级别的变量共享变为线程级别的变量共享，从而辅助平衡资源与效率，本身并不是一种同步机制，因为每个线程持有的都是不同的对象。
至于对象所要处理的状态问题，交给别的角色去处理了。所以，本质上是将整个同步的时机向后延迟了（或者说，转移了同步责任）。
