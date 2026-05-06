# React Native 组件文档站技术栈调研（2026.05）

> 调研背景：要为内部 React Native 组件库搭一个文档站，需求：
> 1. 组件文档站
> 2. 实时展示每个组件样式（参考 Storybook）
> 3. 扫码在 Android / iOS 设备上看效果（参考 reactnative.dev FlatList 页面）
> 4. 存在内部私有包

> 约束收敛后：
> - 仅内部团队访客
> - "扫码能看就行"，不要求任意访客零安装扫码
> - 没有现成 RN 工程，可新建

---

## TL;DR

业界没有"开箱即用同时满足 4 条要求"的方案。reactnative.dev 走的是 **Docusaurus + Expo Snack Player**，但 Snack 不支持私有包；Storybook 原生支持私有包，但不能像 Snack 那样给 URL 让任意人扫码。

**最终推荐**（结合内部团队 + 可新建工程的约束）：

> 一个 **Expo SDK 52+ 工程**，pnpm workspace monorepo，同时跑 **Storybook 8.5+ for React Native Web (Vite)**（浏览器文档站）+ **on-device Storybook**（Expo Go 扫码看真机），两套 Storybook 共享同一份 `*.stories.tsx`。**不需要 Docusaurus、不需要 Snack**。

---

## 一、业界主流方案对比

### 1. Docusaurus + Expo Snack（reactnative.dev 同款）

reactnative.dev 自身就是 Docusaurus，集成方式是一个叫 [`remark-snackplayer`](https://github.com/darshkpatel/remark-snackplayer) 的 remark 插件：

- 把 ` ```SnackPlayer ` 代码块在 build 时替换成 `<div class="snack-player">` 占位符
- 客户端 `snackPlayerInitializer` 模块挂 Docusaurus 生命周期，调用 Expo 的 `initSnackPlayers` 挂载 iframe
- iframe 内提供 Web / iOS / Android tab 切换，"My Device" tab 出 QR Code 由 Expo Go 扫描

**优点**：体验最好，浏览器实时编辑 + 三平台预览 + 任意访客扫码。

**致命缺点（对你的场景）**：Expo Snack 只能从公网 npm registry 拉依赖。[官方论坛上有人问过同样问题](https://forums.expo.dev/t/installing-private-npm-packages-in-an-expo-snack/51319)，没有官方支持的私有包方案。Workaround：

1. 把组件源码 inline 到 Snack `files` 字段（适合纯 JS 小组件，不适合大库）
2. 自托管 [snack-runtime](https://github.com/expo/snack)（开源但运维成本高，要搞 npm proxy 才能拉私有包）
3. 把库分成 public + private 两层，public 部分发 npm

### 2. Storybook for React Native（2026 现状）

2026 年 Storybook 在 RN 圈分两条路，**两条路可以并存**：

#### 2.1 Storybook for React Native Web (Vite)

- Storybook 8.5+ 推荐用 Vite framework（**不是**老的 webpack 版 `@storybook/addon-react-native-web`）
- 用 react-native-web 把组件转 DOM，浏览器里跑
- 文档站质感、可发布、支持 MDX、Autodocs，500+ addons
- **支持私有包**：就是普通 npm/workspace 依赖，Vite 装上就用

#### 2.2 On-device Storybook（`@storybook/react-native`）

架构上不一样：**Storybook 在 RN 里是一个 Component，渲染在你的 App 内**，需要环境变量切换 App / Storybook 模式。

- 能跑原生模块、真实设备渲染
- 在 Expo 工程里执行 `expo start`，终端给 QR Code，Expo Go 扫即可
- 必备 on-device addons：`@storybook/addon-ondevice-controls`（动态改 props）、`@storybook/addon-ondevice-actions`（事件日志）
- 支持多设备 WebSocket 同步（一处改 args，所有连接设备同步）

**对比 Snack**：on-device Storybook 不能像 Snack 那样"任意访客扫 URL 即开"——团队成员需要装 Expo Go，连同一网络。但**支持私有包零成本**，且不依赖外部服务。

### 3. 其它候选（被排除）

- **Ladle**：Storybook 替代品、Vite 极快，但 React Native 生态支持弱，没有 on-device 方案
- **rnx-kit / Pagoda**：Microsoft 的 RN 工具链，偏构建，不解决文档展示
- **Bit.dev / Component Studio**：商业平台，私有部署贵，over-engineering

---

## 二、关键技术点

### Docusaurus 是文档外壳事实标准

reactnative.dev、react-native-paper、react-native-elements、react-native-echarts 等知名库的文档站都是 Docusaurus。优势是首页、博客、changelog、版本切换、i18n 都现成。

但**第一版做内部库没必要**：Storybook 8.5+ 的 Autodocs + MDX 已经能当独立文档站用，少一层抽象少一份维护。等组件库成熟、要做对外开发者门户时再套 Docusaurus 也不迟。

### Storybook 关键配置坑（避免踩雷）

1. **`@storybook/*` 包必须同 major 版本**，混用会运行时崩
2. **Metro 必须包 `withStorybook()`**，否则 stories glob 不生效：
   ```js
   const { getDefaultConfig } = require('expo/metro-config');
   const { withStorybook } = require('@storybook/react-native/metro/withStorybook');
   module.exports = withStorybook(getDefaultConfig(__dirname));
   ```
3. **Reanimated plugin 必须是 babel.config.js 最后一个 plugin**，且需清缓存重启
4. **App / Storybook 切换用环境变量**（如 `STORYBOOK=1 expo start`），不要用代码注释切
5. **Web 端用 Vite framework**，不要再用废弃的 `@storybook/addon-react-native-web`（webpack 版）

### Story 写法（CSF 3 + TypeScript）

```ts
import type { Meta, StoryObj } from '@storybook/react-native';
import { Button } from './Button';

const meta = { component: Button } satisfies Meta<typeof Button>;
export default meta;

type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { label: 'Click me', variant: 'primary' },
};
```

- Story 文件与组件文件同目录（co-location）
- 用 `Meta` / `StoryObj` 泛型获得 args 类型推导
- decorators 提供共享上下文（theme、padding、provider）

### Atomic Design 组织组件

社区共识：组件按 atoms → molecules → organisms 分层。Storybook sidebar 自然形成层级，新人易理解，缩放性好。

### Storybook 2026 新东西

- **MCP server**：Storybook 起了 `/mcp` endpoint，AI 工具（Claude）可以查询 component / story metadata，配合 AI 写 stories
- **多设备 WebSocket 同步**：on-device 多端同步 stories 选择和 args

---

## 三、推荐架构（最终方案）

### 目录结构（pnpm workspace monorepo）

```
my-rn-ui/
├── package.json                 # pnpm workspaces 根
├── pnpm-workspace.yaml
├── packages/
│   ├── ui/                      # 组件库本体（私有 workspace 包 @myorg/ui）
│   │   ├── src/
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   └── Button.stories.tsx     # 唯一一份 story
│   │   │   ├── Input/
│   │   │   └── ...
│   │   └── package.json
│   └── storybook-host/          # Expo app，承载两套 Storybook
│       ├── .storybook/          # on-device 配置（main.ts / preview.ts）
│       ├── .rnstorybook-web/    # web 配置（Vite framework）
│       ├── App.tsx              # ENV 切换 App / on-device Storybook 入口
│       ├── metro.config.js      # withStorybook() wrapper
│       ├── babel.config.js      # reanimated plugin 在最后
│       └── package.json
```

`packages/ui` 里组件和 stories 同文件夹（atomic 规范），`storybook-host` 通过 stories glob 把 `../ui/src/**/*.stories.tsx` 都吸进来。**两套 Storybook 共享同一批 story 文件**，不写两遍。

### 团队两种使用姿势

**浏览器看（PM、设计、QA、code review）**

```bash
pnpm --filter storybook-host storybook
```

Vite dev server 起 web 版 Storybook，react-native-web 把组件渲染成 DOM。Controls panel 实时改 props，Autodocs 自动出组件文档页。**这就是"文档站"**。

**真机看（开发本地、Native 模块组件验证）**

```bash
pnpm --filter storybook-host start  # 等价 expo start
```

终端打印 QR Code → Expo Go 扫 → on-device Storybook 启动。可在 iOS/Android 真机切换 stories、改 controls。**完全替代 Snack 的扫码体验**，私有包就是本地 workspace 依赖，零摩擦。

### 后续可选演进

- **想要更"文档站"质感**（首页、导航、博客、changelog、版本切换）再在外面套 Docusaurus，把 Storybook build 产物挂子路径。第一版没必要。
- **内网部署 web Storybook**：`storybook build` 出纯静态产物，丢任何静态站点（Vercel、内网 nginx、GitHub Pages 私有 repo）即可。
- **CI 视觉回归**：Chromatic / Percy / Lost Pixel 接 web 版 Storybook 做 snapshot diff。
- **多设备同步 review**：用 Storybook on-device 的 WebSocket 同步功能，组件 review 会议上多人多机同步。

---

## 四、决策矩阵

| 方案 | 浏览器实时预览 | QR 扫码到设备 | 私有包 | 工作量 | 适用场景 |
|---|---|---|---|---|---|
| Docusaurus + Expo Snack | ✅ | ✅ 任意访客扫码 | ❌ | 低 | 公开库（如 reactnative.dev、Paper） |
| **Expo + Storybook RN Web + on-device** ⭐ | ✅ | ✅ 装 Expo Go 后扫码 | ✅ | 中 | **内部组件库（本场景）** |
| Docusaurus + Storybook iframe + Showcase App | ✅ | ✅ 装自家 App 扫码 deep link | ✅ | 高 | 大型内部产品组件库，需要门户级文档 |
| 自托管 Snack Runtime + npm proxy | ✅ | ✅ 任意访客扫码 | ✅ | 极高 | 必须复刻 reactnative.dev 体验且接受运维 |

---

## 五、参考资料

- [Storybook for React Native Web (Vite)](https://storybook.js.org/docs/get-started/frameworks/react-native-web-vite) — 官方 framework 文档
- [@storybook/react-native GitHub](https://github.com/storybookjs/react-native) — on-device Storybook 主仓库
- [Writing stories | React Native Storybook](https://storybookjs.github.io/react-native/docs/intro/writing-stories/) — CSF 写法
- [remark-snackplayer](https://github.com/darshkpatel/remark-snackplayer) — reactnative.dev 同款 Docusaurus 插件
- [Expo Snack embedding 官方文档](https://github.com/expo/snack/blob/main/docs/embedding-snacks.md) — `data-snack-id` / `data-snack-code` 嵌入方式
- [Expo Snack SDK 文档](https://github.com/expo/snack/blob/main/docs/snack-sdk.md) — `missingDependencies` 等 API
- [Expo 论坛：Snack 装私有包讨论](https://forums.expo.dev/t/installing-private-npm-packages-in-an-expo-snack/51319) — 私有包卡点的官方讨论
- [Callstack: A Better DX with Expo Snack](https://www.callstack.com/case-studies/expo) — Snack 在 Paper 文档站的应用
- [掘金：为 React Native 库搭建一个现代文档网站](https://juejin.cn/post/7214901105977638949) — 中文实践参考
- [Storybook for React Native tutorial](https://storybook.js.org/tutorials/intro-to-storybook/react-native/en/get-started/) — 官方零到一教程

---

调研日期：2026-05-06
