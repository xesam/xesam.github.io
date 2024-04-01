---
layout: post
title:  "Edit-InputFilter"
date:   2018-01-02 08:00:00 +0800
categories: android
tag: [android]
---

InputFilter 会在 TextWatcher 之前调用，可以在用户输入内容时就禁止用户输入一些非法字符。

<!-- more -->

```java
public interface InputFilter{
    /**
    * 即将使用 source[start, end - 1] 替换 dest[dstart, dend - 1]。
    * 通过返回值可以修改执行替换的部分，如果返回值是 null，则不进行任何干涉。
    */
    public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend);
}
```

官网的注释特别提醒了一句：

    If <var>source</var> is an instance of Spanned or Spannable, 
    the span objects in the <var>source</var> should be copied into the filtered result (i.e. the non-null return value). 
    TextUtils#copySpansFrom can be used for convenience if the span boundary indices would be remaining identical relative to the source.

如果 source 是 Spanned 或者 Spannable 的实例，如果需要进行替换，则在返回值的时候，应该复制 source 的内容，然后再复制的 source 上进行操作，最后返回被复制的 source。
这么处理的考虑是因为 source 本身可能存在一些样式，如果直接返回 CharSequence，会丢失原有的 span 样式。

### LengthFilter

InputFilter 有一个自带的长度过滤器：LengthFilter。EditText 的 android:maxLength="3" 属性就是通过 LengthFilter 产生效果的。

不过 LengthFilter 有一个令人误解的地方： LengthFilter 限制的是字符长度，而不是文字的长度。比如对于 LengthFilter 来说，“陶吉吉” 与 “陶𠮷” 的字符长度是一样的。

这其中涉及的是 UTF-16 的问题，因为 “𠮷” 的 Unicode 码点为 0x20BB7，UTF-16 编码为 0xD842 0xDFB7 ，字符长度是 2 。

LengthFilter 的实际处理：

```java

public static class LengthFilter implements InputFilter {

    //...

    public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {
        int keep = mMax - (dest.length() - (dend - dstart));
        if (keep <= 0) {
            return "";
        } else if (keep >= end - start) {
            return null; // keep original
        } else {
            keep += start;
            if (Character.isHighSurrogate(source.charAt(keep - 1))) {
                --keep;
                if (keep == start) {
                    return "";
                }
            }
            return source.subSequence(start, keep);
        }
    }

    //...

```

其中

```java

if (Character.isHighSurrogate(source.charAt(keep - 1))) {
    --keep;
    if (keep == start) {
        return "";
    }
}

```

是产生效果的部分，如果最后一个字符是某个文字的高位字符，直接就抛弃了。我们输入 “陶大𠮷” 的时候，source 的内容是

    \u9676\u5927\ud842\udfb7

参数值：

    CharSequence source, // 陶大𠮷
    int start, // 0
    int end, // 4
    Spanned dest, // ""
    int dstart, // 0
    int dend // 0

判断出 \ud842 属于 \ud842\udfb7 的高位，因此 \ud842\udfb7-“𠮷” 被整个丢弃了。

除了这些生僻汉字以外，emoji 表情也是占用两个字符。于是在一个 android:maxLength="3" 的输入框内，最多只能容纳一个 emoji 表情。这种限制可能不符合我们实际的需求，所以就需要自定义 InputFilter 来处理了。


### 参考 

1. [彻底弄懂 Unicode 编码](https://blog.whezh.com/encoded/)