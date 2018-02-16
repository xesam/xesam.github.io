---
layout: post
title:  "Android 的SoundPool"
date:   2016-06-30 08:00:00 +0800
categories: android
tag: [android]
---
SoundPool 适合播放小而短促的声音，比如声效。可以同时播放多个声音，效率高。
MediaPlayer 适合播放大片段的声音，比如音乐。一次只能播放一个声音，新的声音会中断当前正在播放的声音。

## 简单使用

看名字就知道，SoundPool 是一个“池”。因此，SoundPool 会先将多个的声音文件全部加载进内存中，需要播放的时候就可以立即播放。

所以，大致的步骤应该是：

1. 创建一个池
2. 加载声音
3. 等待声音加载完成
4. 播放声音

一个简单的例子：

```java

    //创建 SoundPool
    //新版本推荐使用 SoundPool.Builder 来创建
    SoundPool mSoundPool = new SoundPool(2, AudioManager.STREAM_MUSIC, 0);
    
    //加载声音文件，load 方法有多个重载，按需使用
    int soundId = mSoundPool.load("/storage/0/1.aac", 1);
    
    //设置加载监听
    mSoundPool.setOnLoadCompleteListener(new SoundPool.OnLoadCompleteListener() {
        @Override
        public void onLoadComplete(SoundPool soundPool, int sampleId, int status) {

        }
    });

    //播放声音，播放一遍，然后重复10遍，具体参数参见文件
    final int streamId = mSoundPool.play(soundID, 1, 1, 0, 10, 1);
    
    new Handler().post(new Runnable(){
        @Override
        public void run(){
            mSoundPool.stop(streamId);
            mSoundPool.unload(soundId);
        }
    });
    
```

## 几点说明

### soundId 与 streamId

注意上面代码的区别. SoundPool#load 加载完成返回的是 soundId， SoundPool#unload 卸载的也是 soundId。

SoundPool#play 播放的也是 soundId，但是 SoundPool#play 播放返回的是 streamId，同时 SoundPool#stop 停止的是 streamId。

对于同一个声音文件，每次加载 SoundPool#load 的时候，返回的 soundId 都是不同的。
对于同一个 soundId，每次播放 SoundPool#play(soundId) 的时候，返回的 streamId 也是不同的，因此这个不能重用。
因此，在这两种 ID 的处理上，需要谨慎。

<table>
    <thead>
    <tr>
        <th></th><th>Sound Id</th><th>Stream Id</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>load</td><td>（√）返回 soundId</td><td>×</td>
    </tr>
    <tr>
        <td>unload</td><td>（√）传入 soundId</td><td>×</td>
    </tr>
    <tr>
        <td>play</td><td>（√）传入 soundId</td><td>（√）返回 streamId</td>
    </tr>
    <tr>
        <td>pause</td><td>×</td><td>（√）传入 streamId</td>
    </tr>
    <tr>
        <td>resume</td><td>×</td><td>（√）传入 streamId</td>
    </tr>
    <tr>
        <td>stop</td><td>×</td><td>（√）传入 streamId</td>
    </tr>
    </tbody>
</table>

### 资源释放
    
这里的释放包括两方面：

1. 释放 sound。即 unload(soundId)，释放已经加载的声音文件。
2. 释放 stream。即 stop(streamId)，释放每次 play 的播放流，可以起到停止声音的效果，如果只是想暂停/恢复，可以用 pause/resume。

通常来说，运行过程中没必要释放sound，因为使用 SoundPool 通常是为了迅速播放小文件，如果每次都释放 sound，反而会影响效率。在程序结束的时候再统一释放即可。

### 可能问题
 
1. play 没有声音
    
    可能原因有：没有正确加载 sound，或者同时加载的声音数目超过上限， 或者 sound 还未 load 完毕。
    
    因此，可以先检测是否有加载过的 soundId，如果有就直接播放，如果没有则启动加载过程，在 OnLoadCompleteListener 回调中再进行播放。
    
    如果是因为加载的声音数目超过上限，需要先 release 资源，然后再重新 load，注意 unload 不一定会释放数目。
    
    
2. 声音播放结束
    
    SDK 并没有提供方法来获知一段声音是否播放完毕

### priority 参数

SoundPool#play 中的 priority 参数，只在同时播放的流的数量超过了预先设定的最大数量时起作用，管理器将自动终止优先级低的播放流。
如果存在多个同样优先级的流，再进一步根据其创建事件来处理，新创建的流的优先级是最低的，将被终止或者忽略。

SoundPool#load 中的 priority 参数暂时没什么用，我估计也是用来自动处理 sound 加载数目的问题的。


##### 参考
[https://developer.android.com/reference/android/media/SoundPool.html](https://developer.android.com/reference/android/media/SoundPool.html)
[http://blog.csdn.net/qduningning/article/details/8680575](http://blog.csdn.net/qduningning/article/details/8680575)

