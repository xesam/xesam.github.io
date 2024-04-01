---
layout: post
title:  "API 设计案例（一）"
date:   2021-04-02 13:46:04 +0800
categories: software
tag: [software]
---

一个 API 的设计迭代案例...

<!-- more -->

## 概览
我们的某个产品用户端有个界面如下：

```
我是一个标题
```

现在需要给这个标题后面增加**个性化标语，**加上标语之后的显示如下**：**

```
我是一个标题（新年特别推荐）
```
## 版本 1.0
### 接口
于是后端就在接口数据中增加一个字段：

```javascript
{
    item:true
}
```

并约定字段含义：

```
如果 item 为 true，就展示个性化标语。
```
### 用户端
用户端的判定比较简单，控制显示与否即可。

```javascript
function titleV1(item){
  if(item){
    showSlogon();
  }else{
    hideSlogon();
  }
}

```

### 存在问题
现在问题就出现了，这么设计接口，存在几个明显的疏漏：

1. 如果没有这个字段，应用端应该如何处理？
2. 如果后续个性化标签发生了变化，应该如何处理？
3. 如果不同的客户希望支持不同的个性化标签，应该如何处理？
4. 如果个性化标签希望支持动图，应该如何处理？

面对任何一个需求的变更，原本的设计都无法应对。于是对接口字段进行重新设计。
## 版本 2.0：
### 接口
现实问题：由于应用端版本已经发布，原本的接口定义无法更改，就只能再新增一个字段了：

```javascript
{
    newItem:{
      value:''
    }
}
```

并约定字段含义：

```
字段缺失：
如果 newItem 缺失，则不展示个性化标语；
如果 newItem.value 缺失，则不展示个性化标语；

字段值有效：
如果 newItem.value 为 '0'，则不展示个性化标语；
如果 newItem.value 为 '1'，则展示个性化标语“（新年特别推荐）”；
如果 newItem.value 为 '2'，则展示个性化标语“（鼠年特别推荐）”；
```

_关于 value 字段值的类型，也可以选择 int，int 的好处就是可以非常容易的定义有效值范围，比如我们可以约定：如果 value 值小于 0，则判定 value 的值无效，简单丢弃即可。_
### 用户端
用户端采用“白名单”的处理方式，只处理“认识”的值，不认识的值一律丢弃。

```javascript
function titleV2(newItem){
  if(newItem.value === '1'){
      title.text = '（新年特别推荐）';
      showSlogon();
    }else if(newItem.value === '2'){
      title.text = '（鼠年特别推荐）';
      showSlogon();
    }else{
      hideSlogon();
    }
}

if(newItem){
  titleV2();
}else{
  hideSlogon();
}
```

### 管理后台
后台只需要选择 newItem 并设置对应的 value 值即可。
由于存在历史版本，因此运营人员配置 newItem 的时候，后台系统需要自动配置老版本 item 的值：

1. 如果 newItem.value 设置为 '1'，则将 item 配置为 true；
2. 如果 newItem.value 设置为 '2'，则将 item 配置为 true；
3. 如果 newItem.value 设置为其他值，则将 item 配置为 false；
4. 如果没有配置 newItem，则将 item 配置为 false；

### 存在问题
问题一：value 是给程序逻辑看的字段，单看 value 的值，除非看代码或者查找接口文档，不然单从'1'或者'2'这种配置是无法得知用户端展示的文字到底是什么。
问题二：用户端的个性化标语是预置的，如果要新增加标语，则必须要发布用户端版本。

因此，这个接口可以继续改进。

## 版本 3.0
### 接口
既然标语是一段文字，那我们就干脆把实际要展示的文字也放到接口中：

```javascript
{
    newItem:{
      value:'1',
      text:'（新年特别推荐）'
    }
}
```

并约定字段含义：

```
字段缺失：
如果 newItem.text 缺失，则回退到版本2.0；

字段值有效：
如果 newItem.text 不为空，则展示个性化标语“${text}”；
```

关于“不为空”的理解，不同的产品可能有不同的定义，保持一致即可。比如，我们可以认为只有在以下两种情况，text 的值才被认为是“空”：

1. text 为 '';
2. text 为 null；

如果是其他字符串，则均不为空；
### 用户端
优先判定 text，然后判定 value，如果没有 text 字段，则降级到版本 2.0，以保证版本的向前兼容用。至于 text 的值，只要不为空，就直接显示。

```javascript
function titleV3(newItem){
  if(isEmpty(newItem.text)){
    title.text = newItem.text;
    showSlogon();
  }else{
    titleV2(newItem);
  }
}

if(newItem){
  titleV3(newItem);
}else{
  hideSlogon();
}
```

### 管理后台
经过迭代之后，后台需要兼容的配置就多了起来，而且，由于 value 和 text 同时控制了用户端 UI 的显示结果，可能就无法自动的来进行适配了。
因此后台系统需要在运营人员进行配置的时候，可能就需要同时配置 value 和 text 了：

1. 设置 text 的值 ${text}；
2. 如果历史版本中的 value 存在与 ${text} 对应的值，则配置 value 为对应的值；
3. 如果历史版本中的 value 不存在与 ${text} 对应的值，则根据实际情况配置 value 为的值；

比如：
```javascript
{
    newItem:{
      value:'1', // 不存在与 text 对应的 value，则选择一个最合适的 value
      text:'（新年特别特别特别特别特别推荐）'
    }
}
```

## 版本 4.0
在处理完版本 3 的情况之后，“支持动图”的需求就类似了。
### 接口
```javascript
{
    newItem:{
      value:'1', 
      text:'（新年特别特别特别特别特别推荐）',
      icon:'http://x.y.z/xxx.png'
    }
}
```

约定字段含义：

```
字段缺失：
如果 newItem.icon 缺失，则回退到版本 3.0；

字段值有效：
如果 newItem.icon 不为空，则展示个性化标语的动图“${icon}”；
```

### 用户端
接口的定义很明确，但是 icon 与 text 不同，icon 的显示是一个异步的过程，这个过程存在”成功“或者”失败“的可能性，如果”失败“，是选择”不显示“还是”显示 ${text}“就是一个需要定义的机制了。用户端的处理需要明确的约定，在此，我们采取的原则是”尽可能的显示“，于是我们选择”显示 ${text}“。

```javascript
function titleV4(newItem){
  if(isEmpty(newItem.icon)){
    titleV3(newItem);
  }else{
    load(newItem.icon).then(img=>{
      title.imgSrc = img;
      showSlogon();
    }).catch(err=>{
      titleV3(newItem);
    });
  }
}

if(newItem){
  titleV4(newItem);
}else{
  hideSlogon();
}
```


_这里根据不同的用户端平台，采取的策略可能也会不一致，比如 Android 应用，无法直接给图片组件设置 src，因此需要应用自身实现图片的加载逻辑。但是如果是 web 页面，可以给 image 标签设置 src，无需应用自身管理图片的加载。因此，是选择显示顺序上，可以有不同的策略，比如“先显示 text，在 icon 加载完毕之后，再用icon 替代（或者覆盖）”。_

### 管理后台
与版本 3.0 类似，运营人员在配置后台的时候，需要慎重选择各个字段的值：

1. 设置 icon 的值 ${icon}；
2. 根据 icon 的内容，设置 text 的值 ${text}；
3. 参考版本 3.0 的配置，设置 value；
## 总结
与 UI 配置相关的字段，尽量使用对象的形式，以便于后续的扩展。换句话说，需要遵顼设计的基本原则：**渐进增强，平稳降级**。

