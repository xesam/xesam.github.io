---
layout: post
title:  "Javascript TouchSlide"
date:   2015-01-20 12:46:04 +0800
categories: javascript
tag: [javascript]
---
一个简单的手机网页滑屏效果库

进行适当的CSS设置之后可以实现常见的全屏滑动

github地址：[TouchSlide](https://github.com/xesam/TouchSlide)
git.oschina.net地址:[TouchSlide](http://git.oschina.net/xesam/TouchSlide)

## 原理

检测上滑或者左右滑动事件，然后使用CSS3动画进行页面转换。

## 使用

```html

    <div class="demo horizontal">
            <ul>
                <li>1</li>
                <li>2</li>
                <li>3</li>
                <li>4</li>
            </ul>
        </div>

    [script]

    new TouchSlide(containerId or ) //default horizontal slide

    or

    new TouchSlide(containerId, {
        'orientation': TouchSlide.VERTICAL
    }) // vertical slide
```

效果图

![vertical](http://git.oschina.net/xesam/Blog/raw/master/javascript/vertical.png)

*****

![horizontal](http://git.oschina.net/xesam/Blog/raw/master/javascript/horizontal.png)


