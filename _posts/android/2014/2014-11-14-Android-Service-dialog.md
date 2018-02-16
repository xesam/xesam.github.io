---
layout: post
title:  "Android 从service调用dialog"
date:   2014-11-14 12:46:04 +0800
categories: android
tag: [android]
---
## 需要权限

```xml
    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
```

##  示例代码

```java
    Dialog dialog = new AlertDialog.Builder(ctx).create();
    dialog.getWindow().setType(WindowManager.LayoutParams.TYPE_SYSTEM_ALERT);
    dialog.show();
```

## 注意事项

当activity不在前台的时候，部分手机（比如小米2s，系统4.1.1）不支持直接弹出dialog，之后在显示activity之后，才会看到dialog。
