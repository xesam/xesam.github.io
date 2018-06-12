---
layout: post
title:  "fork与printf"
date:   2016-06-06 16:51:38 +0800
categories: computer
tag: [computer]
---
测试 fork 的时候，出现以下的一个情况：

```c
#include <stdio.h>
#include <unistd.h>

int main(int argc, char const *argv[]){
	printf("%s,parent:%d,current:%d\n", "start", getppid(), getpid());
	pid_t fpid;
	fpid = fork();
	if (fpid < 0){ //error
		printf("%s:%d\n", "error", fpid);
	}else if (fpid == 0){ //child
		printf("%s,parent:%d,current:%d, fpid:%d\n", "child", getppid(), getpid(), fpid);
	}else{ //host
		printf("%s,parent:%d,current:%d, fpid:%d\n", "host", getppid(), getpid(), fpid);
	}
	return 0;
}
```

按理来说，结果应该是

	start,parent:15111,current:19431
    host,parent:15111,current:19431, fpid:19432
    child,parent:19431,current:19432, fpid:0

但是在 sublime 使用 CTRL + SHIFT + B 执行的时候，结果却是：

	start,parent:15111,current:19431
    host,parent:15111,current:19431, fpid:19432
	start,parent:15111,current:19431
    child,parent:19431,current:19432, fpid:0

<!-- more -->

其中 start 语句“貌似”被执行了两次，这显然是不可能的，问题就发生在 printf 上，以下几个原因集合到一起，就触发了这个看似怪异的结果：

1. fork 会 copy 父进程的 data space, heap 以及 stack，包括缓冲区。
2. 在使用 stdio 的时候, 如果 stdout 是面向终端（terminal），那么 stdout 是行缓冲的，否则，stdout 是全缓冲的。
3. printf 在 stdio 上操作，碰到 '\n' 的时候，会触发行缓冲机制，从而刷新缓冲区。
3. sublime 的终端不是一个标准终端，所以，即使遇到了 '\n'，依旧没有刷新缓冲区，结果子进程里面有一份与父进程相同的缓冲数据。

所以，为了保证在各种 stdout 上面的行为一致，最好还是在 fork 之前使用 

```c
fflush(stdout); 
```

主动刷新一次缓冲区

同理，在 C++ 里面有相同的问题。

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>
using namespace std;

int main(){
    cout << "Hi , " <<getpid() << endl;
    fork();
    return 0;
}

```

与

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>
using namespace std;

int main(){
    cout << "Hi , " <<getpid() << "\n";
    fork();
    return 0;
}

```

区别就是 endl 会强制刷新缓冲区，所以，在输出的时候还是一致使用 endl 比较妥当。

### 参考 
[http://stackoverflow.com/questions/21491826/cout-vs-printf-when-doing-fork](http://stackoverflow.com/questions/21491826/cout-vs-printf-when-doing-fork)
