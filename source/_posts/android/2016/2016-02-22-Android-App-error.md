---
layout: post
title:  "App错误记录"
date:   2016-02-22 13:46:04 +0800
categories: android
tag: [android]
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

```java
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
```

这里有个详细的说明：

[http://www.cnblogs.com/kissazi2/p/4181093.html](http://www.cnblogs.com/kissazi2/p/4181093.html)

## 3. 同样 Can not perform this action after onSaveInstanceState

注意 ： onBackPressed() 与 finish() 的区别

finish() 这个方法比较纯粹，触发 Activity 生命周期中的 onDestroy 方法。

onBackPressed() 是在 Fragment 引入之后才新增加的方法，所以，onBackPressed() 相比 finish() 会先处理各种 Fragment 的状态。
这样问题就来了，假如按下 Home 键将当前 Activity 放到后台，这个时候某个调用触发 onBackPressed()，会进行状态清理，但是由于此时已经调用了 onSaveInstanceState，
所有涉及到 Fragment 的操作都会导致崩溃。由于 onBackPressed() 是默认方法，除非重写，不然也办法使用 commitAllowingStateLoss() 方法。

## 4. Java IOException  App:transformClassesWithDexForApp_wandoujiaStage

这个错误出现在用 gradle 命令行打包的时候。

我遇到的一个原因就是在 Mac 上修改了类的位置之后，各个模块下的 build 文件没有 clean。

当用命令行来编译的时候，就会报 IOException 的错误。

解决方案：

先在工程根目录调用一下 

```shell
    gradle clean
```

然后再正常编译就行。

## 5. values 语言不完整

一个真实的错误，错误原因：

    res
    |
    |----values :
    |    | 
    |    |----<null> //这里丢失了 cll_update_strings.xml 
    |    |    
    |----values-zh : 
    |    |    
    |    |----cll_update_strings.xml
    
    
如果将系统调成英文，那么会直接报错。

如何预防：

1. 保证 values 的完备！
2. 启动更严厉的 IDE 和 打包时检查

## 6. drawable 资源不完整

当前手机屏幕分辨率为 normal, 如果只在 drawable-normal 放有 xxx.png 资源文件，那么会崩溃。
因为 Android 如果找不到最佳匹配的资源图片，只会向更低级的进行查找，而不会向更高级的进行查找。

## 7. Execution failed for task ':xxx:transformClassesAndResourcesWithProguardForRelease'.

一般是因为 Proguard 配置错误或者不全

## android.view.GLES20Canvas.clipPath

低版本开启硬件加速导致的 2D 绘图问题，参见官网文档：[https://developer.android.com/guide/topics/graphics/hardware-accel.html#unsupported](https://developer.android.com/guide/topics/graphics/hardware-accel.html#unsupported)

不过虽然官网说从 API 18 开始就恢复支持了，但是我在 4.4 以及 5.0 版本上都看到过此类崩溃，待调查。。


####Android分享 Q群：315658668
