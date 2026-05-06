---
title: React Native 组件文档站技术栈选型
tags: [react-native, documentation, storybook]
date: 2026-05-06
sources:
  - "[[sources/posts/frontend/React/React Native/react-native-doc-site-stack-research]]"
last-ingested: 2026-05-06
status: draft
---

业界没有"开箱即用同时满足组件文档 + 实时预览 + 扫码到设备 + 私有包"的单一方案。reactnative.dev 走 Docusaurus + [[wiki/frontend/react-native/expo-snack|Expo Snack]] 路线，但 Snack 不支持私有包；[[wiki/frontend/react-native/storybook-react-native|Storybook for React Native]] 原生支持私有包，但不能像 Snack 那样给 URL 让任意访客零安装扫码。**内部组件库的甜点方案**：Expo + Storybook 双形态（Web Vite + on-device），用 Expo Go 扫码看真机。

> [!note] 四象限决策
> 选型核心是两条轴：**访客是否需要零安装扫码** × **是否有私有包**。两条轴决定方案。

## 决策矩阵

> [!compare] 四种主流组合
> | 方案 | 浏览器实时预览 | QR 扫码到设备 | 私有包 | 工作量 | 适用场景 |
> |---|---|---|---|---|---|
> | Docusaurus + Expo Snack | ✅ | ✅ 任意访客零安装 | ❌ | 低 | 公开库（reactnative.dev、react-native-paper） |
> | **Expo + Storybook 双形态** ⭐ | ✅ | ✅ 装 Expo Go 后扫 | ✅ | 中 | **内部组件库** |
> | Docusaurus + Storybook iframe + Showcase App | ✅ | ✅ 装自家 App 扫 deep link | ✅ | 高 | 大型内部产品组件库，要门户级文档 |
> | 自托管 Snack Runtime + npm proxy | ✅ | ✅ 任意访客 | ✅ | 极高 | 必须复刻 reactnative.dev 体验且接受运维 |

## 推荐架构（Expo + Storybook 双形态）

**单 Expo SDK 52+ 工程 + pnpm workspace monorepo**，同时跑两套 Storybook，共享同一份 `*.stories.tsx`：

```
my-rn-ui/
├── packages/
│   ├── ui/                      # 私有 workspace 包 @myorg/ui
│   │   └── src/Button/Button.tsx + Button.stories.tsx
│   └── storybook-host/          # Expo app
│       ├── .storybook/          # on-device 配置
│       └── .rnstorybook-web/    # Web Vite 配置
```

> [!example] 团队两种使用姿势
> - **浏览器看**（PM/设计/QA/CR）：`pnpm --filter storybook-host storybook` → Vite 起 web 版，react-native-web 渲染成 DOM，Controls 实时改 props。
> - **真机看**（开发本地、Native 模块验证）：`pnpm --filter storybook-host start` → Expo 终端打 QR → Expo Go 扫码 → on-device Storybook 启动。

私有包就是普通 workspace 依赖，零摩擦。**完全替代 [[wiki/frontend/react-native/expo-snack|Snack]] 的扫码体验**，且不依赖外部服务。

## 为什么不用 Docusaurus（第一版）

reactnative.dev、react-native-paper、react-native-elements、react-native-echarts 都是 Docusaurus，优势是首页 / 博客 / changelog / 版本切换 / i18n 现成。但**内部库第一版没必要**：[[wiki/frontend/react-native/storybook-react-native|Storybook]] 8.5+ 的 Autodocs + MDX 已经能当独立文档站用，少一层抽象少一份维护。等组件库成熟、要做对外开发者门户时再外套 Docusaurus 也不迟。

## 被排除的候选

- **Ladle**：Vite 极快的 Storybook 替代品，但 RN 生态支持弱，没有 on-device 方案
- **rnx-kit / Pagoda**（Microsoft）：偏构建工具链，不解决文档展示
- **Bit.dev / Component Studio**：商业平台，私有部署贵，over-engineering

## 后续可选演进

- **想要门户质感**：外套 Docusaurus，把 Storybook build 产物挂子路径
- **内网部署 web 版**：`storybook build` 出静态产物，丢内网 nginx / 私有 GitHub Pages
- **CI 视觉回归**：Chromatic / Percy / Lost Pixel 接 web 版 Storybook 做 snapshot diff
- **多设备同步 review**：用 [[wiki/frontend/react-native/storybook-react-native|on-device Storybook]] 的 WebSocket 同步功能，会议上多人多机同步切换 stories

## 延伸阅读

- [Storybook for React Native Web (Vite)](https://storybook.js.org/docs/get-started/frameworks/react-native-web-vite)
- [Callstack: A Better DX with Expo Snack](https://www.callstack.com/case-studies/expo)
- [掘金：为 React Native 库搭建一个现代文档网站](https://juejin.cn/post/7214901105977638949)
