---
layout: post
title:  "可维护的配置 1"
date:   2021-09-05 09:00:00 +0800
categories: product
tag: [product]
---

场景描述：

> 一群门店给一群园区送外卖，不同门店营业时间不同，不同园区允许外卖进入的时间段也不一样。同时，由于门店与不同园区之间的距离有远有近，所以并不是每个门店都能服务所有的园区，也不是每个园区都能点所有门店的外卖。有的门店可能会因为某些不可预计的原因临时闭店，从而无法按照预期提供外卖服务。

<!-- more -->

现在想要把这些约束关系尽可能简单的配置起来。

### 门店
门店的基本配置项：

1. 营业日期。
2. 营业时间。
3. 营业状态（正常营业/暂停营业）。

### 园区

园区的基本配置项：

1. 允许外卖进入的日期。
2. 允许外卖进入的时间段。
3. 园区开放状态（正常开放/疫情管控）。

### 门店&园区

1. 生效日期。
2. 生效时间。
3. 生效状态（启用/禁用）。

在配置理解之前，有几个问题需要先明确。

#### 一、 如何配置日期？
最精确的当然是配置到每一天，但是这样有比较多的问题：1. 日期是无限的。2. 修改不便。
所以综合考虑下来，像闹钟一样配置星期的重复模式就够用了。如果在此重复模式下，需要临时调整，就通过各项的状态开关进行手动控制。

#### 二、 门店&园区上配置的日期和时间，是什么作用？
这个配置有多种理解：

1. 不论门店或者园区上是如何配置的，一切以 门店&园区 上的配置为准。
2. 门店配置 与 园区配置 与 门店&园区配置，这三者取交集。交集规则：日期与日期计算，时间与时间计算，不然就无限了。

不同的理解有不同的优劣势。如果我们遵循第一种理解，优势是简单直接，实现也简单。但是缺点也很明显：如果门店延长或者缩短了营业时间之后，实际情况就与配置情况不一致了，要么导致门店实际服务时间比实际短了，要么导致用户看到可以下单，但实际门店并不能服务。如果我们遵循第二种理解，优势是可以自动伸缩，缺点就是无法直观的看出最终生效的结果到底是怎样的。

#### 三、 如果不配置，默认值应该是多少？
门店：

    日期：周一到周日。
    时间：00:00 - 23:59 。

园区：

    日期：周一到周日。
    时间：00:00 - 23:59 。

至于门店&园区配置的默认值，对于不同的理解，应该有不同的默认值：如果“一切以 门店&园区 上的配置为准”，理应以创建当时 门店配置 与 园区配置 的交集为默认值。否则，应该以 

    日期：周一到周日。
    时间：00:00 - 23:59 

作为默认值。

配置完成之后，一个门店在某个时间能否为某个社群提供外卖服务，取决于三项配置共同作用的结果。

#### 示例
门店A在1月1号在10:00 - 13:00之间正常营业， 园区在1月1日在12:00 - 14:00之间正常开放。在没有其他配置情况下，门店1月1号就只能在12:00-13:00之间为园区 B 提供外卖服务。

