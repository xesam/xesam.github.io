---
layout: post
title: "小程序组件通信"
date: 2020-09-14 08:00:00 +0800
categories: fe
tag: [fe]
---

小程序文档中关于“组件间通信与事件”的部分写得比较简单，在此主要记录官方的几种标准用法，以及一些骚操作。

<!-- more -->

## 父节点、子节点、父组件、子组件

这些定义并不是官方文档所给出的，只是本文为了方便说明，专门为本文定义的，下面是具体说明。

在小程序中，构建组件页面的方式有两个途径：

1. 在组件自身的布局文件中直接定义，这种在页面中直接定义的节点称为“直接子节点”；
2. 在使用组件时，通过 slot 标签引入子节点，被引入的节点称为“slot子节点”。

一个示例：

组件布局：component.wxml

```xml
<view>
  <view name="view-1">......</view>
  <slot></slot>
</view>
```

页面布局：page.wxml

```xml
<view>
  <component>
    <view name="view-2">......</view>
  </component>
</view>
```

在上面的示例中，view-1 是 component 的“直接子节点”，view-2 是 component 的“slot子节点”。

这两种引入子节点的方式，会影响组件的通信方式，因此特意做个区分。

按照概念来讲，“父组件&子组件” 与 “父节点&子节点” 是两类不同的抽象。“组件”更侧重说明功能，“节点”更侧重表现结构。
还是以上面的例子来讲：

1. 对于组件来讲，component.wxml 代表一个“组件”，view-1 是这个“组件”的一个子节点。
2. 对于页面来讲，component 本身也是一个子节点。

如果不必要区分，后文将混用这两组概念。

## 官方文档方式

### 父组件向子组件传递数据

1. WXML 数据绑定。子组件定义 properties，父组件通过 setData 方法给子组件传递数据。
2. 父组件通过 this.selectComponent 方法获取子组件实例对象，直接访问组件的数据，或者调用子组件的方法。

这里的“子组件”，指的其实是“直接子节点”，“slot子节点”是获取不到的。也就是说：**this.selectComponent 只能在“直接子节点”里面查找，不能在“slot子节点”里面查找**

如果要获取“slot子节点”应该怎么办呢？

官方文档内没有找到直接的方法，不过小程序可以定义“组件间关系”。“组件间关系”有两类：

1. parent 和 child
2. ancestor 和 descendant

可见，“组件间关系”只能定义上下级关系。如果组件配置了“组件间关系”，还可以通过 this.getRelationNodes 方法来获取关系组件的节点实例，也可以直接访问关系组件的数据，或者调用关系组件的方法。由于“组件间关系”本身的局限，这个方法也就只能用于事实上的父子组件，而不能用于兄弟组件。*注意，这里特意指出是“组件”*。

事实上，个人觉得 this.getRelationNodes 正是用来在“slot子节点”内进行查找的，而且确实有效。与 this.selectComponent 类似，这个方式也有局限，与 this.selectComponent 正好相反，**this.getRelationNodes 只能在“slot子节点”里面查找，不能在“直接子节点”里面查找**

示例说明：parent-view 与 child-view 是关系组件。
 
组件布局：parent.wxml

```xml
<view>
    <slot></slot>
    <child-view name="inner-a" class="selectComponent-class"/>
    <child-view name="inner-b" class="selectComponent-class"/>
</view>
```

页面布局：

```xml
<parent-view>
    <child-view name="slot-a" class="selectComponent-class" />
    <child-view name="slot-b" class="selectComponent-class"/>
</parent-view>
```

    this.selectComponent('.selectComponent-class') 返回节点 inner-a.
    this.getRelationNodes('child'); 返回节点 slot-a, slot-b.

总结起来， this.selectComponent 与 this.getRelationNodes 两个主要区别：

1. this.selectComponent 只能在“直接子节点”里面查找，不能在“slot子节点”里面查找;this.getRelationNodes 只能在“slot子节点”里面查找，不能在“直接子节点”里面查找
2. this.selectComponent 只能获取第一个找到的节点，而 this.getRelationNodes 能获取所有找到的节点。

### 子组件向父组件传递数据

1. 子组件通过 this.triggerEvent 发出一个事件，父组通过WXML 绑定的事件监听器来监测此事件。

官方文档只给了这一种方式，其实也可以算是 “WXML 数据绑定” 的一种特别形式。

同理，如果组件配置了“组件间关系”，也可以通过 this.getRelationNodes 方法来获取父组件的节点实例，直接访问父组件的数据，或者调用父组件的方法。

同样，只有“slot子节点”能够通过 this.getRelationNodes 来获取父组件的节点。所以，对于上文的 inner-a，inner-b 这两个“直接子组件”，其实没有获取父节点的官方推荐方法。如果一定要获取，就只能想一些“骚方法”了。

### 骚操作

从 2.0.9 开始，WXML 数据绑定支持在数据中包含函数，比如：

```javascript

Component({
  properties:{
    fn:{
      type:Object,
      value:{
        get:function(){}
      }
    }
  }，
  lifetimes: {
    ready() {
        this.data.fn.get(this);
    }
  },
});

```

虽然写法比较丑，但是能用，因此，在实际使用的时候，不仅可以把数据都格式化好之后再传递给子组件，还可以直接把格式化函数传递给组件，毕竟，格式化的定制需求比较多。

父组件的调用形式：

父组件 page.js：

```javascript
Page({
  onLoad(){
    this.setData({
      fn: {
          get(child) {
              console.log(child.data.name, 'created');
          }
      }
    });
  }
});

```
page.wxml 通过 properties 进行数据绑定：
```xml
  <child-view name="inner-a" fn="{{fn}}"/>
```

理论上只要能够传递函数，就可以在父组件与子组件之间创建一个通道，组件之间直接通过这个通道来通信，效果也是一样的。

子组件：

```javascript

Component({
    options: {virtualHost: true},
    behaviors: [Child],
    properties: {
        name: {type: String, value: ''},
        fn: {
            type: Object,
            value: null,
            observer(newVal, oldVal, changedPath) {
                if (newVal) {
                    const parent = newVal.get(this); //得到 parent
                    console.log('parent = ', parent);
                }
            }
        }
    }
});

```
父组件：

```javascript
Component({
    created() {
        const _this = this;
        this.setData({
            fn: {
                get(child) {
                    console.log('child = ', child); //得到 child
                    return _this;
                }
            }
        });
    }
});

```
如此一来，两个组件之间可以相互持有，由于 WXML 数据绑定是小程序最基础的通信方式，因此，这种方式是没有什么限制的。不过，这种方式带来的问题也很明显：**内存泄漏**，如果一定要这么干，记得一定要在组件的生命周期处理好引用的管理。

同理，既然数据绑定能传递函数，那么子组件的 this.triggerEvent 一样也可以发送一个函数。

子组件：
```javascript

Component({
    methods: {
        emit(){
          this.triggerEvent('emit', {
            sendMessage(data){
              console.log(data); //'来自 parent 的消息'
            }
          });
        }
    }
});

```
父组件：
```javascript

Component({
    methods: {
        onEmit(e){
          e.detail.sendMessage({
            msg:'来自 parent 的消息'
          });
        }
    }
});

```

事件绑定

```xml
  <child-view name="inner-a" class="selectComponent-class" bindemit="{{onEmit}}"/>
```

相比前一种“互相持有”，这种方式显得稳妥不少，毕竟如果不特意持有组件引用，是不会内存泄漏风险的。当然，这种方式稍微改造一下，与前一种方式也无异。

这种方式比较适合希望穿透父组件，直接操作子组件的情况。毕竟有时候直接通过子组件协议来操作比通过父组件协议来操作要方便不少，尤其是对于某些不必知会父组件的操作。

## slot 的问题。

组件数据不能穿过 slot 边界其实挺闹心的，给自定义组件造成了一些麻烦。比如定义一个 Stepper 组件：

stepper.wxml
```xml
<view>
    <view bind:tap="onTapDecrease">增加</view>
    <view>{{count}}</view>
    <view bind:tap="onTapIncrease">增加</view>
</view>
```

stepper.js

```javascript
Component({
    methods: {
        onTapDecrease(){
          this.setData({
            count:this.data.count - 1
          });
        },
        onTapIncrease(){
          this.setData({
            count:this.data.count + 1
          });
        }
    }
});
```

如果希望使用者可以自定义 count 的展现样式，我们通常会这么写：

stepper.wxml
```xml
<view>
    <view bind:tap="onTapDecrease">增加</view>
    <view wx:if={{!useSlot}} class="ext-class">{{count}}</view>
    <slot wx:else></slot>
    <view bind:tap="onTapIncrease">增加</view>
</view>
```
可以把 ext-class 指定为 externalClasses，然后通过 ext-class 来覆盖组件内 count 的样式，不过这种毕竟局限性太大，有时候就只能通过 slot 来自定义 count 的页面结构。

调用方页面结构：
```xml
<stepper-view>
  <view><text>{{count}}</text></view>
</stepper-view>
```

### 绕个大圈

这个时候就面临问题了，由于通过 slot 添加的部分无法直接获取 stepper-view 内部的 count 属性，因此，只能通过 stepper-view 的宿主组件来借道实现（绕个大圈）：

宿主页面结构：
```xml
<stepper-view bindincrease="onIncreased">
  <view><text>{{count}}</text></view>
</stepper-view>
```

宿主方法：
```javascript
  ...
  onIncreased(e){
    this.setData({
      count:e.detail.count
    });
  }
```

这种方式着实麻烦，如果 slot 能支持数据传递，就会方便很多，比如：

stepper.wxml
```xml
<view>
    <view bind:tap="onTapDecrease">增加</view>
    <view wx:if={{!useSlot}} class="ext-class">{{count}}</view>
    <slot wx:else slot:data={{count}}></slot>
    <view bind:tap="onTapIncrease">增加</view>
</view>
```

宿主页面结构：
```xml
<stepper-view bindincrease="onIncreased">
  <view><text>{{slotData.count}}</text></view>
</stepper-view>
```
不过官方始终没有支持 slot 传值，个人开发者也没有办法绕过去，只能期待了。

### 无奈之举

所以，如果开发者想复用 stepper 现有的事件和交互，又想以灵活的方式修改页面结构，就只能将自定义的页面结构包装成特定的类型组件，使得 stepper 可以找到开发者自己的组件。

stepper.wxml
```xml
<view>
    <view bind:tap="onTapDecrease">增加</view>
    <view wx:if={{!useSlot}} class="ext-class">{{count}}</view>
    <slot wx:else></slot>
    <view bind:tap="onTapIncrease">增加</view>
</view>
```
找到开发者自定义的组件：

```javascript
Component({
    methods: {
        onTapDecrease(){
          const countView = this.getRelationNodes('countBehavior')[0];
          countView.setData({
            count:this.data.count - 1
          });
        },
        onTapIncrease(){
          const countView = this.getRelationNodes('countBehavior')[0];
          countView.setData({
            count:this.data.count + 1
          });
        }
    }
});
```
假如开发者自定义的组件叫 custom，那么 custom 须包含 countBehavior 这个 Behavior，从而可以直接接收与 stepper 通信：

```xml
<stepper-view>
  <custom />
</stepper-view>
```

貌似现阶段只有这么些方式，持续跟进...