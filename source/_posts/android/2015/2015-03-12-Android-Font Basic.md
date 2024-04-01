---
layout: post
title:  "Android Font Basic"
date:   2015-03-12 12:46:04 +0800
categories: android
tag: [android]
---
文字最终的大小是和绘制文字的字体的类型和字体的大小是相关的.

设置字体类型 Paint.setTypeface(Typeface typeface)

设置字体大小 Paint.setTextSize(float textSize)

## 几个相关的尺寸和方法

### Paint.FontMetrics
有5个属性,并且这5个属性都是跟字体相关的.

    top: 字体中字符超出基线之上的最大距离
    bottom: 字体中字符超出基线之下的最大距离
    ascent: 单个字符超出基线之上的推荐距离
    descent: 单个字符超出基线之上的推荐距离
    leading: 标准行间距

### Paint.getTextBounds

这个方法获取字符[字符串]占据的矩形区域,意为字体可见部分的矩形区域

```java
    Rect bound = new Rect();
    mPaint.getTextBounds(text, 0, text.length(), bound);

    bound.right - bound.left //得到的就是字符[字符串]的可见部分矩形区域的宽度
```

### Paint.measureText(text)

返回的是字符[字符串]的宽度,注意与

```java
    bound.right - bound.left
```

相互区分.

因为通常来说每个字符两边都会留有一部分空白区域,便于阅读.所以measureText的尺寸通常会大于bound.right - bound.left.所以,对于单个字符来说:

```java
    measureText = bound.right - bound.left + 字符两边的留白宽度
```

## 整体图示如下
![1](/image/android_font.png)

## 应用场景

1. 垂直居中的文字,计算基线位置使用FontMetrics比较方便.

2. 或者大小不一的问题要实现对齐,使用getTextBounds比较方便.

3. 获取文字的理想宽度,使用measureText比较方便

## 图示代码

```java
    Paint mPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    Rect bound = new Rect();

    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        mPaint.setTextSize(600);
        String text = "p";
        draw1(canvas, text, 800);
    }

    private void draw1(Canvas canvas, String text, float baseLineY) {

        mPaint.getTextBounds(text, 0, text.length(), bound);
        mPaint.setColor(Color.rgb(0xb4, 0xb4, 0xb4));
        canvas.drawRect(bound.left, bound.top + baseLineY, bound.right, bound.bottom + baseLineY, mPaint);

        float width = mPaint.measureText(text);
        mPaint.setColor(Color.rgb(0x00, 0x00, 0x00));
        canvas.drawRect(bound.left, bound.top + baseLineY - 30, bound.left + width, bound.top + baseLineY - 20, mPaint);

        Paint.FontMetrics fontMetrics = mPaint.getFontMetrics();
        mPaint.setColor(Color.BLACK);
        canvas.drawText(text, 0, baseLineY, mPaint);
        canvas.drawLine(0, baseLineY, getWidth(), baseLineY, mPaint);
        mPaint.setColor(Color.RED);
        canvas.drawLine(0, baseLineY + fontMetrics.top, getWidth(), baseLineY + fontMetrics.top, mPaint);
        canvas.drawLine(0, baseLineY + fontMetrics.bottom, getWidth(), baseLineY + fontMetrics.bottom, mPaint);
        mPaint.setColor(Color.BLUE);
        canvas.drawLine(0, baseLineY + fontMetrics.ascent, getWidth(), baseLineY + fontMetrics.ascent, mPaint);
        canvas.drawLine(0, baseLineY + fontMetrics.descent, getWidth(), baseLineY + fontMetrics.descent, mPaint);

    }
```

[1]: http://static.oschina.net/uploads/space/2015/0312/141056_3CCV_93688.png
