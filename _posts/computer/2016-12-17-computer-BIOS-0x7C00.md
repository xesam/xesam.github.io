---
layout: post
title:  "BIOS与0x7C00"
date:   2016-12-17 08:00:00 +0800
categories: computer
tag: [computer]
---
## 神秘的 0x7C00

你知道 0x7C00，这个在 x86 汇编中的一个神秘数字吗？
0x7C00 是一个内存地址，BIOS 就是将 MBR (Master Boot Record, hdd/fdd 的第一个 sector) 读入 0x7C00 这个地址，
然后进行后续引导的。

操作系统或是 bootloader 的开发者必须假设他们的汇编代码被加载并从 0x7C00 处开始执行。
不过，为什么在 x86 中 BIOS 要将 MBR 加载到 0x7C00 呢？在回答这个问题之前，我们还有几个疑惑：

第一个疑惑：

    我翻阅了所有的 Intel x86(32bit) 编程手册，都没有找到 0x7C00 这个数字。

没错！0x7C00 不是 x86 CPU 里面的定义，你当然不可能在 cpu 文档里面找得到。那么你就要问了，“那是谁定义了 0x7C00？”

第二个疑惑：

    0x7C00 的值等于 32KiB - 1024B，这个数字表示什么意思？

不管是谁定义了 0x7C00，他/她为何要定义这样一个奇怪的数字？

## 0x7C00 第一次在哪里？

0x7C00 第一次出现是在 IBM PC 5150 的 BIOS int 19 处理程序（中断类型码为 19 的中断处理程序）中。

回顾一下 x86 IBM PC 兼容机的历史：
IBM PC 5150是 x86（32位）IBM PC/AT系列的祖先，这款 PC 于1981年8月发布，使用 intel 8088（16位） 处理器和 16KiB 大小的 RAM，
其 BIOS 以及微软 BASIC 均放在 ROM 中。

上电之后，BIOS 就开始"POST"(Power On Self Test，自检) ，然后触发 int 19 中断，在处理19号中断时，
BIOS 检测电脑是否具有软盘、硬盘或是其他固定磁盘，如果发现任何有效的磁盘，BIOS 就把磁盘第一个扇区（512B）的内容加载到内存的 0x7C00 地址处。

现在知道为何在 x86 文档中找不到 0x7C00 了吧，因为这个数字属于 BIOS 规范。

## 0x7C00 的起源

围绕IBM PC DOS，Microsoft 和 SCP的86-DOS 三者有一个故事，参见：[MS-DOS简史](http://www.patersontech.com/dos/byte%E2%80%93history.aspx)。

在1979年，Digital Research Inc 还没有为当时的 8086/8088 cpu开发 CP/M，于是在 1980年，SCP 发布了一个用于 8086/8088 cpu 的 CP/M 兼容 OS，即 SCP的“86-DOS”。
这个 “86-DOS” 成了后来 IBM PC DOS 1.0 的参照系统。

当时 SCP 出售两种 S-100 总线板，一种是 8086 CPU 板，另一种是 “CPU Monitor” ROM 板。
“CPU Monitor” 提供了引导加载程序（bootloader）和调试器（debugger），
当时，这个“CPU Monitor”引导加载程序将 MBR 加载到“0x200”，而不是“0x7C00”。

到了1981年，另一款用于8086/8088 的类 CP/M 操作系统，IBM PC DOS 发布，不过，与 86-DOS 不同的是， IBM PC DOS 选择将 MBR 加载到“0x7C00”
所以，我们说“0x7C00 第一次出现是在 IBM PC 5150 ROM BIOS”，在此之前，SCP 的 CPU Monitor 引导加载程序是加载到 0x200，而不是 0x7C00。

## 为什么 CPU Monitor 的 引导加载程序将 MBR 加载到 "0x200" ?

这种设计基于以下三点考虑：

1. 8086 的中断向量表占用了 0x0 - 0x3FF
2. 86-DOS 从 0×400 处被加载；
3. 86-DOS 不使用 0×200-0x3FF 这段中断向量地址

这意味着 0×200-0x3FF 这段地址被保留，不论 86-DOS 还是其他应用程序，都不能使用这段地址。
因此，Tim Paterson（86-DOS开发者）选择 0×200 作为 MBR 的加载地址。

## 谁决定使用 0x7C00？
魔数 0x7C00 诞生于1981年，是被 IBM PC 5150 BIOS 开发团队(Dr. David Bradley)定义的，
而不是英特尔（8086/8088 供应商）或微软（操作系统供应商）决定的。后来， “IBM PC/AT 兼容机” PC/BIOS 供应商也沿用了这个值，保留了 BIOS 和操作系统的向后兼容性。

## "0x7C00 = 32KiB - 1024B" 表示什么意思？

IBM PC 5150 最小内存模型只有 16KiB RAM。所以，你可能会问：

    “最小内存模型（16KiB）能从磁盘加载操作系统吗？如果 BIOS 要将 MBR 加载到 32KiB - 1024B 地址，那物理内存显然不够...”

不行，这种情况不在考虑范围内。 IBM PC 5150 ROM BIOS 开发团队成员之一，David Bradley博士说：

    “DOS 1.0需要至少32KiB，所以我们不关心在 16KiB 机器上的引导。

（注：我现在无法确认 DOS 1.0 的最低内存要求到底是 16KiB 还是 32KiB？但是，至少在1981年的早期 BIOS 开发中，他们认为 32KiB 是 DOS 的最低要求）

BIOS开发团队决定使用地址 0x7C00，是因为：

1. 他们想在 32KiB 范围内，留出尽可能多的空间让操作系统加载自己。
2. 8086/8088使用 0x0 - 0x3FF 作为中断向量，并且 BIOS 数据区在它之后。
3. 引导扇区为512字节，引导程序的堆栈/数据区需要512字节。
4. 因此，这 32KiB 中从 0x7C00 开始的最后 1024B 被选中了。

一旦操作系统加载和启动完毕后，直到电源复位，引导扇区都不会被使用。因此，操作系统和应用程序可以自由使用 32KiB 的这最后 1024B。

操作系统加载后，内存分布情况如下：

    +--------------------- 0x0000
    | Interrupts vectors
    +--------------------- 0x4000
    | BIOS data area
    +--------------------- 0x5???
    | OS load area
    +--------------------- 0x7C00
    | Boot sector
    +--------------------- 0x7E00
    | Boot data/stack
    +--------------------- 0x7FFF
    | (not used)
    +--------------------- (...)

这就是 0x7C00 的历史渊源，这个魔数在 PC/AT 兼容 BIOS 的 INT 19h 中断处理程序中延续了了近三十年。

[Why BIOS loads MBR into 0x7C00 in x86](http://www.glamenv-septzen.net/en/view/6)
