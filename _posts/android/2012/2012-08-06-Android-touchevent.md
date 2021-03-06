---
layout: post
title:  "Android 触屏事件流"
date:   2012-08-06 13:46:04 +0800
categories: android
tag: [android]
---

本文请忽略，初学 Android 时的幼稚记录而已。

一次触屏事件分为三个动作

1. ACTION_DOWN
2. ACTION_MOVE
3. ACTION_UP

其中 ACTION_DOWN 和 ACTION_UP 在一次触屏事件中只会触发一次，ACTION_MOVE 可能触发任意次（包括0次）。

主要响应触屏的组件有两种，一种是可以包含子元素的（ViewGroup比如LinearLayout），另一种是不能包含子元素的View（最底层的View比如Button）。

当一个触屏事件产生时，正两者的响应方法有一个主要的区别就是LinearLayout有onInterceptTouchEvent方法，而Button没有onInterceptTouchEvent方法。

ViewGroup（比如LinearLayout）

```java
boolean dispatchTouchEvent(MotionEvent event)
boolean onInterceptTouchEvent(MotionEvent event)
boolean onTouchEvent(MotionEvent event)
```

View（比如Button）

```java
boolean dispatchTouchEvent(MotionEvent event)
boolean onTouchEvent(MotionEvent event)
```

总的来说，dispatchTouchEvent 决定处不处理，onInterceptTouchEvent 决定谁来处理，onTouchEvent 决定怎么处理。
所以对于Button来谁，没有小弟，自然不存在决定谁来处理的问题，故没有onInterceptTouchEvent方法

下面具体说一下这三个函数的主要作用：

### dispatchTouchEvent
dispatchTouchEvent 决定处不处理，看名字就知道是事件分发，初看我还以为是分发到子元素呢，原来不是直接到子元素。其实更好的理解是这是一个过滤方法。
此方法的主要作用是决定相应事件的类型。

假如dispatchTouchEvent 返回 false，那么在响应了 ACTION_DOWN 之后，后续的 ACTION_MOVE 和 ACTION_UP 均忽略，因此ACTION_MOVE和ACTION_UP永远不会有得到处理的机会。
假如dispatchTouchEvent 返回 true，那么后续的 ACTION_MOVE 和 ACTION_UP 均被接受，可以被其他方法响应。

特别注意，如果在这一步的dispatchTouchEvent中没有调用super.dispatchTouchEvent(event),那么事件就到此为止，被终结了。
此时此刻只有dispatchTouchEvent会响应事件，另外两个方法根本没有机会来响应事件。并且，事件不会传递到子元素中。

### onInterceptTouchEvent
onInterceptTouchEvent，主要决定谁来处理（即是否拦截事件）。

只要在dispatchTouchEvent中调用了super.dispatchTouchEvent(event)那么，事件(event)会被交给onInterceptTouchEvent去处理。
注意，这里事件(event)是否会调用onInterceptTouchEvent与dispatchTouchEvent的返回值是true还是false无关。
再次强调，dispatchTouchEvent只决定处理什么，并不能指定谁来调用。

假如onInterceptTouchEvent返回false，将事件(event)交自己的子元素处理（此时事件流是从外到内，从父元素到子元素）。

假如onInterceptTouchEvent返回true，将事件(event)交给自己的onTouchEvent来处理,并且如果有后续的 ACTION_MOVE 和 ACTION_UP（前一步dispatchTouchEvent中返回true）的话，将不再调用onInterceptTouchEvent，直接将事件传递给自己的onTouchEvent来处理。

### onTouchEvent
注意上一步，在 onInterceptTouchEvent 返回true的情况下，onTouchEvent 将获得事件并进行具体的处理。

假如 onTouchEvent 返回 false，将事件(event)交父元素处理，（注意在这一步，事件流反向了，此时事件流是从内到外，从子元素到父元素）。
假如 onTouchEvent 返回 true，本次事件(event)就到此为止，被终结了。

对照上面的说法，下面给出实例说明：

```java
public class MyLinearLayout1 extends LinearLayout{

	private String TAG = "第一层MyLinearLayout";
	
	public MyLinearLayout1(Context context) {
		super(context);
		this.setBackgroundColor(Color.WHITE);
	}
	public void setTagString(String tag){
		TAG = tag;
	}
	
	@Override
	public boolean dispatchTouchEvent(MotionEvent event){
		if(MotionEvent.ACTION_DOWN == event.getAction()){
			Log.v(TAG + "dispatchTouchEvent:", "ACTION_DOWN");
		}else if(MotionEvent.ACTION_MOVE == event.getAction()){
			Log.v(TAG + "dispatchTouchEvent:", "ACTION_MOVE");
		}else{
			Log.v(TAG + "dispatchTouchEvent:", "ACTION_UP");
		} //super.dispatchTouchEvent(event); return true;
	}

	@Override
	public boolean onInterceptTouchEvent(MotionEvent event){super.onInterceptTouchEvent

		if(MotionEvent.ACTION_DOWN == event.getAction()){
			Log.v(TAG + "onInterceptTouchEvent:", "ACTION_DOWN");
		}else if(MotionEvent.ACTION_MOVE == event.getAction()){
			Log.v(TAG + "onInterceptTouchEvent:", "ACTION_MOVE");
		}else{
			Log.v(TAG + "onInterceptTouchEvent:", "ACTION_UP");
		}
		return true;
	}
	
	@Override
	public boolean onTouchEvent(MotionEvent event){super.onTouchEvent(event)
		if(MotionEvent.ACTION_DOWN == event.getAction()){
			Log.v(TAG + "onTouchEvent:", "ACTION_DOWN");
		}else if(MotionEvent.ACTION_MOVE == event.getAction()){
			Log.v(TAG + "onTouchEvent:", "ACTION_MOVE");
		}else{
			Log.v(TAG + "onTouchEvent:", "ACTION_UP");
		}
		
		return true;
	}
}
```

此时没有调用super.dispatchTouchEvent(event)，所以事件没有机会得到其他的处理。

打印信息：

    第一层MyLinearLayoutdispatchTouchEvent:(460): ACTION_DOWN
    第一层MyLinearLayoutdispatchTouchEvent:(460): ACTION_UP
    如果将上面boolean dispatchTouchEvent(MotionEvent event)的返回值修改为false，那么按照前面说的，MyLinearLayout1在响应了ACTION_DOWN之后，不会再响应本次触屏操作的其他事件。所以此时的打印结果是：
    第一层MyLinearLayoutdispatchTouchEvent:(460): ACTION_DOWN

可以看到，ACTION_UP没有被响应，因为本事件被忽略了。

现在，将super.dispatchTouchEvent(event)的注释去掉，注意，现在的boolean dispatchTouchEvent(MotionEvent event)变成下面这样：

```java
	@Override
	public boolean dispatchTouchEvent(MotionEvent event){
		if(MotionEvent.ACTION_DOWN == event.getAction()){
			Log.v(TAG + "dispatchTouchEvent:", "ACTION_DOWN");
		}else if(MotionEvent.ACTION_MOVE == event.getAction()){
			Log.v(TAG + "dispatchTouchEvent:", "ACTION_MOVE");
		}else{
			Log.v(TAG + "dispatchTouchEvent:", "ACTION_UP");
		}

    super.dispatchTouchEvent(event);//去掉注释了

    return true;
}
```
打印信息：

    第一层MyLinearLayout ACTION_DOWN:(783): ACTION_DOWN
    第一层MyLinearLayout onInterceptTouchEvent:(783): ACTION_DOWN
    第一层MyLinearLayout onTouchEvent:(783): ACTION_DOWN
    第一层MyLinearLayout dispatchTouchEvent:(783): ACTION_UP
    第一层MyLinearLayout onTouchEvent:(783): ACTION_UP
    
具体顺序为下：

    ACTION_DOWN：ACTION_DOWN——>onInterceptTouchEvent——>onTouchEvent
    ACTION_UP：ACTION_DOWN——>onTouchEvent


