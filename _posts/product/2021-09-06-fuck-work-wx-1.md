---
layout: post
title:  "对企业微信“加入群聊”功能的吐槽"
date:   2021-09-06 08:00:00 +0800
categories: product
tag: [product]
---
企业微信提供了一个“加入群聊”的功能，可以通过活码来建群，同时也打通了企业微信与微信。本来还算好用的，不过本周改版之后，
就体现出企业微信产品经理脱离实际业务太久了。

<!-- more -->

改版之前：

1. 群码是永久性的。
2. 一个群码可以关联5个外部群。
3. 每个群码可以单独配置新群的命名规则。


改版之后：

1. 群码是永久性的。
2. 一个群码可以关联5个外部群。
3. 每个群码可以指定一个模板。

主要的改变就是把新群的配置策略全部放到“模板”这个新的对象上了。
本来机制挺好的，但是由于官方加了几个限制，导致使用起来非常恶心。限制如下：

1. 企业管理员通过web后台只能创建100个模板，超过这个数量之后，管理员无法再创建新的模板。不过，虽然限制了管理员，还好每个企业成员也可以创建100个模板。但是！成员创建的模板，无法指定新群的群名称。
2. 拥有外部联系人权限的企业成员也可以通过客户端的“加入群聊”创建群码，但是！一旦创建完成，就意味着永远没有办法编辑这个群码，真的是“永远”，因为根本就没有提供再次查看的入口。于是就出现了成员看不见，管理员也看不见的窘境！哪怕提供一个api管理也行啊。
3. 模板的设计无法理解。以前群码新建群聊码的时候，可以独立配置新群的命名规则。现在把命名的部分挪到模板中，就意味着模板失去了重用性。如果管理员创建了一个带有命名配置的模板，根本不可能下发给成员，因为成员不需要这个名字；而如果管理员创建了一个不带命名部分的模板，下发给成员之后，那成员新扩建的群，名字全都是“未命名群聊”。一个模板只能用于一个群聊码，那“模板”还有什么意义呢？

