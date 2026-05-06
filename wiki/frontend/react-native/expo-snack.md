---
title: Expo Snack
tags: [react-native, expo, sandbox]
date: 2026-05-06
sources:
  - "[[sources/posts/frontend/React/React Native/react-native-doc-site-stack-research]]"
last-ingested: 2026-05-06
status: draft
---

Expo 出品的开源浏览器内 RN 运行时，能把一段 React Native 代码动态打包后在 Web Player 跑、或在 Expo Go 里跑——并提供 iOS / Android tab 切换 + "My Device" tab 出 QR Code 让任意访客扫码到真机。**reactnative.dev 文档里的所有可交互示例都是 Snack iframe**。但**只能从公网 npm registry 拉依赖**，是它在内部 [[wiki/frontend/react-native/react-native-component-docs-stack|组件文档站]] 场景的致命缺口。

> [!note] 一句话定位
> Snack ≈ "RN 版 CodeSandbox + Expo Go 扫码"。强项是零门槛分享与扫码到设备；弱项是私有包。

## 核心能力

- **Web Player**：浏览器内编辑 + 即时渲染（react-native-web）
- **iOS / Android tab**：模拟器风格预览
- **My Device tab**：出 QR Code，[Expo Go](https://expo.dev/go) 扫码后真机原生运行
- **嵌入**：`<div data-snack-id="...">` 或 `data-snack-code` 内联代码，加载 `https://snack.expo.dev/embed.js` 后自动替换为 iframe

## 在 Docusaurus 里的集成（reactnative.dev 同款）

通过 [`remark-snackplayer`](https://github.com/darshkpatel/remark-snackplayer) 插件：

1. Build 时 visit 所有 `node.lang == 'SnackPlayer'` 的代码块
2. 替换为 `<div class="snack-player">` 占位
3. 客户端 `snackPlayerInitializer` 监听 Docusaurus 生命周期，调 Expo 的 `initSnackPlayers` 挂 iframe

````markdown
```SnackPlayer name=Hello World
import React from 'react';
import { Text, View } from 'react-native';
// ...
```
````

## 私有包卡点

Snack 依赖解析走 **公网 npm registry**。Snack SDK 通过 `missingDependencies` 字段报告缺失依赖，但只能从公网拉。

> [!warning] [官方论坛讨论](https://forums.expo.dev/t/installing-private-npm-packages-in-an-expo-snack/51319) 没有官方解
> 一位开发者公司内做 RN UI 库 + Docusaurus 文档站、SnackPlayer 跑通后想预览私有组件——卡死在私有包。

可行 workaround：

1. **inline 源码**：把组件源码塞 Snack `files` 字段。适合纯 JS 小组件，**不适合大库**。
2. **自托管 [snack-runtime](https://github.com/expo/snack)**：开源但要搭 npm proxy，运维成本高。
3. **库分公私两层**：public 部分发 npm，private 部分另行处理。

## 内部场景的替代方案

放弃 Snack，改用 [[wiki/frontend/react-native/storybook-react-native|on-device Storybook]] + Expo Go 扫码：

- 牺牲："任意访客零安装扫 URL"——团队成员需要装一次 Expo Go
- 收益：**私有包就是普通 workspace 依赖**，零摩擦；不依赖外部服务

详见 [[wiki/frontend/react-native/react-native-component-docs-stack|RN 组件文档站技术栈选型]] 决策矩阵。

## 延伸阅读

- [Expo Snack 主页](https://snack.expo.dev/)
- [snack/embedding-snacks.md（嵌入方式）](https://github.com/expo/snack/blob/main/docs/embedding-snacks.md)
- [snack/snack-sdk.md（SDK API）](https://github.com/expo/snack/blob/main/docs/snack-sdk.md)
- [remark-snackplayer 插件](https://github.com/darshkpatel/remark-snackplayer)
