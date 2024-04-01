---
layout: post
title:  "Android 导致notifyDataSetChanged无效的一个错误"
date:   2012-05-31 13:46:04 +0800
categories: android
tag: [android]
---

初学Android，发现有时候notifyDataSetChanged不起作用。后来发现是我理解错了。

一个典型的错误是：

```java
list1 = new String[]{"listView1 item"};
ap1 = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,list1);
listView1.setAdapter(ap1);
list1 = new String[]{"new listView1 item"};
ap1.notifyDataSetChanged();
```

我一直以为ap1会监听list1的变化，重新初始化list1，然后执行相应的更新，现在才知道不对，ap1监听的是new String[]{"listView1 item"}的变化。

换种说法就是ap1本身会保存一个对原始数据源（new String[]{"listView1 item"}）的内部引用inner_list1。

```java
　　list1 = new String[]{"new listView1 item"};
```
相当与切断了list1与原始数据源（new String[]{"listView1 item"}）的关系，因此之后调用notifyDataSetChanged并不会起作用，因为list1 和inner_list1已经是存在于堆上的完全不同的两个对象了

错误回顾：

前段时间都是使用的Arrayist等等作为原始数据源，一般都是进行add之类的操作，所以list1 和inner_list1和一直都是保持对同以个变量的引用，
并没有出什么问题，当然，改为直接赋值还是会出问题。

看了一下Arrayadapter的源码：

ArrayAdapter：

```java
public ArrayAdapter(Context context, int textViewResourceId, T[] objects) {
    init(context, textViewResourceId, 0, Arrays.asList(objects));
}
```
Arrays：

```java
public static <T> List<T> asList(T... array) {
    return new ArrayList<T>(array);//注意这里的ArrayList不是常见的那个ArrayList，而是Arrays的一个内部类。。
}
```
所以上面的问题可以归结为这么个问题：


```java
String[] a = new String[] {"hello","world"};
String[] b = a;
List c = Arrays.asList(a);
a = new String[] {"hello","xesam"};
System.out.println(c.toString());//["hello","world"]
b[1] = "xesam";
System.out.println(c.toString());//["hello","xesam"]
````

下面是一个demo：


```java
package com.xesam.demo.listview;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;

public class TestDemoActivity extends Activity {
    
    private Button   button1;
    private ListView listView1;
    private Button   button2;
    private ListView listView2;
    private Button   button3;
    private ListView listView3;
    
    private String[] list1;
    private String[] list2;
    private String[] list3;
    private String[] temp;
    
    ArrayAdapter<String> ap1;
    ArrayAdapter<String> ap2;
    ArrayAdapter<String> ap3;
    
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        button1   = (Button) findViewById(R.id.button1);
        listView1 = (ListView) findViewById(R.id.listview1);
        button2   = (Button) findViewById(R.id.button2);
        listView2 = (ListView) findViewById(R.id.listview2);
        button3   = (Button) findViewById(R.id.button3);
        listView3 = (ListView) findViewById(R.id.listview3);
        
        list1 = new String[]{"listView1 item"};
        list2 = new String[]{"listView2 item"};
        list3 = new String[]{"listView3 item"};
        temp = list3;
        
        ap1 = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,list1);
        ap2 = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,list2);
        ap3 = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,list3);
        
        listView1.setAdapter(ap1);
        listView2.setAdapter(ap2);
        listView3.setAdapter(ap3);
        
        button1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                list1 = new String[]{"new listView1 item"};
                ap1.notifyDataSetChanged();//无效
            }
        });
        button2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                list2[0] = "new listView2 item";
                ap2.notifyDataSetChanged();//有效
            }
        });
        button3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                temp[0] = "new listView3 item";
                ap3.notifyDataSetChanged();//有效
            }
        });
    }
}
```
