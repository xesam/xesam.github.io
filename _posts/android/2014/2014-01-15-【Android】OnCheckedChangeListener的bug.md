---
layout: post
title:  "【Android】OnCheckedChangeListener的bug"
date:   2014-01-15 12:46:04 +0800
categories: android
---

## 问题描述
RadioGroup.OnCheckedChangeListener 被回调两次

今天又碰到了，貌似还没有被修复，顺便贴出来。

原android Issue地址：[RadioGroup.OnCheckedChangeListener is called twice when the selection is cleared](https://code.google.com/p/android/issues/detail?id=4785)

## 具体表现

RadioGroup中包含有若干个RadioButton,当在代码中调用RadioGroup.check(id)方法动态设置被选中的RadioButton的时候，RadioGroup.OnCheckedChangeListener(RadioGroup group, int checkedId)会被调用多次。

## 示例

假设当前选择的是RadioButtonA,调用RadioGroup.check(RadioButtonBid)之后，RadioGroup.OnCheckedChangeListener(RadioGroup group, int checkedId)的调用情况如下：

第一次：checkedId 为 RadioButtonAId

第二次：checkedId 为 RadioButtonBId

第三次：checkedId 为 RadioButtonBId

## 测试代码

```java
public class MainActivity extends Activity implements CompoundButton.OnCheckedChangeListener,
RadioGroup.OnCheckedChangeListener{

	RadioGroup mRadioGroup;
	RadioButton radio_0;
	RadioButton radio_1;
	RadioButton radio_2;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		mRadioGroup = (RadioGroup) findViewById(R.id.group);
		radio_0 = (RadioButton) findViewById(R.id.radio_0);
		radio_1 = (RadioButton) findViewById(R.id.radio_1);
		radio_2 = (RadioButton) findViewById(R.id.radio_2);

		mRadioGroup.setOnCheckedChangeListener(this);
		radio_0.setOnCheckedChangeListener(this);
		radio_1.setOnCheckedChangeListener(this);
		radio_2.setOnCheckedChangeListener(this);
	}

	public void doTestClick(View view) {
		switch (view.getId()) {
		case R.id.check_radio_0:
			mRadioGroup.check(R.id.radio_0);
			break;
		case R.id.check_radio_1:
			mRadioGroup.check(R.id.radio_1);
			break;
		case R.id.check_radio_2:
			mRadioGroup.check(R.id.radio_2);
			break;

		default:
			break;
		}
	}

	@Override
	public void onCheckedChanged(RadioGroup group, int checkedId) {
		Log.i("mRadioGroup onCheckedChanged", "checkedId:" + checkedId);
	}
	
	@Override
	public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
		switch (buttonView.getId()) {
		case R.id.radio_0:
			Log.i("radio_0 onCheckedChanged", "isChecked:" + isChecked);
			break;
		case R.id.radio_1:
			Log.i("radio_1 onCheckedChanged", "isChecked:" + isChecked);
			break;
		case R.id.radio_2:
			Log.i("radio_2 onCheckedChanged", "isChecked:" + isChecked);
			break;

		default:
			break;
		}
	}

}
```

```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    tools:context=".MainActivity" >

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:orientation="vertical" >

        <Button
            android:id="@+id/check_radio_0"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:onClick="doTestClick"
            android:text="check_radio_0" />

        <Button
            android:id="@+id/check_radio_1"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:onClick="doTestClick"
            android:text="check_radio_1" />

        <Button
            android:id="@+id/check_radio_2"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:onClick="doTestClick"
            android:text="check_radio_2" />
    </LinearLayout>

    <RadioGroup
        android:id="@+id/group"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical" >

        <RadioButton
            android:id="@+id/radio_0"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="0" />

        <RadioButton
            android:id="@+id/radio_1"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="1" />

        <RadioButton
            android:id="@+id/radio_2"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="2" />
    </RadioGroup>

</LinearLayout>
```

## 产生原因

RadioGroup check简化如下：

```java
public void check(int newid) {
	setCheckedStateForView(mCheckedId, false); //这里取消原来选择的RadioButton
	setCheckedStateForView(newid, true);//设置当前选中的RadioButton为激活状态
	setCheckedId(newid);//触发OnCheckedChangeListener
}
```

RadioGroup setCheckedStateForView简化如下：

```java
private void setCheckedStateForView(int viewId, boolean checked) {
	RadioButton childRadioButton = (RadioButton)findViewById(viewId);
	childRadioButton.setChecked(checked);
}
```

RadioGroup setCheckedId简化如下：

```java
private void setCheckedId(int id) {
	mCheckedId = id;//保存当前选择的RadioButton
	mOnCheckedChangeListener.onCheckedChanged(this, mCheckedId);
}
```

同时RadioGroup内部有一个check状态跟踪器，简化一下如下：

```java
private class CheckedStateTracker implements CompoundButton.OnCheckedChangeListener {
	public void onCheckedChanged(CompoundButton childRadioButton, boolean isChecked) {
	    int childRadioButtonId = childRadioButton.getId();
	    setCheckedId(id);
	}
}
```

当每一个RadioButton被添加到RadioGroup的时候，就给每一个RadioButton设置一个checked状态监听

```java
childRadioButton.mOnCheckedChangeWidgetListener = mCheckedStateTracker;
```

所以每当RadioButton的check状态发生变化，都会触发check状态跟踪器。

RadioButton的setChecked(boolean)简化如下：

```java
public void setChecked(boolean checked) {
	mOnCheckedChangeListener.onCheckedChanged(this, mChecked); //触发RadioButton各自的监听
	mOnCheckedChangeWidgetListener.onCheckedChanged(this, mChecked);//触发check状态跟踪器
}
```

## 说明

所以结合开头的例子，调用RadioGroup.check(RadioButtonBid)之后发生的情况如下：
    
    1.RadioGroup.setCheckedStateForView(RadioButtonAid, false);
        --> RaidoButton.mOnCheckedChangeWidgetListener.onCheckedChanged(RadioButtonA, false) 
            --> RadioGroup.setCheckedId(RadioButtonAId) 
                --> RadioGroup.mOnCheckedChangeListener.onCheckedChanged(RadioGroup, RadioButtonAId);
    
    2.RadioGroup.setCheckedStateForView(RadioButtonBid, true);
        --> RaidoButton.mOnCheckedChangeWidgetListener.onCheckedChanged(RadioButtonB, true) 
            --> RadioGroup.setCheckedId(RadioButtonBId) 
                --> RadioGroup.mOnCheckedChangeListener.onCheckedChanged(RadioGroup, RadioButtonBId);
    
    3.RadioGroup.setCheckedId(RadioButtonBId) 
        --> RadioGroup.mOnCheckedChangeListener.onCheckedChanged(RadioGroup, RadioButtonBId);
    

按照Android官方文档的API说明：

    public abstract void onCheckedChanged (RadioGroup group, int checkedId)
    Parameters
        group	the group in which the checked radio button has changed
    checkedId	the unique identifier of the newly checked radio button


那个checkedId的参数在实现上是名不副实的。

