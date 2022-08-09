---
layout: post
title: "小程序组件通信"
date: 2020-09-14 08:00:00 +0800
categories: fe
tag: [fe]
---

小程序文档中关于“组件间通信与事件”的部分写得比较简单，在此主要记录官方的几种标准用法，以及一些骚操作。

<!-- more -->

## 官方文档方式

### 父组件向子组件传递数据

1. WXML 数据绑定。子组件定义 properties，父组件通过 setData 方法给 子组件传递数据。
2. 父组件通过 this.selectComponent 方法获取子组件实例对象，直接访问组件的数据，或者调用子组件的方法。

如果父子组件配置了“组件间关系”，还可以使用：

3. 父组件通过 this.getRelationNodes 方法来获取子组件的节点实例，也可以直接访问子组件的数据，或者调用子组件的方法。

不过 this.selectComponent 与 this.getRelationNodes 有些区别：

1、this.selectComponen 只能获取第一个匹配的节点，而 this.getRelationNodes 能获取所有匹配的节点。
2、this.selectComponen 无法在父组件内查找 slot 中的节点，而 this.getRelationNodes 只能在父组件内查找 slot 中的节点。

示例说明：

父组件：

```xml
<view>
    <slot></slot>
    <child-view name="inner-a" class="selectComponent-class"/>
    <child-view name="inner-b" class="selectComponent-class"/>
</view>
```

页面文件：

```xml
<parent-view mini-data="{{active}}">
    <child-view name="slot-a" class="selectComponent-class" />
    <child-view name="slot-b" class="selectComponent-class"/>
</parent-view>
```

this.getRelationNodes('child') 返回节点 slot-a, slot-b.

this.selectComponent('.selectComponent-class') 返回节点 inner-a.

所以，这个区别使“父组件”与“子组件”的定义有点模糊不清，文档也没有直接说明。

### 子组件向父组件传递数据

1. 子组件通过 this.triggerEvent 发出一个事件，父组通过WXML 绑定的事件监听器来监测此事件。

如果父子组件配置了“组件间关系”，还可以使用：

2. 子组件通过 this.getRelationNodes 方法来获取父组件的节点实例，直接访问父组件的数据，或者调用父组件的方法。

*同样，只有通过 slot 添加的子组件能够通过 this.getRelationNodes 来获取父组件的节点。所以，对于上文的 inner-a，inner-b 组件，其实没有直观的办法获取父组件的节点。还是说，其实 inner-a，inner-b 本就是父组件的一部分？*

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

虽然写法比较丑，但是能用，比如可以把格式化函数传递给组件，避免在父组件来进行格式化。调用形式：

父组件：

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
通过 properties 进行数据绑定：
```xml
  <child-view name="inner-a" class="selectComponent-class" fn="{{fn}}"/>
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
                    const parent = newVal.get(this);
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
                    console.log('child = ', child);
                    return _this;
                }
            }
        });
    }
});

```
如此一来，两个组件之间可以相互持有，由于 WXML 数据绑定是小程序最基础的通信方式，因此，这种持有是没有什么限制的，不过，这种方式带来的问题也很明显：**内存泄漏**，如果一定要这么干，记得一定要处理好组件的生命周期。

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

这种方式相比前一种“互相持有”，显得稳妥不少，毕竟如果不特意保存引用，是不会有什么内存泄漏的问题的。这种方式比较适合希望穿透父组件，直接操作子组件的情况。毕竟有时候直接通过子组件协议来操作比通过父组件协议来操作要方便不少，尤其是对于某些不必知会父组件的操作。

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
如果希望使用者可以自定义 count 的显示样式，我们通常会这么写：

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
<stepper-view bindincrease="onIncreased" slot-data="slotData">
  <view><text>{{slotData.count}}</text></view>
</stepper-view>
```
不过官方始终没有支持 slot 传值，个人开发者也没有办法绕过去，只能期待了。

### 无奈之举

所以，如果开发者想重用 stepper 现有的事件和交互，又想以灵活的方式修改页面结构，就只能要求开发者将自定义的页面结构包装成特定的类型组件，使得 stepper 可以找到开发者自己的组件。

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
<stepper-view bindincrease="onIncreased" slot-data="slotData">
  <custom />
</stepper-view>
```

貌似现阶段只有这么些方式，持续跟进...