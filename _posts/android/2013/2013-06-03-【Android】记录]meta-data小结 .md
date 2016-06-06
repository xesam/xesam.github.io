---
layout: post
title:  "【Android】meta-data小结"
date:   2013-06-03 12:46:04 +0800
categories: android
tag: [android]
---
# 【Android】meta-data小结

## 概念

meta-data就像其名一样，主要用来定义一些组件相关的配置值。

按照官方定义，metadata是一组供父组件使用的名值对（name-value pair），因此相应的meta-data元素应该定义在相应的组件中。
即如果想在activity中使用metadata，那么meta-data必须定义在AndroidManifest.xml的activity声明中。

## 使用

所有的名值对被包装成Bundle供组件使用，因此使用方式同Bundle。metadata普通值由value属性给出，资源ID由resource属性给出。比如我们定义资源:

```xml
<string name="x_key">resource key</string>
```
//R

```java
public static final int ic_launcher=0x7f020000;
```

定义metadata

```xml
<meta-data
    android:name="com.xesam.key_1"
    android:value="x_key" />
<meta-data
    android:name="com.xesam.key_2"
    android:value="@string/x_key" />
<meta-data
    android:name="com.xesam.img"
    android:resource="@drawable/ic_launcher" />
```

那么有：

	metadata.getString("com.xesam.key_1") ==> "x_key"
	metadata.getString("com.xesam.key_2") ==> "resource key"
	metadata.getInt("com.xesam.img")      ==> 0x7f020000
	
由于resource指向资源ID，因此用metadata可以定义一些稍微复杂的值。 

比如要定义一副图片，则可以用这个，然后在代码中用getInt()取出图片的ID：

```java
int imageId = meta.getInt("com.xesam.img");
((ImageView) findViewById(R.id.img)).setImageResource(imageId);
```

### 使用问题

形如：

```xml
<meta-data
    android:name="com.xesam.key_1"
    android:value="000" />
```

类似这样的值如果使用bundle.getString()的话是不起作用的，因为Bundle中使用的是形如： 

```java
return (String) o;
```

的代码获取一个StringValue值的，但是在将metadata包装成bundle的时候，"000"被解析成整数0， 
因此bundle.getString("com.xesam.key_1")返回的是(String)0，显然，java是不允许这样的，因此最后得到的是null。 话说android为什么不是用String.valueOf()或者obj.toString()呢？
为了避免这种情况：
1，可以在形如000的字符串前面放个\0空字符，强迫android按照字符串解析000。
2，在资源文件中指定需要的值，然后在metadata的value中引用此值。

示例代码

附：

//在Activity应用<meta-data>元素。
```java
    ActivityInfo info = this.getPackageManager()
            .getActivityInfo(getComponentName(),PackageManager.GET_META_DATA);
    info.metaData.getString("meta_name");

    //在application应用<meta-data>元素。
    ApplicationInfo appInfo = this.getPackageManager()
            .getApplicationInfo(getPackageName(),PackageManager.GET_META_DATA);
    appInfo.metaData.getString("meta_name");

    //在service应用<meta-data>元素。
    ComponentName cn = new ComponentName(this, MetaDataService.class);
    ServiceInfo info = this.getPackageManager().getServiceInfo(cn, PackageManager.GET_META_DATA);
    info.metaData.getString("meta_name");

    //在receiver应用<meta-data>元素。
    ComponentName cn = new ComponentName(context, MetaDataReceiver.class);
    ActivityInfo info = context.getPackageManager().getReceiverInfo(cn, PackageManager.GET_META_DATA);
    info.metaData.getString("meta_name");
```

meta-data官方地址 [http://developer.android.com/reference/android/os/Bundle.html](http://developer.android.com/reference/android/os/Bundle.html)
