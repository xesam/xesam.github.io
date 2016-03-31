---
layout: post
title:  "【Android】ListPopupWindow"
date:   2014-12-04 12:46:04 +0800
categories: android
---

# ListPopupWindow

## 简述

ListPopupWindow最低要求为api11，为了兼容到2.1, 可以使用包含在support V7包中实现。
从效果上来讲，ListPopupWindow就是一个弹出层的ListView，比较适合用来实现自定义的下拉菜单以及自定义的下拉选择列表。

## 使用

### 自定义样式

一个示例：

```xml
    <style name="V7.ListPopupWindowStyle" parent="@style/Widget.AppCompat.ListPopupWindow">
        <item name="android:popupBackground">#404040</item> //弹出层的背景
        <item name="android:dropDownVerticalOffset">0dip</item>
        <item name="android:dropDownHorizontalOffset">0dip</item> //水平以及垂直位移
        <item name="android:dropDownWidth">match_parent</item> //这个效果不大
    </style>

    <style name="V7.DropDownListViewStyle" parent="@style/Widget.AppCompat.ListView.DropDown">
        <item name="android:listSelector">@drawable/list_selector</item> //
        <item name="android:divider">#242424</item>
        <item name="android:dividerHeight">1px</item>

        ... //其他列表样式
    tyle>

    AppTheme是应用到Activity的主题
    listPopupWindowStyle 对应弹出层的主题样式
    dropDownListViewStyle 对应内含列表的主题样式，与普通ListView的定制方式一致

    <style name="V7.ListPopupWindow" parent="AppTheme">
        <item name="listPopupWindowStyle">@style/V7.ListPopupWindowStyle</item>
        <item name="dropDownListViewStyle">@style/V7.DropDownListViewStyle</item>
    </style>
```

### 代码调用

实现微信右上角弹出菜单，使用方式与PopupWindow差不多：

```java
    ListPopupWindow listPopupWindow = new ListPopupWindow(this);
    listPopupWindow.setAnchorView(view);
    listPopupWindow.setWidth(300); //如果不设置宽度的话，默认取AnchorView的宽度，一般不是我们想要的结果
    listPopupWindow.setModal(true); //是否为模态，影响到对back按钮的处理
    listPopupWindow.setAdapter(new ArrayAdapter<String>(this, R.layout.apt_v7_list_popup_window, R.id.apt_v7_tv, new String[]{
            "发起群聊",
            "添加朋友",
            "扫一扫",
            "意见反馈"
    }));
    listPopupWindow.show();
```

## 与PopMenu的对比

1. PopMenu难以定制，ListPopupWindow的定制性更好
2. ListPopupWindow不能自适应宽度
3. PopMenu以面向菜单为核心，可以更方便的实现 禁用/开启 功能

一个让ListPopupWindow自适应宽度的方案，设置adapter后，检测每一行的最大宽度，然后再来设置 ListPopupWindow 的宽度，有利有弊，自己取舍了。


关于菜单那的其他实现方式：

1. PopMenu
2. PopupWindow + 自定义ContentView
3. 页面内View + 自定义touch事件以及按键事件处理

## demo
[demo](http://git.oschina.net/xesam/AndroidLollipop)
