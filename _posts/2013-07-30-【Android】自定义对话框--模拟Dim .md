---
layout: post
title:  "【Android】自定义对话框--模拟Dim"
date:   2013-07-30 12:46:04 +0800
categories: android
---
##背景

Android 在弹出 Dialog 的时候,默认在 dialog 背后会产生办透明的模糊效果(backgroundDim).这个dim层可以调整模糊值:

```xml
<item name="android:backgroundDimEnabled">true</item><!-- 开启背景模糊 -->
<item name="android:backgroundDimAmount">0.5</item><!-- 背景模糊值 -->
```

现在的问题是要改变此dim层的颜色,我没有找到修改这个dim color 的方法,因此只能弄点偏门了.

## 解决办法:

将对话框覆盖整个activity,然后自定义背景.

```java
class MockDimDialog extends Dialog{
	
	public MockDimDialog(Context context) {
		super(context, R.style.MockDimDialog);
		setContentView(R.layout.sample_segment_dialog);
		WindowManager.LayoutParams wlp = getWindow().getAttributes();
		wlp.width = WindowManager.LayoutParams.MATCH_PARENT;
		wlp.height = WindowManager.LayoutParams.MATCH_PARENT;
		//下面两行用来保留status bar,不然就全屏了
		wlp.gravity = Gravity.TOP;
		wlp.y = 1;
		getWindow().setAttributes(wlp);
	}
}
```

样式:

```xml
    <style name="MockDimDialog" parent="android:Theme.Dialog">
        <item name="android:windowNoTitle">true</item>
        <item name="android:backgroundDimEnabled">false</item>
        <item name="android:windowBackground">@color/dim</item>
    </style>
    <color name="dim">#55ff6600</color>
```

自定义的dialog view:

```java
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical" >

    <ProgressBar
        style="@android:style/Widget.ProgressBar"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="4dip"
        android:textSize="20dip"
        android:textColor="#707070"
        android:text="Loading..." />

</LinearLayout>
```

## 显示效果:

![1](http://static.oschina.net/uploads/space/2013/0730/095642_ZMnX_93688.png)

