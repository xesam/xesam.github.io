---
layout: post
title:  "【computer】C++与Java简单对比"
date:   2016-01-02 08:00:00 +0800
categories: computer
tag: [computer]
---

<table>
    <caption>类访问权限</caption>
    <thead>
    <tr>
        <th></th>
        <th>C++</th>
        <th>Java</th>
    </tr>
    </thead>
    <tboady>
        <tr>
            <td>类默认权限</td>
            <td>私有</td>
            <td>包访问</td>
        </tr>
        <tr>
            <td>私有</td>
            <td>private</td>
            <td>private</td>
        </tr>
        <tr>
            <td>受保护</td>
            <td>protected</td>
            <td>protected</td>
        </tr>
        <tr>
            <td>公开</td>
            <td>public</td>
            <td>public</td>
        </tr>
        <tr>
            <td>友元</td>
            <td>friend</td>
            <td>不支持</td>
        </tr>
    </tboady>
</table>
<table>
    <caption>继承体系</caption>
    <thead>
    <tr>
        <th></th>
        <th>C++</th>
        <th>Java</th>
    </tr>
    </thead>
    <tboady>
        <tr>
            <td>多态方法</td>
            <td>virtual（虚函数）</td>
            <td>非静态，非私有方法</td>
        </tr>
        <tr>
            <td>要求子类实现的方法</td>
            <td>pure virtual（纯虚函数）</td>
            <td>abstract（抽象方法）</td>
        </tr>
        <tr>
            <td>接口</td>
            <td>完全纯虚函数</td>
            <td>interface</td>
        </tr>
        <tr>
            <td>多重继承</td>
            <td>支持</td>
            <td>不支持</td>
        </tr>
    </tboady>
</table>