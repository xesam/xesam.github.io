---
layout: post
title:  "Edit-TextWatcher"
date:   2018-01-01 08:00:00 +0800
categories: android
tag: [android]
---

Something about EditText's TextWatcher.

<!-- more -->

```java

public interface TextWatcher extends NoCopySpan {
    /**
    * sequence: 文本框发生修改之前的文本
    * start: sequence 即将被修改区域的起始位置
    * count: sequence 即将被修改区域的字符数目
    * after: 用来替换原文本被修改区域的新文本长度
    * 
    * 即 sequence 的 [start, start + count) 区域即将被修改为一串长度为 after 的新文本
    * 这个回调在文本内容应用修改前触发，此回调内不应使用 setText 方法修改当前文本框的内容。
    */
    public void beforeTextChanged(CharSequence sequence, int start, int count, int after);

    /**
    * sequence: 文本框发生修改之后的文本
    * start: 对应于 beforeTextChanged 方法的 start 参数
    * before: 对应于 beforeTextChanged 方法的 count 参数
    * count: 对应于 beforeTextChanged 方法的 after 参数
    * 
    * 即 sequence 的 [start, start + count) 区域被修改之前是一串长度为 before 的旧文本
    * 这个回调在文本内容应用修改的时候触发，此回调内不应使用 setText 方法修改当前文本框的内容。
    */
    public void onTextChanged(CharSequence sequence, int start, int before, int count);

    /**
    * sequence: 文本框发生修改生效之后的文本
    * 
    * 可以在这个方法中使用 setText 来修改文本框中的文本，每一次修改都会再次触发 TextWatcher 的三个回调，因此需要谨慎避免陷入无限循环。
    */
    public void afterTextChanged(Editable sequence);
}

```

综合这三个方法，可以获取文本修改的各个部分：

beforeTextChanged 方法：

```java
    sequence.subSequence(0,start); //修改区域之前的内容
    sequence.subSequence(start, start+count); //修改区域的旧内容
    sequence.subSequence(start+count, sequence.length()); //修改区域之后的内容
```

```java
    sequence.subSequence(start, start+count); //修改区域的新内容
```
