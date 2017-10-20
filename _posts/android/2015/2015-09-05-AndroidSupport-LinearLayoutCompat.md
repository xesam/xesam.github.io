---
layout: post
title:  "【AndroidSupport】LinearLayoutCompat"
date:   2015-09-05 12:46:04 +0800
categories: android
tag: [android]
---

LinearLayoutCompat 所在位置 android.support.v7.widget.LinearLayoutCompat

## 主要特性:
1. 支持分割线

## 注意
2.3 中使用xml定义drawable的时候有bug,所以在2.3 下最好还是使用图片作为分隔符

## 使用

定义分割线 /drawable/linearlayout_compat_divider.xml

    <?xml version="1.0" encoding="utf-8"?>
    <shape xmlns:android="http://schemas.android.com/apk/res/android">
        <solid android:color="#000000" />
        <size android:width="5dp" />
    </shape>

定义layout

    <android.support.v7.widget.LinearLayoutCompat xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:app="http://schemas.android.com/apk/res-auto"
        xmlns:tools="http://schemas.android.com/tools"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="horizontal"
        app:divider="@drawable/linearlayout_compat_divider"
        app:dividerPadding="10dp"
        app:showDividers="middle"
        tools:context="dev.xesam.android.support.v7.widget.LinearLayoutCompatDemo">

        <TextView
            android:layout_width="0dp"
            android:layout_height="match_parent"
            android:layout_weight="1.0"
            android:background="#ff0000"
            android:gravity="center"
            android:text="@string/hello_blank_fragment" />

        <TextView
            android:layout_width="0dp"
            android:layout_height="match_parent"
            android:layout_weight="1.0"
            android:background="#00ff00"
            android:gravity="center"
            android:text="@string/hello_blank_fragment" />

        <TextView
            android:layout_width="0dp"
            android:layout_height="match_parent"
            android:layout_weight="1.0"
            android:background="#0000ff"
            android:gravity="center"
            android:text="@string/hello_blank_fragment" />

    </android.support.v7.widget.LinearLayoutCompat>

## 效果

![输入图片说明](https://static.oschina.net/uploads/img/201509/05204957_GSvE.png "在这里输入图片标题")
