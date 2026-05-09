---
title: Storybook for React Native
tags: [react-native, storybook, documentation]
date: 2026-05-06
sources:
  - "[[sources/posts/frontend/React/React Native/react-native-doc-site-stack-research]]"
last-ingested: 2026-05-06
status: stable
---

Storybook 在 React Native 圈 2026 年分两条可并存的路：**Storybook for React Native Web (Vite)** 把组件转 DOM 在浏览器跑（适合做文档站），**On-device Storybook** 作为 Component 渲染在 RN App 内（适合真机验证、跑原生模块）。这两条路通常在同一工程里同时启用，共享同一份 [[wiki/frontend/react-native/csf-story-format|CSF stories]]，**是内部 [[wiki/frontend/react-native/react-native-component-docs-stack|RN 组件文档站]] 的事实首选**。

> [!note] 与其它 Storybook 的关键差异
> 在 React 等框架里 Storybook 自己是独立进程；在 RN 里 Storybook 是**一个你渲染在 App 里的 Component**，需要环境变量切换 App / Storybook 入口。这条架构差异决定了所有配置坑。

## 两种形态对比

> [!compare] Web vs On-device
> | | Storybook RN Web (Vite) | On-device Storybook |
> |---|---|---|
> | 包 | `@storybook/react-native-web-vite` | `@storybook/react-native` |
> | 渲染 | react-native-web → DOM | 真实 RN 渲染 |
> | 看法 | 浏览器打开 URL | 装 Expo Go 扫 QR / 装 dev build |
> | 原生模块 | 不支持（依赖宿主） | 完全支持 |
> | Addons 生态 | 500+（web 全套） | on-device 子集（controls / actions） |
> | 适合 | 文档站、设计 review、对外分享 | 真机验证、原生组件、a11y 真实测 |

**选型默认**：内部组件库**两个都开**，浏览器看 + 扫码看，不互相替代。

## On-device 必备 addons

```ts
addons: [
  '@storybook/addon-ondevice-controls',  // 动态改 props
  '@storybook/addon-ondevice-actions',   // 事件日志（按下、focus 等）
],
```

支持**多设备 WebSocket 同步**：起 WebSocket server，多设备连上后切换 story / 改 args 全部同步——团队 review 时多人多机同步。

## 关键配置坑（避免踩雷）

> [!warning] 五条铁律
> 1. **`@storybook/*` 包必须同 major 版本**，混用会运行时崩；从 9 升 10 走官方迁移指南
> 2. **Metro 必须包 `withStorybook()`**，否则 stories glob 不工作：
>    ```js
>    const { getDefaultConfig } = require('expo/metro-config');
>    const { withStorybook } = require('@storybook/react-native/metro/withStorybook');
>    module.exports = withStorybook(getDefaultConfig(__dirname));
>    ```
> 3. **Reanimated plugin 必须是 `babel.config.js` 最后一个 plugin**，且需清缓存重启
> 4. **App / Storybook 切换用环境变量**（如 `STORYBOOK=1 expo start`），不要用代码注释切
> 5. **Web 端用 Vite framework**，不要再用废弃的 webpack 版 `@storybook/addon-react-native-web`

## 2026 新东西

- **MCP server**：Storybook 起 `/mcp` endpoint，AI 工具（如 Claude）能查询 component / story metadata，配合 [[wiki/claude-code/mcp|MCP]] 让 AI 写 stories
- 官方还出了 Claude-specific 指南，覆盖 [[wiki/frontend/react-native/csf-story-format|CSF]]、Expo / Expo Router / RN CLI / Re.Pack 集成、5.3.x → 10.x 增量升级

## 与 Snack 的对比

[[wiki/frontend/react-native/expo-snack|Expo Snack]] 给的是"任意访客扫 URL 即开"的零门槛体验，但卡在私有包不支持。On-device Storybook 反过来：团队成员要装 Expo Go、连同一网络，但**私有包零成本**（就是普通 workspace 依赖），且不依赖外部服务。

详见 [[wiki/frontend/react-native/react-native-component-docs-stack|RN 组件文档站技术栈选型]]。

## 延伸阅读

- [Storybook for React Native Web (Vite) 官方文档](https://storybook.js.org/docs/get-started/frameworks/react-native-web-vite)
- [@storybook/react-native GitHub](https://github.com/storybookjs/react-native)
- [Writing stories | React Native Storybook](https://storybookjs.github.io/react-native/docs/intro/writing-stories/)
- [Storybook for React Native tutorial](https://storybook.js.org/tutorials/intro-to-storybook/react-native/en/get-started/)
