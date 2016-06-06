---
layout: post
title:  "【Linux】各种配置记录"
date:   2016-01-01 13:46:04 +0800
categories: computer
tag: [computer]
---
# 【Linux】各种配置记录

# Python

### pip

安装

```shell
    sudo apt-get install python-pip
    #或者
    sudo aptitude install python-pip
```

### virtualenv

安装

```shell
    sudo pip install virtualenv
```

创建虚拟环境

```shell
    virtualenv test_env
```
默认情况下，虚拟环境会依赖系统环境中的site packages，就是说系统中已经安装好的第三方package也会安装在虚拟环境中，
如果不想依赖这些package，那么可以加上参数 

    --no-site-packages　

进入虚拟环境

    source ./bin/activate

退出虚拟环境

    deactivate
    
### supervisor

    pip install supervisor

### tornado

    pip install tornado

autoreload

```python
    ioloop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
```

# Docker

Ubuntu 14.04 

### 安装最新

```shell

sudo apt-get install apt-transport-https  
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9  
sudo sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"  
sudo apt-get update  
   
apt-get install -y lxc-docker  #安装
  
apt-get update -y lxc-docker  #更新
  
ln -sf /usr/bin/docker /usr/local/bin/docker  
```
    
# lua

环境 Ubuntu 14.04

ubuntu 下 lua 的安装包，binary和dev是分开装的。

```shell
    sudo apt-get install lua5.2
    sudo apt-get install liblua5.2-dev
```

c 调用 lua

```c

#include <stdio.h>
#include <string.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

int main(int argc, char const *argv[]){
	char buff[256];
	int error;
	lua_State *L = luaL_newstate();
	//...
	lua_close(L);
	return 0;
}

```

第一个错误：

    lua.h: No such file or directory
    
没有找到 h 头文件，需要指定：

    gcc lua_test.c -I/usr/include/lua5.2

第二个错误：

    undefined reference to `luaL_newstate'

没有找到 so 文件，需要指定：

    gcc lua_test.c -I/usr/include/lua5.2 -llua5.2
    
找到文件位置：

    locate lua.h
    locate liblua
    
