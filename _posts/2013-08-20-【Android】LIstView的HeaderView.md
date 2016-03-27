---
layout: post
title:  "【Android】LIstView的HeaderView"
date:   2013-08-20 13:46:04 +0800
categories: android
---
# 【Android】LIstView的HeaderView

## 一，添加HeaderView之后尺寸布局被忽略。

通常添加头部的方法是 

```java
LayoutInflater lif = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
View headerView = lif.inflate(R.layout.header, null);
mListView.addHeaderView(headerView);
```

原因： 

lif.inflate(R.layout.header, null)丢失了XML布局中根View的LayoutParam，应该使用的是 

```java
lif.inflate(R.layout.header, mListView, false);
```

## 二，添加HeaderView之后导致OnItemClickListener的position移位

OnItemClickListener接口的方法： 

```java
void onItemClick(AdapterView<?> parent, View view, int position, long id)
```

position通常是从0开始的，但是添加了HeaderView之后，position也会将HeaderView的数目计算进去。 

几个解决办法： 

1,手动计算真实的position位置： 

```java
final headerCount = 1;
mListView.setOnItemClickListener(new OnItemClickListener() {
	@Override
	public void onItemClick(AdapterView<?> parent, View view,
			int position, long id) {
		Item item = myAdapter.getItem(position - headerCount);
	}
});
```

2,其实上面的步骤ListView已经为我们提供了，所以可以改写为：
 
```java
mListView.setOnItemClickListener(new OnItemClickListener() {
	@Override
	public void onItemClick(AdapterView<?> parent, View view,
			int position, long id) {
		Item item = parent.getAdapter().getItem(position);
	}
});
```

原因在源码中有比较清晰的解释： 

当有headerView被添加时，实际传递给ListView的adapter被包装，parent.getAdapter()返回真实被 ListView 使用的 Adapter（HeaderViewListAdapter），HeaderViewListAdapter的getItem(int)方法处理了position的问题。 

## 三，LayoutInflater的infalte()

用来呼应第一个问题。LayoutInflater的作用很简单，就是将XML的布局文件“翻译”成相应的View对象，而且出于性能的考虑，LayoutInflater只能处理编译后的XML文件，而不能处理通常明文编码的XML文件。 
最常用的一个方法： 

```java
View inflate(int resource, ViewGroup root, boolean attachToRoot)
```

其中： 

    resource是布局文件ID 
    root是父ViewGroup对象， 
    attachToRoot是是否将“翻译”出来的View添加到上面的root中 

root和attachToRoot是共同作用的： 

1. 有root，同时attachToRoot为false，那么inflate()返回的就是“翻译”得到的view 
2. 有root，同时attachToRoot为true，那么inflate()就是将“翻译”得到的view添加到root后，然后返回root 
3. 无root，同时attachToRoot为false，那么inflate()返回的就是“翻译”得到的view。 
4. 无root，同时attachToRoot为true，报错。 

另外，root还有一个重要的作用就是为“翻译”得到的view添加合适的LayoutParam，并且如果并不想将得到的View添加到root的话，传递何种root是并没有要求的，比如： 

```java
View view = mLayoutInflater.inflate(R.layout.header, new ListView(mContext), false);
View view = mLayoutInflater.inflate(R.layout.header, new LinearLayout(mContext), false);
View view = mLayoutInflater.inflate(R.layout.header, new RelativeLayout(mContext), false);
```

上面得到的View，除了view的LayoutParam分别为AbsListView.LayoutParams，LinearLayout.LayoutParams，RelativeLayout.LayoutParams之外，内容都一致。 

