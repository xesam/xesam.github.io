---
layout: post
title:  "【Android】自定义ADT模板"
date:   2013-07-11 12:46:04 +0800
categories: android
tag: [android]
---
## 简介

ADT模板就是在Eclipse中使用向导新建Android工程或者Android组件的时候使用的模板。ADT模板的特点：

1. 可以通过简单的可视化配置[后面称之为UI parameters]来生成Android代码和资源样本
2. 集成到Eclipse ADT中
3. FreeMarker驱动

## Android的默认模板

SDK下载完成之后，一般自带了一部分模板，模板的位置为：

    $your_android_sdk_dir/tools/templates

模板的类型有： 

1. Android Application Templates 
这个模板是使用Eclipse的新建Android工程向导[包括Android project，lib project和test project]时使用的模板类型 
2. Android Activity Templates 
这个显然就是使用Eclipse的新建Android Activity向导时使用的模板类型 
3. Android Object Templates 
这个就是创建其他一些android组件向导时使用的一些模板[File -> New -> Other -> Android/Android Object 可以打开此类向导]

## Activity示例

打开新建Android Activity向导，ADT插件首先就会列出一些可选模板让我们选择，如下：

![1](http://static.oschina.net/uploads/space/2013/0711/104913_6mBB_93688.png)

我们再打开 $your_android_sdk_dir/tools/templates/activities 文件夹，会发现正好和向导的选择一一对应，不过要指出的是，模板文件夹的名字并不是模板的名字，这里只是恰好一样而已。
至于其他的Application Templates和Object Templates的基本情况都是一样的。

## 模板的工作流程

![2](http://static.oschina.net/uploads/space/2013/0711/103344_TJJ9_93688.png)

## 模板的具体构成

下面结合Activity模板来稍微说明下。开始之前，除了必要的Eclipse + ADT plugin + Android SDK，我们需要一个辅助工具——FreeMarker IDE 
FreeMarker IDE是个eclipse的插件，安装过程在FreeMarker的官网有介绍。 

官方提供的模板就是最好的资料，为了避免破坏原有的模板，我们新建一个模板工程： 
File -> New ->  Project -> General/Project: 
把新工程Xe_CustomActivity建立在了SDK的templates里面，然后将BlankActivity文件夹中的内容拷贝到新工程里面，这样就可以在eclipse里面直接使用了。 

![3](http://static.oschina.net/uploads/space/2013/0711/103605_lhLb_93688.png)

我们重复一下上面的使用向导创建Activity的步骤，会发现有两个BlankActivity，其中一个是SDK自带的，一个是我们刚才创建的，这里再次表明文件夹的名字和模板名字是两码事。 
 
![4](http://static.oschina.net/uploads/space/2013/0711/104934_zf4y_93688.png)

我们查看一下新工程的大致目录结构： 

    project_name:
    ...root
    ......AndroidManifest.xml.ftl
    ......res
    .........layout
    ............*.ftl/*.*
    ......src
    .........app_package
    ............*.ftl/*.*
    ...template.xml
    ...recipe.xml.ftl
    ...globals.xml.ftl
    ...*.png

附带说明：.ftl表示FreeMarker模板语言

## 文件说明

template.xml

可以说是模板的模板，定义了模板的流 程框架 基本结构：

```xml
<?xml version="1.0"?>
<template
    format="3"
    revision="2"
    name="Blank Activity" <!-- 在向导中显示的模板名称 -->
    description="Creates a new blank activity, with an action bar and optional navigational elements such as tabs or horizontal swipe.">
    <dependency name="android-support-v4" revision="8" />
    <category value="Activities" /> <!-- 模板类型 -->
    <parameter
        id="activityClass" <!-- 参数名，在ftl文件中可以用${activityClass}获取参数值 -->
        name="Activity Name" <!-- UI 界面输入框前的提示标签值 -->
        type="string" <!-- 参数值类型 -->
        constraints="class|unique|nonempty" <!-- 参数值约束条件，这里的约束是必须是类名，唯一，非空 -->
        suggest="${layoutToActivity(layoutName)}" <!-- 自动提示，比如输入layout的值可以自动生成activityClass -->
        default="MainActivity" <!--默认值 -->
        help="The name of the activity class to create" /> <!-- 向导对话框底部的帮助性文字 -->
    <thumbs>
        <thumb>template_blank_activity.png</thumb>
        <thumb navType="none">template_blank_activity.png</thumb>
        <thumb navType="tabs">template_blank_activity_tabs.png</thumb>
        <thumb navType="tabs_pager">template_blank_activity_tabs_pager.png</thumb>
        <thumb navType="pager_strip">template_blank_activity_pager.png</thumb>
        <thumb navType="dropdown">template_blank_activity_dropdown.png</thumb>
    </thumbs>

    <globals file="globals.xml.ftl" />
    <execute file="recipe.xml.ftl" />

</template>

```

## 几个重要的节点：

category节点：表示模板的类型，可选的值包括三种：

1. Applications表示Android Application Templates
2. Activities表示Android Activities Templates
3. UI Component表示Android Object Templates中那些带有试图的UI组件模板，所以类似Service这种没有界面的组件模板中就没有这个节点了。

#### parameter节点：定义了图形配置界面的用户输入参数项。

参数类型由parameter节点的type属性定义，常见的类型有：
string——表现为输入框
boolean——表现为勾选框
enum——表现为下拉选择框

#### thumbs节点：定义了静态预览图。

对照Activity向导可以很容易的知道各个节点的意思：

![6](http://static.oschina.net/uploads/space/2013/0711/103850_AVId_93688.png)

<globals file="globals.xml.ftl" />就是将工程定义的全局变量包含进来。

<execute file="recipe.xml.ftl" />表示开始执行模板渲染。

因此，template.xml的结构和作用可以描述为：

![7](http://static.oschina.net/uploads/space/2013/0711/104259_jGWX_93688.png)

#### globals.xml.ftl

这个文件的目的只有一个，就是提供全局变量[Global Values]，简单示例：

    <global id="resOut" value="res" />
    <global id="menuName" value="${classToResource(activityClass)}" />

其他文件中的引用方式就是${resOut}以及${menuName}等等 

#### recipe.xml.ftl 

菜单模板，名字挺形象的，定义流程执行的步骤，一个典型的recipe.xml.ftl文件：

```xml
<?xml version="1.0"?>
<recipe>
    <merge from="AndroidManifest.xml.ftl" />

    <copy from="res/values-v14/styles_ics.xml"
            to="res/values-v14/styles.xml" />

    <instantiate from="res/menu/main.xml.ftl"
            to="res/menu/${menuName}.xml" />

    <open file="res/layout/${layoutName}.xml" />
</recipe>
```

可以看到recipe.xml.ftl使用了许多变量[后文称之为模板变量]，那么这些变量来自那些地方呢？主要来自两个方面： 

1. UI Parameters 
2. Global Values 

## 模板变量数据流向

![8](http://static.oschina.net/uploads/space/2013/0711/104451_SudQ_93688.png)
 
## 定制化自己的ADT模板，简单上手

1. 我们将所有的模板帮助提示都改成中文，在template.xml文件中，主要是修改description的属性值：

```xml
<parameter
    id="activityClass"
    name="Activity名称"
    type="string"
    constraints="class|unique|nonempty"
    suggest="${layoutToActivity(layoutName)}"
    default="MainActivity"
    help="Activity的类名" />
```
        
2. 一般我不会直接使用android默认的titlebar，而会自己定义一个TextView来定制title,因此我希望在向导中添加一个Page Title配置项，在template.xml添加下面的内容： 

```xml
    <parameter
        id="pageTitle"
        name="My Page Title"
        type="string"
        constraints="nonempty"
        default="默认标题"
        suggest="${activityClass}_page_title"
        help="自定义页面的标题" />
```

![9](http://static.oschina.net/uploads/space/2013/0711/110152_2RiN_93688.png)

在默认的activity布局文件[可以是root/res/layout/activity_simple.xml.ftl]中添加一个TextView 

```xml
    <TextView
    	android:background="#ff5500"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="${pageTitle}" />
```

3.app中会引用其他的一些库，这些库通常也会带有很多activity布局文件，为了和自己的布局文件去分开，所以我通常在自己的布局文件前面添加一个前缀，可以这么修改： 

    1. 定义一个前缀全局变量 
    2. 分别在template.xml和recipe.xml.ftl修改相应的名称

#### globals.xml.ftl

```xml
<global id="xe_prefix" value="xe" />
recipe.xml.ftl： 
<instantiate from="res/menu/main.xml.ftl"
    to="${resOut}/menu/${xe_prefix}_${menuName}.xml" />
<instantiate from="res/layout/activity_simple.xml.ftl"
    to="${resOut}/layout/${xe_prefix}_${layoutName}.xml" />
```

root/src/app_package/SimpleActivity.java.ftl: 

```java
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.${xe_prefix}_${layoutName});
        <#if parentActivityClass != "">
        // Show the Up button in the action bar.
        setupActionBar();
        </#if>
    }
```
    
附录

1. classToResource等方法定义在ADT插件中，具体源码： 
[https://android.googlesource.com/platform/sdk/+/7dd444ea0125e50a5e88604afb6de43e80b7c270/eclipse/plugins/com.android.ide.eclipse.adt/src/com/android/ide/eclipse/adt ](https://android.googlesource.com/platform/sdk/+/7dd444ea0125e50a5e88604afb6de43e80b7c270/eclipse/plugins/com.android.ide.eclipse.adt/src/com/android/ide/eclipse/adt )
2. FreeMarker参考 [http://freemarker.org/index.html](http://freemarker.org/index.html) ，
中文文档： [http://jaist.dl.sourceforge.net/project/freemarker/chinese-manual/FreeMarker_Manual_zh_CN.pdf](http://jaist.dl.sourceforge.net/project/freemarker/chinese-manual/FreeMarker_Manual_zh_CN.pdf) 
参考 [《Custom Android Code Templates》](http://es.droidcon.com/wp-content/uploads/2012/12/Custom-Android-Code-Templates.pdf)
