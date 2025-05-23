---
layout: post
title: "React.js + vite的变量管理"
date: 2025-05-20 08:00:00 +0800
categories: fe
tag: [fe]
---

使用`vite` 构建项目时，管理变量的方式有如下几种：

1. 从`.env`等文件中读取;
2. 在`vite.config.js`中定义;
3. 通过命令行参数配置；
4. 从`package.json`等文件中读取并注入;

<!-- more -->

以上的几种方式，都可以将变量注入到项目中，但是注入的方式不同：

- 一类是注入到 `import.meta.env` ；
- 一类是注入为全局变量 ；

## 1. `.env`文件;

`vite` 会自动加载项目根目录下的 `.env` 文件，`.env` 文件中以 `VITE_` 开头的变量会自动注入到 `import.meta.env` 中，例如：

```bash
# .env
VITE_DEFAULT=".env"
VITE_NAME=".env"
```

加载完毕后，`import.meta.env` 中的变量如下：

```javascript
console.log(import.meta.env.VITE_DEFAULT); // .env
console.log(import.meta.env.VITE_NAME); // .env
```

多个 `.env` 文件等加载顺序如下：

1. `.env`；
2. `.env.local`；
3. `.env.[mode]`；
4. `.env.[mode].local`；

如果存在多个的 `.env` 文件，则后面的会覆盖前面的，例如：

```bash
# .env
VITE_DEFAULT=".env"
VITE_NAME=".env"
# .env.local
VITE_DEFAULT=".env.local"
VITE_NAME=".env.local"
```

加载完毕后，`import.meta.env` 中的变量如下：

```js
console.log(import.meta.env.VITE_DEFAULT); // .env.local
console.log(import.meta.env.VITE_NAME); // .env.local
```

如果要指定当前的模式（注意[与 `NODE_ENV` 的区别](https://vite.dev/guide/env-and-mode.html#node-env-and-modes)），可以在命令行中指定，例如：

```bash
vite --mode development # 默认加载 .env.development
vite --mode staging # 默认加载 .env.staging
```

## 2. 在`vite.config.js`文件中进行定义

`vite.config.js` 文件中可以配置 `define` 属性，该属性是一个对象，可以配置一些全局变量，例如：

```js
export default defineConfig({
  define: {
    "import.meta.env.VITE_VAR_1": `"[vite.config.ts]var_1"`,
    __VUE_I18N_LEGACY_API__: false,
    __VUE_I18N_FULL_INSTALL__: false,
    __INTLIFY_PROD_DEVTOOLS__: false,
  },
});
```

注意这里的差异：加载完毕后，`VITE_VAR_1` 会注入到`import.meta.env` ，而其他则是注入为**全局变量**：

```js
console.log(import.meta.env.VITE_VAR_1); // "[vite.config.ts]var_1"
console.log(__VUE_I18N_LEGACY_API__); // false
console.log(__VUE_I18N_FULL_INSTALL__); // false
console.log(__INTLIFY_PROD_DEVTOOLS__); // false
```

如果使用 `Typescript`，则配置文件是`vite.config.ts` ，同时需要在 `src/vite-env.d.ts` 中定义全局变量的类型：

```ts
// vite-env.d.ts
declare const __VUE_I18N_LEGACY_API__: boolean;
declare const __VUE_I18N_FULL_INSTALL__: boolean;
declare const __INTLIFY_PROD_DEVTOOLS__: boolean;

// 扩展 ImportMetaEnv 接口，实现智能提示
interface ImportMetaEnv {
  // Vite 默认环境变量
  readonly VITE_VAR_1: string;
}

// 扩展 ImportMeta 接口
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

## 3. 通过命令行参数进行配置

可以在命令行中指定环境变量，例如：

```bash
cross-env VITE_DEFAULT='[cli]default' VITE_NAME='[cli]name' vite
```

注：`cross-env`是一个跨平台设置环境变量的包，用来解决不同平台设置环境变量的问题。

执行命令后，`import.meta.env` 中的变量如下：

```js
console.log(import.meta.env.VITE_DEFAULT); // [cli]default
console.log(import.meta.env.VITE_NAME); // [cli]name
```

## 4. 从`package.json`等文件加载变量

这个方式其实还是第二种方法：`vite.config.js`中定义，只不过是从`package.json`中读取的，单独列出来是因为`package.json`是标准文件，有时候也用来配置自定义变量：。

`vite`默认不会读取 `package.json` 中的变量，如果需要读取，可以在 `vite.config.js` 中进行配置：

```js
impport pkg from "./package.json";
export default defineConfig({
  define: {
    "import.meta.env.APP_NAME": `"${JSON.stringify(
      pkg.name
    )}"`,
  },
});
```

注意：如果`package.json` 中的变量是字符串，则需要使用 `JSON.stringify` 进行包裹。 否则，会被解析为变量。

```json
//package.json
{
  "name": "vite-env-demo"
}
```

加载完毕后，`APP_NAME` 会注入到`import.meta.env` ，例如：

```js
console.log(import.meta.env.APP_NAME); // "vite-env-demo"
```

## 总结

如果一个变量同时通过`.env`、`vite.config.js`、`命令行参数`定义，则优先级如下：

- 优先级低：`.env`；
- 优先级中：`命令行参数`;
- 优先级高：`vite.config.js`；

[示例程序：https://github.com/xesam/react-dev-examples](https://github.com/xesam/react-dev-examples)

## 参考

1. [vite.config.js](https://vitejs.dev/config/)
2. [vite-env](https://vitejs.dev/guide/env-and-mode.html)
