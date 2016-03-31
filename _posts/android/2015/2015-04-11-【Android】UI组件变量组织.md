---
layout: post
title:  "【Android】UI组件变量组织"
date:   2015-04-11 12:46:04 +0800
categories: android
---
# 【Android】UI组件变量组织

# 说明

***这不是一篇技术文章，而是因为最近项目新来了几个android新人，所以我琢磨在代码风格上进行一下统一，所以有了以下以及后面的几篇文章。***

## java文件内部UI组件变量组织

### UI组件使用小写字母“v”作为前缀。

v主要表示“View”，android源码中，变量前缀主要是“m”，但是个人觉得对于UI变量，还是用“v”比较清晰

### 意图导向，最小化抽象

UI变量的“声明类型”应该是能够实现意图的最小化抽象类型，变量名需要能表现出一个组件的功能。

比如，交互需求有一个ImageButton，点击之后的动作是触发一个搜索请求。应该怎么组织变量呢？

#### 第一步：声明类型

声明这个变量大概有几种方式：

```java
    1. private ImageButton varName;
    2. private ImageView varName;
    3. private View varName;
```

这些声明都没有什么问题，问题是如果这个按钮只是单纯的触发一个点击事件，
那么也就表明我们的意图只需要使用View级别就行，因为View.setOnClickListener(OnClickListener)是我们唯一关心的功能，所以只需要将类型限定在View级别就行。

另外，UI是一个变化频度比较高的部分，越抽象就越容易修改。
换句话说，就是“面向接口编程”，View在这里就充当了接口的角色，这样，不管以后我们把ImageButton换成ImageView，Button或者TextView都不用修改定义的。

#### 第二步：变量名

变量命名可能有下面几种：

1.

        ImageButton vImageButton1

这种命名只应该出现在教程代码中，项目代码中是绝对不应该出现的

2.

        ImageButton vSearchImageButton（或者vQueryBtn）

这个命名其实可以接受，但是一个问题就是，变量名涉及到具体的组件类型，参照上面第一步的说明，如果并不会使用到“ImageButton”特定的方法，就没有必要过于具体化一个变量。

3.

        ImageButton vSearch

这个命名其实也可以接受，而且也比较适用。

4.

        ImageButton vSearchAction

相比上面的vSearch，个人还是比较偏向于这种命名。
虽然都是纯粹的意图相关，但一个问题就是完成某个意图可能需要几个组件配合，比如对于搜索来说，一般还会有一个输入框，这时候就可以将输入框命名为vSearchContent，这样可以使用后缀“Action”和“Content”将两个部分区分开来


## XML内部组件id命名

xml文件中的id命名也是一样，需要提供给java文件使用的尽量意图导线。
比如RelativeLayout命名中没有必要含有完整的“RelativeLayout”字段，因为实际项目中，需要调用RelativeLayout特定方法的情况基本没有。所以使用container等更泛的名字也可以。

至于只在布局文件中用来进行定位或者锚点的组件，可以将id命名得更明显一下，比如使用local,anchor之类名字，以便告诉java代码不应该随意获取这些组件，因为这些id并非稳定字段。
