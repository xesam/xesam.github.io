---
layout: post
title:  "【Android】App错误记录"
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

### 3. Can not perform this action after onSaveInstanceState

比较常见的情况是 Activity 发起一个异步调用，然后 Activity 退到后台，异步调用返回之后，想弹出一个 Dialog 或者 DialogFragment，这个时候就会报

    Can not perform this action after onSaveInstanceState
    
原因就是 Activity 调用 onStop （有的版本是 onPause） 之前，先触发了 onSaveInstanceState。

解决方案：

如果是在 Fragment 里面弹出 Dialog，可以判断宿主 Fragment 的当前状态，比如：

```java
    if(fragment.isResumed()){
        dialog.show();
    }
```

如果是 Activity，需要自己来实现当前状态检测，比如：

    class BaseActivity extends Activity{
        boolean isResumed = false;
        @Override
        public void onResume(){
            super.onResume();
            isResumed = true;
        }
        @Override
        public void onPause(){
            super.onResume();
            isResumed = false;
        }
        @Override
        public void isResumed(){
            return isResumed;
        }
    }
    



这里有个详细的说明：

[http://www.cnblogs.com/kissazi2/p/4181093.html](http://www.cnblogs.com/kissazi2/p/4181093.html)



####Android分享 Q群：315658668