---
layout: post
title:  "【Android】Apk错误记录"
date:   2016-02-22 13:46:04 +0800
categories: android
---

#### 1. INSTALL_PARSE_FAILED_NO_CERTIFICATE

解决方法：在签名时，添加参数 

    -digestalg SHA1 -sigalg MD5withRSA
  
示例如下：

    jarsigner -digestalg SHA1 -sigalg MD5withRSA -keystore my_keystore -signedjar $signed_apk $unsign_apk my_alias_name

#### 2. AppCompat does not support the current 

最新的Surpport里面的主题检查好像更严格了。以前使用

ActionBarActivity + Toolbar 

的时候，我是这么定义的

```xml
    <style name="AppTheme.Base" parent="Theme.AppCompat.Light">
            <item name="android:windowNoTitle">true</item>
            <item name="windowActionBar">false</item>
    </style>
```

升级之后就出问题了。应该使用

```xml
    <style name="AppTheme.Base" parent="Theme.AppCompat.Light">
            <item name="windowNoTitle">true</item>
            <item name="windowActionBar">false</item>
    </style>
```

其实最好的方法还是，不管在哪里，都使用sdk预置的主题：

```xml
    <style name="AppTheme.Base" parent="Theme.AppCompat.Light.NoActionBar">
    </style>
```

其他问题类似

####Android分享 Q群：315658668