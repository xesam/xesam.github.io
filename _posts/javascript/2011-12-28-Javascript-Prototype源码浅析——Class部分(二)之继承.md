---
layout: post
title:  "【Javascript】Prototype源码浅析——Class部分(二)之继承"
date:   2011-12-28 08:36:04 +0800
categories: javascript
tag: [javascript]
---
前面分析了Class的构造部分，现在，需求变动啦（又变动啦！），现在需要一个Teacher类，同样有say方法，但是除此之外还有teach方法。我们再重复定义say就不划算了，因为Person有现成的，于是就牵扯到继承的问题，我要让Teacher类继承Person的方法。

先复习一下JS常见继承的基本原理。假定现在有Person和Teacher类，让Teacher继承Person的方法：

```javascript
Teacher.prototype = new Person();
```
这个方法的缺点是Person有可能很庞大，许多初始化操作是我们不必要的，我们只需要Person.prototype的方法而已。因此用一个Obj作为桥梁来传递prototype，改造如下：

```javascript
    var Obj = function(){};
    Obj.prototype = Person.prototype;
    Teacher.prototype = new Obj();
```
现在回到Prototype的继承来：

第一、先规定继承采用的调用形式：

```javascript
    var teacher = Class.create(Person,{
        initialize:function(age){
            this.age = age;
        },
        teach : function(){
            console.log('teach');
        }
    });
```
第二、既然有父类和子类，我们规定用Teacher.superclass来表示Teacher的父类，用Teacher.subclasses来表示Teacher的子类，一旦Teacher被别的类（暂记为ClassTest）继承，那么Teacher.subclasses中就会添加ClassTest这一项。

按照上面说的，继续改造我们的create方法。具体的步骤就是

1、如果有父类，就获取父类——>2、将新类的superclass指向父类——>3、将新类推入父类的subclasses数组中，同时创建新类的subclasses——>如果有父类，那么新类继承父类。

所以可以得到我们的实现：

```javascript
　　　　　　var Class = (function(){
         function create(){

             var properties = $A(arguments);

             var parent = null;
             if(properties[0].constructor == Function){
                 parent = properties.shift(); //如果有父类的话，那么在这一步就获得了父类的引用。
             }

             function kclass(){
                this.initialize.apply(this,arguments);
             };
             kclass.addMethods = Class.Methods.addMethods;

             kclass.superclass = parent;
             kclass.subclasses = [];//用来存储类的子类
             if(parent){
                 var blank = function(){};
                 blank.prototype = parent.prototype;
                 kclass.prototype = new blank();
                 parent.subclasses.push(kclass);
             }

             for(var i = 0; i < properties.length; i++){
                kclass.addMethods(properties[i]);
             }
             if (!kclass.prototype.initialize){
                 kclass.prototype.initialize = function(){};
             }
             return kclass;
        }
　　　　　　  function addMethods(source){
            for(var property in source){
                this.prototype[property] = source[property];
            }
        }
        return {
            create : create,
            Methods : { 
                addMethods : addMethods
            }
        }
    })();
```
一个实例：

```javascript
   var Person = Class.create({
        initialize:function(name){
            this.name = name;
        },
        say : function(){
            console.log('hello ' + this.name);
        }
    });
    var xesam =new Person('xesam');
    xesam.say();
    
    var Teacher = Class.create(Person,{
        initialize:function(name,age){
            this.name = name;
            this.age = age;
        },
        teach : function(){
            console.log('teach');
        }
    });
    var teacher = new Teacher('xesam_1',24);
    teacher.say();
```

OK，到这里，继承部分可以算完了。不过现在需求又变了（真的是又TM变啦！）。

现在要求Teacher里面有一个不一样的say方法，但是又部分功能是一样的。

```javascript
    var Teacher_2 = Class.create(Person,{
        initialize:function(name,age){
            this.name = name;
            this.age = age;
        },
        teach : function(){
            console.log('teach');
        },
        say : function(){
            console.log('hello ' + this.name);//这里和Person里面的say一致
            console.log('这里才是我自己的部分');
        }
    });
```
因此我们需要一个调用父类同名方法的机制，现在还是按照Prototype的定义来做如下规定：

要调用父类的方法，我们就将'$super'作为子类同名方法的第一个参数传入，来代替父类的同名方法，因此Teacher_2的定义就变为：

```javascript
    var Teacher_2 = Class.create(Person,{
        initialize:function(name,age){
            this.name = name;
            this.age = age;
        },
        teach : function(){
            console.log('teach');
        },
        say : function($super){
            $super();
            console.log('这里才是我自己的部分');
        }
    });
```
现在继续来处理Class对象，下面的内容需要用到Function.prototype部分的知识。

还记得大明湖畔的Function.prototype.wrap方法么，可以回过头去看看Prototype源码浅析——Function.prototype部分(一)。

所以最终的实现为：

```javascript
    var Class = (function(){
         function create(){
             var properties = $A(arguments);
             var parent = null;
             if(properties[0].constructor == Function){
                 parent = properties.shift(); //如果有父类的话，那么在这一步就获得了父类的引用。
             }

             function kclass(){
                this.initialize.apply(this,arguments);
             };
             kclass.addMethods = Class.Methods.addMethods;

             kclass.superclass = parent;
             kclass.subclasses = [];//用来存储类的子类
             if(parent){
                 var blank = function(){};
                 blank.prototype = parent.prototype;
                 kclass.prototype = new blank();
                 parent.subclasses.push(kclass);
             }

             for(var i = 0; i < properties.length; i++){
                kclass.addMethods(properties[i]);
             }
             if (!kclass.prototype.initialize){
                 kclass.prototype.initialize = function(){};
             }
             return kclass;
        }
        function addMethods(source){
            var ancestor = this.superclass && this.superclass.prototype;//注意这里的写法，ancestor获得的是this.superclass.prototype
            for(var property in source){
                //如果需要继承调用父类的同名方法，那么就会进入下面的条件分支
                var value = source[property]
                if(ancestor){
                    if (ancestor && value.argumentNames()[0] == "$super") {
                        var method = value;
                        value = (function(m) {
                            return function(){
                                return ancestor[m].apply(this, arguments);
                            };
                        })(property);
                        value = value.wrap(method);//此时，value的第一个参数$super被替换成父类同名方法，并且修正了作用域
                    }
                }
                this.prototype[property] = value;
            }
        } 
        return {
            create : create,
            Methods : { 
                addMethods : addMethods
            }
        }
    })();
```
实例代码：

```javascript
    var Person = Class.create({
        initialize:function(name){
            this.name = name;
        },
        say : function(){
            console.log('hello ' + this.name);
        }
    });
    var xesam =new Person('xesam');
    xesam.say();// hello xesam
    
    var Teacher = Class.create(Person,{
        initialize:function(name,age){
            this.name = name;
            this.age = age;
        },
        teach : function(){
            console.log('teach');
        }
    });
    var teacher = new Teacher('xesam_1',24);
    teacher.say();// hello xesam_1

    var Teacher_2 = Class.create(Person,{
        initialize:function($super,name,age){
            $super(name);
            this.age = age;
        },
        teach : function(){
            console.log('teach');
        },
        say : function($super){
            $super();
            console.log('这里才是我自己的部分');
        }
    });

    var teacher_2 = new Teacher_2('xesam_2',24);
    teacher_2.say();
    // hello xesam_2
    // 这里才是我自己的部分
```

最后有一点没有说的是对象枚举bug，就是Prototype源码中定义的：

```javascript
    var IS_DONTENUM_BUGGY = (function(){
        for (var p in { toString: 1 }) {
            if (p === 'toString') return false;
        }
        return true;
    })();
```
因为这个在前面的Object部分已经说过了，参见：Prototype源码浅析——Object部分(一)

总结:在Prototype的Class中。

在我们创建一个类的时候，完成类的方法设置、父类和子类之间的关系设置。
在我们创建一个实例的时候，initialize是自动调用的，以初始化一个实例。
一个类有addMethods方法，但是实例没有addMethods方法的，因为addMethods并没有加载到原型上面。
因此我们创建多少个类，就有多少个addMethods方法，这样也是一种浪费。而且，我们不能用addMethods来给一个实例添加方法。

这里所有的类与继承机制都是很基本的，基本没有涉及封转的部分。

