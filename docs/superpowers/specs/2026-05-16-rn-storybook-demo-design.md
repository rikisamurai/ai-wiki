---
title: rn-storybook-demo 设计
date: 2026-05-16
status: draft
---

# rn-storybook-demo 设计

## 背景

参考 [`react-native-doc-site-stack-research`](../../../sources/posts/frontend/React/React%20Native/react-native-doc-site-stack-research.md)（2026-05-06 调研）推荐的 **Expo + Storybook RN Web (Vite) + on-device Storybook** 方案，在 `/Users/shanyulong/riki/repo/rn-storybook-demo` 新建一个最小可跑的 monorepo demo，用真实代码验证方案是否成立。

调研写于 2026-05-06；2026-05-16 重新核实版本生态后，与调研当时的版本基线已差出多个 major（Expo SDK 52 → 55、Storybook 8.5+ → 10.4+）。本 spec 采用 **2026-05-16 时点的全部最新稳定版本**，避免在老版本上做"考古式"验证。

## 目标与「跑通」的硬验证项

demo 要回答的核心命题：source 推荐的「同一份 `*.stories.tsx` 物理唯一、被两套 Storybook 引擎（on-device + web）同时消费」方案在最新 Expo + Storybook 生态下是否成立。

完成的客观判定（详见 §8 verification checklist）：

1. `pnpm dev:web` 起 Vite Web Storybook，浏览器看到 5 个组件、controls 实时改 props、Autodocs 自动出文档
2. `pnpm dev:device` 起 Expo dev server，QR 用 Expo Go 扫，能在真机看到 on-device Storybook，能切 stories 和改 controls
3. 5 份 `*.stories.tsx` 物理上只写一份（`packages/ui` 内），两套 Storybook 都消费同一份
4. `EXPO_PUBLIC_STORYBOOK=1 expo start` 与 `expo start` 能切换 on-device SB 与业务占位 App 入口
5. 内部私有包能力靠 `pnpm workspace` 的 `@myorg/ui` 引用本地 `packages/ui` 体现

## Out of scope

- 不套 Docusaurus 外壳（source §三明确建议第一版不做）
- 不接 Chromatic / Percy 视觉回归
- 不接 CI workflow
- 不写真实业务 App（业务占位只是一句文字 + 一个按钮）
- 不发 npm（`@myorg/ui` 只是 workspace 私有包）
- 5 个组件实现只追求"能渲染、能交互"，不追求生产级样式与可访问性

---

## §1 架构总览

单仓库 + 双 package + 双 Storybook 引擎共享同一份 stories：

```
                    ┌─────────────────────────────────────────────┐
                    │  packages/ui  (workspace 私有包 @myorg/ui)   │
                    │                                              │
                    │  src/atoms/button/                           │
                    │       button.tsx                             │
                    │       button.stories.tsx ◄────┐              │
                    │  src/atoms/input/             │              │
                    │  src/atoms/avatar/            │ 唯一一份     │
                    │  src/molecules/card/          │ stories      │
                    │  src/molecules/list-item/     │              │
                    └───────────────────────────────┼──────────────┘
                                                    │
                    ┌───────────────────────────────┼──────────────┐
                    │  packages/storybook-host (Expo SDK 55 工程) │
                    │                               │              │
                    │  .storybook/main.ts ──────────┘              │ ← on-device 引擎
                    │  .storybook-web/main.ts ──────┘              │ ← Web Vite 引擎
                    │  app.tsx (ENV 路由 业务 / SB)                │
                    │  metro.config.js (withStorybook 包裹)        │
                    │  babel.config.js (reanimated plugin 最末)    │
                    └──────────────────────────────────────────────┘

  两个引擎的 stories glob 都指向 ../../ui/src/**/*.stories.tsx
```

**核心机制**：

- stories 物理唯一，写在 `packages/ui` 跟组件同目录（atomic co-location）
- 两个 Storybook 引擎都跨 package 吸 stories：on-device 是 `@storybook/react-native`、Web 是 `@storybook/react-native-web-vite`
- stories 的 import 写法用 `@storybook/react`（核心包类型，两个 framework 都重新导出此类型）
- App ↔ Storybook 切换走 `EXPO_PUBLIC_STORYBOOK` 环境变量，不用代码注释切换

**架构选择理由**：

- monorepo 必须：要让 stories 物理唯一被两个引擎吸，必须走 workspace；同时是 source「私有包」需求的最小实现
- 只两个 package：再拆（如把 stories 单独抽 `packages/stories`）会破坏 atomic co-location；少拆（单 package）就丧失了「私有包」语义
- 不上 Docusaurus 外壳：Storybook 10 Autodocs 已经是文档站质感，套 Docusaurus 在第一版纯增加复杂度

---

## §2 关键依赖版本

全部采用 2026-05-16 时点的最新稳定版本。

| 类别 | 包 | 版本 | 备注 |
|---|---|---|---|
| 包管理 | `pnpm` | **^11**（latest = 11.1.2） | install 时取当下最新 |
| Runtime | `expo` | **^55**（latest = 55.0.24） | 全新最新 SDK |
| Runtime | `react` / `react-dom` | **^19.2**（latest = 19.2.6） | SDK 55 自然组合 |
| Runtime | `react-native` | SDK 55 配套（约 0.85.x，由 `expo install` 决定） | |
| Runtime | `react-native-web` | SDK 55 配套（由 `expo install` 决定） | Web SB 必需 |
| SB on-device | `@storybook/react-native` | **^10.4**（latest = 10.4.4） | |
| SB on-device | `@storybook/addon-ondevice-controls` | **^10.4** | controls panel |
| SB on-device | `@storybook/addon-ondevice-actions` | **^10.4** | events 日志 |
| SB Web | `@storybook/react-native-web-vite` | **^10.4**（latest = 10.4.0） | |
| SB CLI | `storybook` | **^10.4** | 跟 framework 同 major |
| SB Docs | `@storybook/addon-docs` | **^10.4** | Autodocs |
| 构建 | `vite` | 跟 SB framework peer 决定 | install 时 framework 自动拉对版本 |
| **SB 强制 peer** | `react-native-reanimated` | `expo install` 决定 | `@storybook/react-native@10.4` 强制 peer |
| **SB 强制 peer** | `react-native-gesture-handler` | `expo install` 决定 | 同上 |
| **SB 强制 peer** | `@gorhom/bottom-sheet` | `npm install` | 同上 |
| 必备 | `@react-native-async-storage/async-storage` | `expo install` 决定 | on-device controls 持久化 |
| 必备 | `react-native-safe-area-context` | `expo install` 决定 | on-device 渲染必需 |

**为什么 `@storybook/*` 必须同 major**：source §二明示「混用会运行时崩」。所有 `@storybook/*` 包统一锁 `^10.4`。

**关于 reanimated**：5 个组件本身不需要，但 `@storybook/react-native@^10.4` 自身 peer 强制要求 reanimated。这反而是好事——demo 会自动踩到 source §二警告的「reanimated plugin 必须 babel.config.js 最末」坑，验证此配置。

**没有 `pnpm.overrides`**：信任 expo 解决配套（SDK 55 的 RN 0.85 peer 强约束 React 19）。install 阶段如果出 ERESOLVE 冲突再补 override。

---

## §3 目录结构

仓库根：`/Users/shanyulong/riki/repo/rn-storybook-demo/`。所有目录与文件名走 kebab-case，组件标识符（`export function Button`）保持 PascalCase。`README.md` 例外保留大写（社区铁律）。

```
rn-storybook-demo/
├── .gitignore
├── .nvmrc                                   # node 20+ (Expo SDK 55 要求)
├── README.md
├── package.json                             # workspace 根 + 顶层 scripts
├── pnpm-workspace.yaml
├── tsconfig.base.json
│
├── packages/
│   │
│   ├── ui/                                  # 私有包 @myorg/ui
│   │   ├── package.json                     # name: "@myorg/ui", main: "./src/index.ts"
│   │   ├── tsconfig.json
│   │   ├── README.md
│   │   └── src/
│   │       ├── index.ts                     # barrel
│   │       ├── atoms/
│   │       │   ├── button/
│   │       │   │   ├── button.tsx
│   │       │   │   ├── button.stories.tsx
│   │       │   │   └── index.ts
│   │       │   ├── input/
│   │       │   │   ├── input.tsx
│   │       │   │   ├── input.stories.tsx
│   │       │   │   └── index.ts
│   │       │   └── avatar/
│   │       │       ├── avatar.tsx
│   │       │       ├── avatar.stories.tsx
│   │       │       └── index.ts
│   │       └── molecules/
│   │           ├── card/
│   │           │   ├── card.tsx
│   │           │   ├── card.stories.tsx
│   │           │   └── index.ts
│   │           └── list-item/
│   │               ├── list-item.tsx
│   │               ├── list-item.stories.tsx
│   │               └── index.ts
│   │
│   └── storybook-host/                      # Expo SDK 55 工程
│       ├── package.json
│       ├── app.json                         # Expo 配置
│       ├── tsconfig.json
│       ├── app.tsx                          # ENV 路由：业务占位 / on-device SB
│       ├── index.ts                         # registerRootComponent(App)
│       ├── metro.config.js                  # withStorybook(getDefaultConfig(...))
│       ├── babel.config.js                  # reanimated plugin 最末
│       ├── .storybook/                      # on-device 配置（CLI 默认目录）
│       │   ├── main.ts
│       │   ├── preview.tsx
│       │   ├── index.tsx                    # 导出 StorybookUIRoot
│       │   ├── storage.ts                   # AsyncStorage adapter
│       │   └── storybook.requires.ts        # CLI 自动生成，git ignore
│       └── .storybook-web/                  # web Vite 配置（自定义目录）
│           ├── main.ts
│           └── preview.tsx
│
└── docs/
    └── verification.md                      # 5 条核心验证项的人工 checklist
```

**几个非显然的点**：

1. 两个引擎 `main.ts` 的 `stories` glob 都写 `'../../ui/src/**/*.stories.@(ts|tsx)'`，跨 package 穿透
2. `.storybook/` vs `.storybook-web/` 拆两个目录避免两个 framework 配置互相打架
3. `packages/ui/src/index.ts` barrel 让 `app.tsx` 能 `import { Button } from '@myorg/ui'`，验证私有包 import
4. `storybook.requires.ts` git ignore（on-device CLI 自动生成）
5. 不引入 `apps/` 顶层目录（source 方案就是 `packages/`）

---

## §4 关键脚本

### root `package.json` scripts

```jsonc
{
  "scripts": {
    "dev:web":    "pnpm --filter storybook-host dev:web",
    "dev:device": "pnpm --filter storybook-host dev:device",
    "dev:app":    "pnpm --filter storybook-host dev:app",
    "build:web":  "pnpm --filter storybook-host build:web",
    "typecheck":  "pnpm -r typecheck"
  }
}
```

### `packages/storybook-host/package.json` scripts

```jsonc
{
  "scripts": {
    "dev:web":    "storybook dev --config-dir .storybook-web --port 6006",
    "build:web":  "storybook build --config-dir .storybook-web --output-dir storybook-static",
    "dev:device": "sb-rn-get-stories --config-path .storybook && EXPO_PUBLIC_STORYBOOK=1 expo start",
    "dev:app":    "expo start",
    "typecheck":  "tsc --noEmit"
  }
}
```

### 三条命令对应的验证项

| 命令 | 起什么 | 验证哪条 |
|---|---|---|
| `pnpm dev:web` | Vite dev server @ `localhost:6006` | V2/V3/V4 |
| `pnpm dev:device` | Metro + Expo dev server，QR 出现 | V5/V6 |
| `pnpm dev:app` | Metro + Expo dev server，业务占位屏 | V8 |

### `app.tsx` ENV 路由

```tsx
import { Text, View } from 'react-native';
import { Button } from '@myorg/ui';
import StorybookUIRoot from './.storybook';

export default function App() {
  if (process.env.EXPO_PUBLIC_STORYBOOK === '1') {
    return <StorybookUIRoot />;
  }
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', gap: 12 }}>
      <Text>业务占位 — 跑 pnpm dev:device 看 Storybook</Text>
      <Button label="来自 @myorg/ui" onPress={() => {}} />
    </View>
  );
}
```

### ENV 切换的已知约束

`process.env.EXPO_PUBLIC_*` 在 Expo 是编译时 inline，bundle 一旦生成就锁定。**切换 SB / App 模式必须重启 Metro**（kill `pnpm dev:device` 后跑 `pnpm dev:app`）。这是 Expo 行为，不是配置问题。

### `.gitignore` 关键条目

```
node_modules/
.expo/
storybook-static/
packages/storybook-host/.storybook/storybook.requires.ts
```

---

## §5 关键代码实现要点

只标注容易踩雷的配置文件和两套 SB 共享 stories 的关键写法。组件实现细节（5 个 atomic 组件）用最简 RN 原语即可，不在 spec 内固化。

### `metro.config.js` (storybook-host)

```js
const { getDefaultConfig } = require('expo/metro-config');
const { withStorybook } = require('@storybook/react-native/metro/withStorybook');
const path = require('path');

const config = getDefaultConfig(__dirname);
config.watchFolders = [path.resolve(__dirname, '../..')];   // 跨 package watch

module.exports = withStorybook(config, {
  enabled: process.env.EXPO_PUBLIC_STORYBOOK === '1',
  configPath: path.resolve(__dirname, './.storybook'),
});
```

### `babel.config.js` (storybook-host)

```js
module.exports = {
  presets: ['babel-preset-expo'],
  plugins: [
    'react-native-reanimated/plugin',  // 必须最末（source §二警告）
  ],
};
```

### `.storybook/main.ts` (on-device)

```ts
import type { StorybookConfig } from '@storybook/react-native';

const config: StorybookConfig = {
  stories: ['../../ui/src/**/*.stories.@(ts|tsx)'],
  addons: [
    '@storybook/addon-ondevice-controls',
    '@storybook/addon-ondevice-actions',
  ],
};
export default config;
```

### `.storybook/index.tsx` (on-device，导出 StorybookUIRoot)

```tsx
import { view } from './storybook.requires';
export default view.getStorybookUI({
  storage: require('./storage').default,
});
```

### `.storybook-web/main.ts` (web Vite)

```ts
import type { StorybookConfig } from '@storybook/react-native-web-vite';

const config: StorybookConfig = {
  framework: '@storybook/react-native-web-vite',
  stories: ['../../ui/src/**/*.stories.@(ts|tsx)'],
  addons: ['@storybook/addon-docs'],
};
export default config;
```

### Stories 写法（兼容两套 framework 的关键）

```tsx
// packages/ui/src/atoms/button/button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './button';

const meta = { component: Button } satisfies Meta<typeof Button>;
export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = { args: { label: 'Primary' } };
export const Disabled: Story = { args: { label: 'Disabled', disabled: true } };
```

`@storybook/react-native@^10` 和 `@storybook/react-native-web-vite@^10` 的 Meta/StoryObj 类型本质都从核心 `@storybook/react` 重新导出。如果实施时发现某个 framework 类型偏离，回退方案是定义本地 type alias 在两套配置里分别 patch。

### `pnpm-workspace.yaml`

```yaml
packages:
  - 'packages/*'
```

### `packages/ui/package.json`

```jsonc
{
  "name": "@myorg/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "peerDependencies": {
    "react": "*",
    "react-native": "*"
  }
}
```

### `packages/storybook-host/package.json` 关键依赖

```jsonc
{
  "name": "storybook-host",
  "private": true,
  "dependencies": {
    "@myorg/ui": "workspace:*",
    "expo": "^55.0.0",
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "react-native": "*",
    "react-native-web": "*",
    "react-native-reanimated": "*",
    "react-native-gesture-handler": "*",
    "react-native-safe-area-context": "*",
    "@react-native-async-storage/async-storage": "*",
    "@gorhom/bottom-sheet": "*"
  },
  "devDependencies": {
    "@storybook/react-native": "^10.4.0",
    "@storybook/react-native-web-vite": "^10.4.0",
    "@storybook/addon-ondevice-controls": "^10.4.0",
    "@storybook/addon-ondevice-actions": "^10.4.0",
    "@storybook/addon-docs": "^10.4.0",
    "storybook": "^10.4.0",
    "vite": "^8.0.0",
    "typescript": "*"
  }
}
```

`react-native` / `react-native-web` / 三个 RN 必备包用 `*`，由 `expo install` 在实施阶段固化为 SDK 55 兼容版本。

---

## §6 错误处理（install / 启动期）

| 失败场景 | 触发命令 | 处置 |
|---|---|---|
| `pnpm install` peer dep 警告 | install | 忽略（RN 生态 peer 警告常态，除非 ERESOLVE 硬错） |
| `pnpm install` ERESOLVE 冲突（React 版本） | install | root `package.json` 加 `"pnpm": { "overrides": { "react": "19.2.6" } }` |
| `dev:web` 报「找不到 framework」 | dev:web | 确认 `@storybook/react-native-web-vite` 已装、`.storybook-web/main.ts` 的 `framework` 字段拼写正确 |
| `dev:web` 报 `react-native-web` 解析失败 | dev:web | 跑 `npx expo install react-native-web @expo/metro-runtime` |
| `dev:device` 报「stories not found」 | dev:device | 漏跑 `sb-rn-get-stories`；或 `metro.config.js` 没 `withStorybook()` 包裹 |
| Metro 启动报 reanimated babel 错 | dev:device | reanimated plugin 不在 babel.config.js 最末，或 Metro 没清缓存 → `expo start --clear` |
| Expo Go 扫码 SB 进了业务占位屏 | dev:device | `EXPO_PUBLIC_STORYBOOK=1` 没生效——确认 cross-env 或 shell 正确设置 ENV |
| ENV 切换不生效 | 反复切 | Metro 缓存了 inline ENV → kill Metro 重启 |

---

## §7 风险与回退

**主要风险**：Storybook 10.x + Expo SDK 55 是「全新组合」，2026-05-16 时点 npm peer 检查通过，但实战未必丝滑。

**回退路径（按优先级）**：

1. 若 `dev:device` 启动失败但 `dev:web` 正常 → on-device SB 全家桶降到 `^9` 或 `^8.5`，保持 web SB 在 `^10.4`，前提是同 major 内自洽（即 web 也同步降）
2. 若 SDK 55 + RN 0.85 上 SB 自身崩 → 整 Expo 降到 SDK 54（保持 React 19 + RN 0.79.x，更接近 SB 10 测试基线）
3. 若彻底走不通 → fallback 到 source §三推荐的 SDK 52 + Storybook 8.5+ 组合

回退动作不在初始 spec 内固化，按实施时实测决定。

---

## §8 验收（手工 verification checklist）

`docs/verification.md` 内容（demo 完成的客观判定）：

```markdown
# Verification Checklist

每次 implementation 完成后逐条手工验。任一条 fail = 没跑通。

- [ ] V1: `pnpm install` 完成无 ERESOLVE 错误
- [ ] V2: `pnpm dev:web` 起在 6006，浏览器打开看到 5 个组件 sidebar
- [ ] V3: V2 中点 Button → Controls panel 改 label、disabled，画面实时变
- [ ] V4: V2 中能切到 Docs tab 看到 Autodocs 自动生成的 Button props 表
- [ ] V5: 终端 `pnpm dev:device`，QR 出现，Expo Go 扫描成功进入 on-device SB
- [ ] V6: V5 中能看到同样 5 个组件，点 Button 能改 controls
- [ ] V7: 改 `packages/ui/src/atoms/button/button.stories.tsx` 加一个 export → Web 端 Vite HMR 自动出现新 story；on-device 端 `Ctrl+C` 后重跑 `pnpm dev:device` 后出现新 story（证明两套 SB 共享同一份 stories；on-device 不要求 HMR）
- [ ] V8: `pnpm dev:app`（不带 ENV），扫 QR 进真机看到「业务占位」屏 + Button 渲染
- [ ] V9: `pnpm typecheck` 通过
- [ ] V10: `pnpm build:web` 产出 `storybook-static/`，本地 `npx serve storybook-static` 能预览
```

---

## §9 实施顺序

按依赖从底向上分 6 阶段，每阶段独立可验，每阶段一次 commit。

```
Phase 0  仓库脚手架     → 根 package.json + pnpm-workspace.yaml + tsconfig.base + .gitignore + .nvmrc
Phase 1  packages/ui    → 5 组件最简实现 + barrel + 5 份 stories
Phase 2  storybook-host → expo init + metro/babel/app.tsx + 装齐 SB 全家桶
Phase 3  on-device SB   → .storybook/* 配置 + dev:device 跑通 → 验 V5/V6
Phase 4  web SB         → .storybook-web/* 配置 + dev:web 跑通 → 验 V2/V3/V4
Phase 5  跨链路验证     → 改 stories 验 V7、ENV 切验 V8、build:web 验 V10
```

每阶段失败先排查 §6 错误处理表；多步排查无果再考虑 §7 回退路径。
