---
layout: post
title:  "【Javascript】轻量级Web Database存储库html5sql.js"
date:   2012-03-10 10:46:04 +0800
categories: Javascript
---

阅读之前，先看W3C关于WEB Database的一段话：

    Beware. This specification is no longer in active maintenance and the Web
    Applications Working Group does not intend to maintain it further. 

意味着WEB Database规范陷入僵局。

## html5sql

html5sql官方网址：[http://html5sql.com/](http://html5sql.com/)

## 简述

html5sql是一个让HTML5 Web Database使用更方便的轻量级JavaScript模块，它的基本功能是提供在一个事务中顺序执行SQL语句的结构。
虽然 Web Database并没有停止前进的脚步，这个模块仅仅可以简化与数据库的交互过程。这个模块还包含有其他很多小细节以便开发人员能够更简单，自然便捷的工作。

### 核心特征

1. 提供以不同方式顺序执行SQL语句的能力：

        单条SQL语句
        一组SQL语句
        一组SQL语句对象（当你要想SQL中注入数据或者在SQL执行后调用一个回调函数时，可能需要使用这种形式）
        从一个分割完毕包含SQL语句的文件中
        
2. 提供一个控制数据库版本的框架

### 例子

如果你用过HTML5 web database,你就会发现它有多蛋疼，尤其是当你开始建立你的表时。好了，现在你会发现这些都不是问题。为了更清楚的表明我的意思以及这个模块的能力，看下面的例子：

假设你打算建立一个表兵千插入一组数据到这个表里面。如果你使用html5sql的话，你只需要把所有的语句都放入一个单独的文件中，本例中我们取名为Setup-Tables.SQL。这个文件的形式类似于

本例中我们取名为Setup-Tables.SQL。这个文件的形式类似于：

```sql
CREATE TABLE example (id INTEGER PRIMARY KEY, data TEXT);
INSERT INTO example (data) VALUES ('First');
INSERT INTO example (data) VALUES ('Second');
INSERT INTO example (data) VALUES ('Third');

CREATE TABLE example2 (id INTEGER PRIMARY KEY, data TEXT);
INSERT INTO example2 (data) VALUES ('First');
INSERT INTO example2 (data) VALUES ('Second');
INSERT INTO example2 (data) VALUES ('Third');
```

有了html5sql之后，为了顺序执行这些SQL语句（包括创建表），你只需要打开数据库，然后添加下面一段代码就可以了。

```javascript
    $.get('Setup-Tables.SQL',function(sqlStatements){
    
    html5sql.process(
        //This is the text data from the SQL file you retrieved
        sqlStatements,
        function(){
            // After all statements are processed this function
            //   will be called.
        },
        function(error){
            // Handle any errors here
        }
        );
    });
```

借助于jQuery的get方法，你已经从单独的文件（'Setup-Tables.SQL'）获得了SQL语句，并且按照出现的顺序分割执行了。

## 性能
上面的描述听起来还不错，不过你可能会问SQL顺序执行的时候性能是不是会受损。答案就是，影响不算明显，至少就我看来目前是这样。
比如，我用 Google的Chrome桌面版创建一张表，然后向表中顺序插入10,000条记录，整个执行过程的时间有波动，不过平均值处于2-6秒的范围内，
因此我有理由相信html5sql在处理大量数据的时候会有不俗的表现。

## 建议
SQL的核心被设计为一种顺序执行的语言，某些语句必须在其他的语句前面执行。比方说，在插入记录之前，你必须先创建一张表。
相反的，javascript 是一种异步、事件驱动的语言。对于开发者来说，这些异步特征增加了HTML5客户端数据库规范与说明的复杂性。
写这个库的时候，W3C已经不再维护Web SQL Database规范了。
尽管如此，由于webkit已经实现了设个接口，而且由于webkit内核浏览器的庞大用户群，尤其是移动设备上，因此这个库还是有用的。

虽然这个模块减少了HTML5 SQL database的复杂程度，但是并没有简化SQL本身，这是有意而为之的。SQL是一门强大的语言，盲目的简化它只会弄巧成拙。在我的经验中，学好SQL才是王道，大势所趋撒。

## 用户指南

html5sql模块中内建了3个函数：

### 一，html5sql.openDatabase(databaseName, displayName, estimatedSize)
html5sql.openDatabase是对原生openDatabase方法的一个封装，这个方法打开一个数据库连接并返回对连接的引用。这是所有其他操作之前的第一步。

这个方法有三个参数：

    databaseName - 数据库的名字.任意你喜欢的有效的名字，通常可以是“com.yourcompany.yourapp”之类的
    displayName - 数据库描述信息
    estimatedSize - 数据库大小.5M = 5*1024*1024

如果读者熟悉web database原生方法的话，会发现上面的封装中少了版本信息这个参数。当你需要改变数据库的表结构时，版本信息是一个得力的标识工具，改变版本的这个方法被封装成html5sql的changeVersion方法。

现在，我们创建一个通常的数据库连接：

```javascript
html5sql.openDatabase(
     "com.mycompany.appdb",
     "The App Database"
     3*1024*1024
);
```

### 二，html5sql.process(SQL, finalSuccessCallback, errorCallback)

html5sql.process()方法是所有功能的载体，一旦你创建了数据库连接，就可以传递SQL语句，剩下的事情就交给html5sql.process()，他会保证SQL顺序执行。

html5sql.process()的第一个参数是SQL语句，其传递形式有许多种：

1. 字符串形式 - 你可以向process方法传递一个简单字符串，形如：

        "SELECT * FROM table;"
        
    或者一组用分号（“;”）连接的简单字符串，形如：

        "CREATE table (id INTEGER PRIMARY KEY, data TEXT);" +
        "INSERT INTO table (data) VALUES ('One');" +
        "INSERT INTO table (data) VALUES ('Two');" +
        "INSERT INTO table (data) VALUES ('Three');" +
        "INSERT INTO table (data) VALUES ('Four');" +
        "INSERT INTO table (data) VALUES ('Five');"

2. 来自独立文件的SQL语句。来自独立文件的SQL语句的例子跟上面的例子一样，没有本质区别。
3. 一组SQL语句字符串，你可以向html5sql.process()传递一组SQL语句，形如：

         [
             "CREATE table (id INTEGER PRIMARY KEY, data TEXT);",
             "INSERT INTO table (data) VALUES ('One');",
             "INSERT INTO table (data) VALUES ('Two');",
             "INSERT INTO table (data) VALUES ('Three');",
             "INSERT INTO table (data) VALUES ('Four');",
             "INSERT INTO table (data) VALUES ('Five');"
         ]
4. 一组SQL语句对象。这是一种最实用的形式，直接传递一组SQL语句对象。SQL语句对象的结构域原生executeSQL 方法的参数一致，有三个部分：

        SQL[string]——包含SQL语句的字符串，其中可以包含替换符“?”
        data[array]——一组需要插入到SQL语句中替换?符号的数据，其中SQL语句中?的数量必须与data中数据的数量一致
        success (function)——执行完SQL语句后回调的函数，可以处理SQL语句的执行结果。另外，如果这个方法返回一个数组，这个返回的数组还可以作为下一条SQL语句的data参数来执行。这样就允许你在SQL执行中调用将上一条SQL语句的结果，在使用外键的情况中，这个比较常见。
        
    或许最简单的定义以及使用这个对象的方式是只用对象字面量。通用的模板类似下面的形式：

             {
                "sql": "",
                "data": [],
                "success": function(transaction, results){
                 //Code to be processed when sql statement has been processed
                }
             }
             
    因此，一个简单的SQL对象参数实例如下：
        
        [
            {
                "sql": "INSERT INTO contacts (name, phone) VALUES (?, ?)",
                "data": ["Joe Bob", "555-555-5555"],
                "success": function(transaction, results){
                        //Just Added Bob to contacts table
                    },
                },
            {
                "sql": "INSERT INTO contacts (name, phone) VALUES (?, ?)",
                "data": ["Mary Bob", "555-555-5555"],
                "success": function(){
                    //Just Added Mary to contacts table
                },
            }
        ]
　　上面的对象中，唯一与原生executesql()不同的是，没有error部分的处理方式，这是因为有一个通用的错误处理回调函数来处理出现error的情况，从而避免每条语句都进行error定义。这个通用的错误处理函数就是 html5sql.process()的第三个参数。

#### 小结

html5sql.process()总共有三个参数，

    SQL - 上面叙述的任一种形式均可
    finalSuccessCallback - 一个最终的，在所有SQL成功执行完毕后触发
    errorCallback - 处理本过程中的所有错误的通用函数，发生任何错误时，当前事务会回滚，数据库版本不改变。
    
总结一下，这个方法的一个完整示例如下：

```javascript
 html5sql.process(
     [
         "DROP TABLE table1",
         "DROP TABLE table2",
         "DROP TABLE table3",
         "DROP TABLE table4"
     ],
     function(){
         console.log("Success Dropping Tables");
     },
     function(error, statement){
         console.error("Error: " + error.message + " when processing " + statement);
     }
 );
```

### 三，html5sql.changeVersion("oldVersion","newVersion",SQL,successCallback,errorCallback)

html5sql.changeVersion() 是创建、迁移数据库以及处理版本所需要的方法。

这个方法会检测当前版本与旧的版本参数（oldVersion）是否一致，如果吻合的话，就会执行参数中的SQL语句，并改变数据库的版本为 newVersion参数所示的值。

    oldVersion - 需要修改的数据库的版本号，默认初始值为""
    newVersion - 你赋的新值
    SQL - 你要执行的SQL语句.具体说明参见html5sql.process()部分
    finalSuccessCallback - 成功执行后调用的函数
    errorCallback - 通用数据处理函数，与html5sql.process()中一样， 发生错误的时候，整个事务回滚，并且不改变版本号。

## 源码深入

本JS库最大的问题就是如果要同时操纵多个数据库，那么就会引起混乱，这一点作者似乎并没有做多考虑。另外就是对于这种批量执行SQL语句的错误恢复处理感觉还是不够完善。

## 补充

#### 补充一

html5sql.openDatabase()其实有四个参数

```javascript
    html5sql.openDatabase = function (name, displayname, size, whenOpen) {
         html5sql.database = openDatabase(name, "", displayname, size);
         readTransactionAvailable = typeof html5sql.database.readTransaction === 'function';
         if (whenOpen) {
             whenOpen();
         }
     };
```
                 
最后的whenOpen是在获取数据库引用的时候触发的。

#### 补充二
　　另外还有两个用于调试的属性，logErrors和logInfo:默认都是false，设置为true的时候可以看到每一步操作的过程。由于调用的是控制台的console.log，可能在某些浏览器上引发错误。

#### 补充三

对于process方法，不论你采用什么形式的SQL参数，最终都会被转换成SQL对象的形式。

当SQL语句包含的仅仅只有SELECT操作时，内部使用的是readTransaction方法，注意一下readTransaction与transaction的区别。

这边用的是readTransaction，这是为了保证不对表进行写操作，这是一种安全的举措，当然也可以用transaction。不过readTransaction方法存在一定的兼容性问题，所以使用之前应该保证检测无误。
