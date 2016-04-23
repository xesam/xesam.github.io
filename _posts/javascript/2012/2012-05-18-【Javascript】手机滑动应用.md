---
layout: post
title:  "【Javascript】手机滑动应用"
date:   2012-05-18 13:46:04 +0800
categories: Javascript
---

## 完善版本参见Github

[https://github.com/xesam/TouchSlide](https://github.com/xesam/TouchSlide)

## 简介

浏览器的动画效果一般都是用js来控制元素的 top,left,right,bottom 等属性来实现，不过在移动浏览器上，鉴于对css3的支持，完全可以抢先使用css3 translate。
不过需要注意的是，使用css translate在android上比较那个啥XX，在safari上，transalte2d的效果远远不如translate3d。
所以，移动浏览器上，最好是使用translate3d来实现。

手机滑动事件处理主要使用的是一个touch事件，在iOS上还有gusture事件，不过android现在还很悲剧。具体可以参考apple开发论坛，里面有详细说明。

当我们点击一个元素时，touchstart会最先触发，出发顺序：

    touchstart —— mousedown —— click

测试代码

```html
<div id="test" style="width: 100%; height: 200px; background: red;"></div>
<div id="result"></div>
<script type="text/javascript">
    var Time = {};
    document.getElementById("test").addEventListener('touchstart',function(){
        Time.t1 = (new Date()).getTime();
    },false);
    document.getElementById("test").addEventListener('mousedown',function(){
        Time.t2 = (new Date()).getTime();
    },false);
    document.getElementById("test").addEventListener('click',function(){
        Time.t3 = (new Date()).getTime();
        document.getElementById("result").innerHTML = 'touchstart - mousedown = ' + (Time.t2 - Time.t1) + '<br />'
                'mousedown - click = ' + (Time.t3 - Time.t2) ;
    },false);
</script>
```

测试的各个浏览器版本越低，click相对 touchstart 的延迟越高

具体的滑动实现（一个swipe.js的简化版本）：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title></title>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <style type="text/css">
        *{margin: 0; padding: 0;}
        body{ width: 100%;}
        ul,li{ list-style: none;}
        input[type="button"]{ margin: 10px; width: 40px; height: 24px;}
        #page{ text-align: center;}
        .demo{ width: 100%; height: 200px; overflow: hidden;}
        .list{}
        .list li{ display: table-cell; height: 200px; }
        .list li:first-child{ background: #87ceeb;}
        .list li:last-child{ background: #8b4513;}
    </style>
</head>
<body>
<div id="page">
    <div class="demo">
        <ul class="list">
            <li>1</li>
            <li>2</li>
        </ul>
    </div>
    <div class="demo">
        <ul class="list">
            <li>3</li>
            <li>4</li>
        </ul>
    </div>
</div>
<script type="text/javascript">

    window.TouchSlide = function(container){
        if(!container){ //没有外包装，直接返回
            return 1;
        }
        this.container = this._$(container);
        this.element   = this.container.children[0];
        this.slides    = this.element.children;
        this.index     = 0;
        this.init();

        var _this = this;

        this.element.addEventListener('touchstart',function(e){
            _this.touchstart(e);
        },false);
        this.element.addEventListener('touchmove',function(e){
            _this.touchmove(e);
        },false)
        this.element.addEventListener('touchend',function(e){
            _this.touchend(e);
        },false)
        window.addEventListener('resize', function(e){ //缩放屏幕的时候需要动态调整
            _this.init();
        }, false);
    }
    TouchSlide.prototype = {
        constructor : TouchSlide,
        _$ : function(el){
            return 'string' == el ? document.getElementById(id) : el;
        },
        init : function(){
            this.container.style.visibility = 'none';
            this.width = this.container.getBoundingClientRect().width;
            this.element.style.width = this.slides.length * this.width + 'px';
            var index = this.slides.length;
            while(index--){
                this.slides[index].style.width = this.width + 'px';
            }
            this.container.style.visibility = 'visible';
        },
        slideTo : function(index, duration) {
            this.move(0,index,duration);
            this.index = index;
        },
        move : function(deltaX,index,duration){
            var style = this.element.style;
            style.webkitTransitionDuration = duration + 'ms';
            style.webkitTransform = 'translate3d(' + ( deltaX - index * this.width) + 'px,0,0)';
        },
        isValidSlide : function(){
            return Number(new Date()) - this.start.time < 250 && Math.abs(this.deltaX) > 20 //在250ms内滑动的距离超过20px
                    || Math.abs(this.deltaX) > this.width/2 //或者滑动超过容器的一半宽度
        },
        isPastBounds : function(){
            return !this.index && this.deltaX > 0 //第一个，但是依旧向右滑动
                    || this.index == this.slides.length - 1 && this.deltaX < 0//最后一个，但是依旧向左滑动，这两种情况越界了，是无效的
        },
        touchstart : function(e){
            var touchEvent = e.touches[0];
            this.deltaX = 0;
            this.start = {
                x    : touchEvent.pageX,
                y    : touchEvent.pageY,
                time : Number(new Date())
            } ;
            this.isScrolling = undefined;
            this.element.style.webkitTransitionDuration = 0;
        },
        touchmove : function(e){
            this.deltaX = e.touches[0].pageX - this.start.x;
            //判断是左右滑动还是上下滑动，上下滑动的话就无视
            if(typeof this.isScrolling == 'undefined'){
                this.isScrolling = !!( this.isScrolling || Math.abs(this.deltaX) < Math.abs(e.touches[0].pageY - this.start.pageY) );//判断是否是是竖直滚动
            }
            if(!this.isScrolling){
                e.preventDefault();
                this.deltaX = this.deltaX / (this.isPastBounds() ? 2 : 1);
            }
            this.move(this.deltaX,this.index,0);
        },
        touchend : function(e){
            if (!this.isScrolling) {
                this.slideTo( this.index + ( this.isValidSlide() && !this.isPastBounds() ? (this.deltaX < 0 ? 1 : -1) : 0 ), 200 );
            }
        }
    }

    Array.prototype.slice.call(document.getElementsByClassName('demo'),0).forEach(function(item){
        new TouchSlide(item)
    })

</script>
</body>
</html>
```