---
layout: post
title:  "【Android】Android事件传递"
date:   2016-02-29 13:46:04 +0800
categories: android
tag: [android]
---

MotionEvent 传递流程

```java
    //->ViewRootImpl:
    private void deliverPointerEvent(QueuedInputEvent q) {
        ...
        boolean handled = mDecorView.dispatchPointerEvent(event);
        ...
    }
    
    //-> DecorView:
    public final boolean dispatchPointerEvent(MotionEvent event) {
        if (event.isTouchEvent()) {
            return dispatchTouchEvent(event);
        } else {
            return dispatchGenericMotionEvent(event);
        }
    }
    
    //-> DecorView:
    public boolean dispatchTouchEvent(MotionEvent ev) {
        final Callback cb = getCallback();//这里的 Callback 是 Activity 
        return cb != null && !isDestroyed() && mFeatureId < 0 ? cb.dispatchTouchEvent(ev)
                : super.dispatchTouchEvent(ev);
    }
    
    //->Activity:
    public boolean dispatchTouchEvent(MotionEvent ev) {
        if (ev.getAction() == MotionEvent.ACTION_DOWN) {
            onUserInteraction();
        }
        if (getWindow().superDispatchTouchEvent(ev)) { //对于手机来说 getWindow() 返回一个 PhoneWindow
            return true;
        }
        return onTouchEvent(ev);
    }
    
    //->PhoneWindow:
    public boolean superDispatchTouchEvent(MotionEvent event) {
        return mDecor.superDispatchTouchEvent(event);
    }
    
    //-> DecorView:
    public boolean superDispatchTouchEvent(MotionEvent event) {
        return super.dispatchTouchEvent(event);
    }
        
    //-> ViewGroup:
    public boolean dispatchTouchEvent(MotionEvent ev) {
    ...
    }
```

ViewGroup 分发流程




##ACTION_DOWN


##ACTION_MOVE


##ACTION_UP

