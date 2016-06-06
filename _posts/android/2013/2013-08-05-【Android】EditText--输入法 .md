---
layout: post
title:  "【Android】EditText--输入法"
date:   2013-08-05 12:46:04 +0800
categories: android
tag: [android]
---

## 1. 默认显示输入法的数字键盘,但是同时允许输入文本.

初始化的时候调用setRawInputType来设置输入法类型
EditText editText = (EditText) findViewById(R.id.x_edit_id);
edit.setRawInputType(EditorInfo.TYPE_CLASS_NUMBER);


## 2. 上接(1), 动态修改默认的输入法类型

修改方式参考(1),但是动态修改的之后需要重启一下InputMethodManager 
示例: 

```java
final EditText editText = (EditText) findViewById(R.id.x_edit_1);

findViewById(R.id.x_show_number).setOnClickListener(new OnClickListener() {
	
	@Override
	public void onClick(View v) {
		editText.setRawInputType(EditorInfo.TYPE_CLASS_NUMBER);
		InputMethodManager inputMethodManager=(InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
        if (inputMethodManager != null){
        	inputMethodManager.restartInput(editText);
        }
	}
});

findViewById(R.id.x_show_text).setOnClickListener(new OnClickListener() {
	
	@Override
	public void onClick(View v) {
		editText.setRawInputType(EditorInfo.TYPE_CLASS_TEXT);
		InputMethodManager inputMethodManager=(InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
        if (inputMethodManager != null){
        	inputMethodManager.restartInput(editText);
        }
	}
});
```

## 3.setRawInputType与setInputType的区别

setRawInputType只是修改输入法类型,不做其他的改动.  setInputType除了修改输入法类型外,还会修改KeyListener.
换句话说,就是setRawInputType修改输入法的类型,setInputType修改输入框的类型.

输入法面板的显示由输入法类型类型控制,内容的过滤由KeyListener控制.所以设置下面的调用是不同的: 

```java
edit.setRawInputType(EditorInfo.TYPE_CLASS_NUMBER)
```

只是设置输入法类型为数字类型,于是输入法面板会弹出数字面板.

```java
setInputType(EditorInfo.TYPE_CLASS_NUMBER)
```

除了设置输入法类型为数字类型,同时会将非数字的输入全部过滤掉,因此只能输入纯数字.

## 4.设置输入法面板类型

```java
EditText editText = (EditText) findViewById(R.id.x_edit_id);
editText.setRawInputType(Configuration.KEYBOARD_12KEY);
```

但是各输入法实现不是很标准,所以使用也不是非常可靠. 

    KEYBOARD_12KEY:设备有一个12键的物理键盘,就是以前功能机的那种数字键盘. 
    KEYBOARD_NOKEYS):设备有一个没有物理键盘. 
    KEYBOARD_QWERTY):设备有一个QWERTY键的物理键盘,比如Moto里程碑系列. 
    KEYBOARD_UNDEFINED):未定义 
