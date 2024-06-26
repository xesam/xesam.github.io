---
layout: post
title:  "Android 多语言切换"
date:   2016-08-04 08:00:00 +0800
categories: android
tag: [android]
---

这里的多语言切换专指应用内的多语言切换，不涉及直接通过应用修改系统语言设置的功能。比如微信里面的

    我 -> 设置 -> 通用 -> 多语言

举个例子，假如 App 支持简体和繁体两种设置，默认界面为“中文简体”。

    如果用户选择“中文简体”，那么展示简体界面；
    如果用户选择“中文繁体”，那么展示繁体界面；
    如果用户选择“跟随系统”，那么如果系统语言设置是“中文简体”，则展示简体界面，如果系统语言设置是“中文繁体”，则展示繁体界面，
    如果系统语言设置是“English(US)”，则展示默认界面，即简体界面。

上文描述功能的流程图大致如下：

![android_push](/image/android_change_language_1.png)

另外，在 App 运行过程中，用户如果在系统的设置里面切换语言，同样会提示应用“语言设置”发生变化，因此，多一个流程图：

![android_push](/image/android_change_language_2.png)

此图与前一个图的区别就是，如果用户没有选择“跟随系统”，那么，来自系统的设置就被忽略掉。

现在需要处理的问题如下：

1. 如何获取应用内语言设置
2. 如何获取系统语言设置
3. 如何更改应用的语言设置

## 1. 如何获取应用内语言设置

这个问题比较好处理，在 SharedPreference 内保存用户的语言设置即可。

```java
class UserLocale{
    public static final int FOLLOW_SYSTEM = 0;//跟随系统
    public static final int SIMPLIFIED_CHINESE = 1; //简体中文
    public static final int TRADITIONAL_CHINESE = 2; //繁体中文

    //获取用户设置
    public int getUserLocale(){
        //...
    }
}
```

## 2. 如何获取系统语言设置
第一种：

```java
Locale.getDefault()
```
这是从 Java 来的方法，可以通过 Locale.setDefault(Locale) 来修改。
不过这个方法有时候会出现莫名其妙的问题，比如一会儿返回系统语言 “zn_CN”，一会儿就返回 “en_US”，并不稳定。

第二种：

```java
context.getResources().getConfiguration().locale;
```
对于 Android N 来说，应该这样

```java
context.getResources().getConfiguration().getLocales().get(0);
```
这个返回的是当前 APP 的 Resource 对应的 Locale 设置。这个也可以通过代码来修改。后面“更新应用的语言设置”的时候就是通过更新 Configuration 来实现的。
同样，问题是我们肯定要修改 Configuration，一旦修改之后，这个操作就再也获取不到系统语言设置了。
如果一定要用这个，一个变通的方法就是在一开始就将 Configuration 保存下来，同时在以后每次系统语言设置有改动的时候，就同步更新一次即可。

第三种：

```
Resources.getSystem().getConfiguration().locale;
```
这个方法与上面的很像，不过这个返回的是系统全局 Resource 的 Locale，可以当做系统 Locale 来用。

## 3. 如何更改应用的语言设置

如上文所述，用户选定语言之后，要修改 APP 对应的 Configuration：

```java
    Locale targetLocale = getTargetLocale();
    Locale.setDefault(targetLocale);
    Resources resources = context.getResources();
    Configuration config = resources.getConfiguration();
    DisplayMetrics dm = resources.getDisplayMetrics();
    config.locale = targetLocale;
    resources.updateConfiguration(config, dm);

```

至于 getTargetLocale() 的实现：

```java
int getTargetLocale(){
    int userType = UserLocale.getUserLocale();
    if(userType == LanguageType.FOLLOW_SYSTEM){
        int sysType = getSysLocale();
        if(sysType == LanguageType.TRADITIONAL_CHINESE){
            return Locale.TRADITIONAL_CHINESE;
        }else{
            return Locale.SIMPLIFIED_CHINESE;
        }
    }else if(userType == LanguageType.TRADITIONAL_CHINESE){
        return Locale.TRADITIONAL_CHINESE;
    }else{
        return Locale.SIMPLIFIED_CHINESE;
    }
}
```
getSysLocale() 的实现参考 “2. 如何获取系统语言设置”。

触发语言切换的来源有两种：

1. 应用内切换语言设置
2. 系统切换语言设置

对于“应用内切换语言设置”来说，用户选择语言之后，需要手动重启所有的界面，为了方便，可以直接重启 Root Activity 并 Clear Top，这样方便快捷。

对于“系统切换语言设置”，默认情况下，如果我们的 APP 在后台运行，系统会主动重建所有的 Activity。我们可以在 Root Activity 监听

    Intent.ACTION_LOCALE_CHANGED

广播，在重启 Activity 之前修改 APP 全局的 Configuration。

如果对应的 Activity 设置了

```xml
android:configChanges="locale"
```
则可以直接在

```java
Activity.onConfigurationChanged(Configuration newConfig)
```
中响应 Configuration 的变化。如果无效，请参[《android:configChanges locale 改语言后，该配置不起作用的原因》](http://blog.sina.com.cn/s/blog_629712650101a1o3.html)
更详细的可以参考[《Android-语言设置流程分析》](http://blog.csdn.net/u013656135/article/details/50555391)

## 几个问题

1. RadioButton 或者 CheckBox 在重建之后没有更改语言。

这个问题应该存在于 5.0 之前的系统，问题原因可以参考[Not all items in the layout update properly when switching locales](https://stackoverflow.com/questions/4504024/android-localization-problem-not-all-items-in-the-layout-update-properly-when-s/16295141#16295141)

主要是 setFreezesText(true) 导致的，不过 5.0 之后好像就修复了这个问题，因为 Framework 中 CompoundButton 的源码有改动：

Android 4.1.1_r3：

```java
    @Override
    public Parcelable onSaveInstanceState() {
        setFreezesText(true);
        Parcelable superState = super.onSaveInstanceState();

        SavedState ss = new SavedState(superState);

        ss.checked = isChecked();
        return ss;
    }
```

Android 6.0：

```java
    @Override
    public Parcelable onSaveInstanceState() {
        Parcelable superState = super.onSaveInstanceState();

        SavedState ss = new SavedState(superState);

        ss.checked = isChecked();
        return ss;
    }
```
比不过其他版本源码还没翻，我不能太确认。
