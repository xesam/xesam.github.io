---
layout: post
title:  "Js Promise"
date:   2029-07-04 08:00:00 +0800
categories: javascript
tag: [javascript]
---
最近面试前端，发现很多人虽然经常用 Promise，但其实并不是很理解，同时也发现其实好几个同事也不是很理解，所以做了一个内部培训，简单整理如下：

## 如何把人绕晕

片段一：

```javascript
let p0 = Promise.resolve(1);
let p1 = Promise.resolve(p0);
p1.then(res=>{
    console.log('1', res);
})
```

片段二：
```javascript
let p0 = Promise.resolve(1);
let p1 = new Promise(resolve=>{
    setTimeout(()=>{
        resolve(p0);
    }, 0);
});
p1.then(res=>{
    console.log('1', res);
})
```

片段三：
```javascript
let p0 = Promise.resolve(1);
let p1 = Promise.reject(p0);
p1.then(res=>{
    console.log('1', res);
}).catch(res=>{
    console.log('2', res);
}).then(res=>{
    console.log('3', res);
});
```

片段四：
```javascript
let p0 = Promise.resolve(1);
let p1 = new Promise((resolve,reject)=>{
    setTimeout(()=>{
        reject(p0);
    }, 0);
});
p1.then(res=>{
    console.log('1', res);
}).catch(res=>{
    console.log('2', res);
}).then(res=>{
    console.log('3', res);
});
```

片段五：
```javascript

let p0 = Promise.resolve(1);

const p1 = p0.then(res=>{
                console.log(res);
            })
            .then(res=>{
                console.log(res);
                throw new Error(2);
            })
            .catch(err=>{
                console.log(3);
                return 4;
            })
            .then(res=>{
                console.log(res);
                return Promise.reject(5);
            })
            .catch(err=>{
                console.log(err);
            });

p2 = p1.then(res=>{
    console.log(res);
    return Promise.resolve(p0);
}).then(res=>{
    console.log(res === p0);
    console.log(res);
    console.log(p0);
    return p0;
});

console.log(p1 === p0);
console.log(p2 === p0);

```

最后的输出是怎样的？

```shell
false
false
1
undefined
3
4
5
undefined
```

无解最多的地方是 Promise#throw， Promise#throw 的作用不是中断链条，而是吃掉错误。

Promise#then 以及 Promise#throw 方法的方法体如果在执行过程中没有发生异常，那么两者都会返回一个新的 Promise，后续是触发 Promise#then 还是 Promise#throw，完全取决于新 Promise 的状态。


## 公式


## 与 async 和 await 之间的关系

一个常见的错误是没有理解 async 和 await 的语义，这两者都是语法糖，并没有改变 js 单线程执行的本质。await 的返回值永远是一个 Promise，于是又回到 Promise 的世界了。

一个真实案例：

```javascript
async function isLogin(){
    try{
        const res = await checkSession();
    }catch(e){
        console.err(e);
    }
}

function getUser(){
    if(isLogin()){
        return getUser();
    }else{
        return {};
    }
}

```

isLogin() 永远不会是 fasly，因此这个条件判断没有任何意义，对于新手来说，如果没有理解 Promise，还是不要使用 async/await 的好。 
