---
layout: post
title:  "【Android】修改菜单"
date:   2015-04-06 12:46:04 +0800
categories: android
tag: [android]
---
# 【Android】修改菜单

## 菜单的回调时机

常用的与菜单相关的主要有三个回调：

```java
    //创建菜单的时候调用
    public boolean onCreateOptionsMenu(Menu menu)；

    //显示菜单的时候调用
    public boolean onPrepareOptionsMenu(Menu menu)；

    //选择菜单项的时候调用
    public boolean onOptionsItemSelected(MenuItem item)；
```

## 修改view

因此，如果我们想自定义菜单的显示效果，应该在创建菜单项的时候去干预创建过程，但是这个过程并没有向开发者开放。
这种情况下，我们要么重新自定义整个菜单视图，要么在系统创建号之后，再去修改每一个菜单项。

对于后面一中情况，我们可以在onCreateOptionsMenu中对每一项进行修改，主要方法就是通过ActionView来模拟：

```java
    MenuItem.setActionView(actionView);

    或者

    MenuItemCompat.setActionView(menuItem, actionView);//兼容包
```

比如，替换成Textview：

```java
    TextView action = new TextView(this);
    action.setText(menuItem.getTitle());
    action.setOnClickListener(new View.OnClickListener() {

        @Override
        public void onClick(View v) {
            onOptionsItemSelected(menuItem);
        }
    });
    MenuItemCompat.setActionView(menuItem, action);
```

## 动态修改

有时候需要动态修改菜单，这个时候就需要分情况了，对于那些被收起来的菜单，可以在onPrepareOptionsMenu中进行动态增减，
因为onPrepareOptionsMenu会在每次菜单展示给用户的时候调用（比如点击ActionBar上的“更多”按钮）。

但是如果需要修改的菜单是一直展示在ActionBar或者Toolbar上面的话，可能触发修改菜单事件的时候，并不会涉及到onPrepareOptionsMenu，这个时候可以重新创建菜单,使用

```java
    Activity.invalidateOptionsMenu()

    或者

    ActionBarActivity.supportInvalidateOptionsMenu()//兼容包
```

来重新进入菜单流程。

## 演示图

![在此输入图片描述](http://static.oschina.net/uploads/space/2015/0406/210351_3vdX_93688.png)

## demo源码

[android_menu](http://git.oschina.net/xesam/AndroidLollipop/blob/master/archive/AndroidMenu.zip)
