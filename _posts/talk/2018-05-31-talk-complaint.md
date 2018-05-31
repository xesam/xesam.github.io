---
layout: post
title:  "吐槽-碎碎念"
date:   2018-05-31 08:00:00 +0800
categories: talk
tag: [talk]
---
纯吐槽，请忽略。

最近一直在帮忙做 code review，对现在有的程序员的态度真的是不敢恭维。贴代码：

```java
    Function<String, Integer> getTimeNo = ts -> {
        Integer timeNo = 0;
        if (StringUtils.isBlank(ts))
            return timeNo;
        String hour = ts.split(":|：")[0].trim();
        String minute = ts.split(":|：")[1].trim();
        if (hour.startsWith("0")) {
            timeNo += Integer.parseInt(hour.substring(1, 2)) * 4;
        } else {
            timeNo += Integer.parseInt(hour) * 4;
        }
        if (minute.startsWith("0")) {
            timeNo += (Integer.parseInt(minute.substring(1, 2)) / 15);
        } else {
            timeNo += (Integer.parseInt(minute) / 15);
        }
        return timeNo;
    };
```

这段代码的本意是将一天按 15 分钟划分成一个连续的片段，即 1 个小时被划分成 4 段，全天的划分就类似[0:00 - 0:14, 0:15 - 0:29,...,23:45 - 23:59]，然后输入一个 time 字符串（格式为 02:23 表示 2 分 23 秒），获取这个 time 字符串对应到哪个 15 分钟片段内，然后返回片段的索引。

就这么一个简单的需求，看看上面的代码犯了多少错误。

第一、如何解析 time 字符串，获取小时和时间

```java
    String hour = ts.split(":|：")[0].trim();
    String minute = ts.split(":|：")[1].trim();
```

犯下的错误：

1. 是否有必要区分半角和圆角。没有必要，因为字段是前后端约定的，如果在约定格式上还需要做兼容，就说明相关的前端开发人员需要好好反思。如果容许前端乱传，那这么点兼容实在远远不够。

2. 如果不信任前端，那 split 也可能出问题，而且出了问题就异常，这是一个风险点。

2. 想象力太丰富。这了既然用了 java8 的特性，就应该多了解一点，直接用 LocalTime.parse 就搞定了所有的解析过程。

第二、解析数字字符串

```java
    if (hour.startsWith("0")) {
        timeNo += Integer.parseInt(hour.substring(1, 2)) * 4;
    } else {
        timeNo += Integer.parseInt(hour) * 4;
    }
```

犯下的错误：

1. 不得不说，这对 java 的理解也太敷衍了，前面有没有 0 对 Integer.parseInt 一点影响都没有，这个 if 纯粹是多此一举。
2. 上文中既然连半角和全角的情况都考虑了，那为何在这里又这么信任前端的数据，如果前端传一个 25:00，那么最后得到的时间就是错误的，却无法被发现。  
3. Integer.parseInt 的异常没有处理，一旦出错就会导致程序崩溃，简直初级！
4. 与第 2 条同样的疑问，如果前端传过来的是 0:12 这样字段，那 substring(1,2) 就毫不留情的抛出 StringIndexOutOfBoundsException 异常，又是一个坑。不如直接使用 substring(1)，何必画蛇添足去指定第 2 个参数。


那这段代码应该怎么写？

其实这里用 Function 就已经很坑爹了，这个逻辑完全应该是一个独立的方法：

```java
    public static int getTimeIndex(String timeStr) throws Exception {
        LocalTime time = LocalTime.parse(timeStr);
        return time.getHour() * 4 + time.getMinute()/15;
    }

```

当然，整理还有改进的方法，就看具体的需求和度了。比如 15 这个魔数不应该要，以及 15 应该是一个参数变量，以及异常应该怎么处理，是不是需要提供默认值，等等。不过本文只是一个纯粹的吐槽，不是关于重构的主题。

深深的忧虑。