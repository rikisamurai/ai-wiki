# rn-storybook-demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `/Users/shanyulong/riki/repo/rn-storybook-demo` 新建一个 pnpm workspace monorepo，验证「同一份 `*.stories.tsx` 物理唯一、被 on-device Storybook + Web Vite Storybook 两套引擎同时消费」方案在 Expo SDK 55 + React 19.2 + Storybook 10.4 全新组合下能否跑通。

**Architecture:** 单仓库两 package：`packages/ui`（私有包 @myorg/ui，5 个 atomic 组件 + 5 个共居 stories）+ `packages/storybook-host`（Expo SDK 55 工程，承载 `.storybook/` on-device 配置和 `.storybook-web/` Web Vite 配置，两个引擎跨 package 吸 `packages/ui/src/**/*.stories.tsx`）。`app.tsx` 通过 `EXPO_PUBLIC_STORYBOOK` 环境变量切换业务占位 / on-device SB 入口。

**Tech Stack:** pnpm 11 / Expo SDK 55 / React 19.2 / React Native 0.85 / Storybook 10.4（react-native + react-native-web-vite framework）+ Vite 8 / TypeScript。

**Spec:** `docs/superpowers/specs/2026-05-16-rn-storybook-demo-design.md`

**仓库目标路径:** `/Users/shanyulong/riki/repo/rn-storybook-demo/`（不在 ai-wiki 仓库内，是同 parent 下的兄弟仓库）

---

## 任务 0: 仓库初始化与 root 配置

**Files:**
- Create: `/Users/shanyulong/riki/repo/rn-storybook-demo/.gitignore`
- Create: `/Users/shanyulong/riki/repo/rn-storybook-demo/.nvmrc`
- Create: `/Users/shanyulong/riki/repo/rn-storybook-demo/README.md`
- Create: `/Users/shanyulong/riki/repo/rn-storybook-demo/package.json`
- Create: `/Users/shanyulong/riki/repo/rn-storybook-demo/pnpm-workspace.yaml`
- Create: `/Users/shanyulong/riki/repo/rn-storybook-demo/tsconfig.base.json`

- [ ] **Step 0.1: 创建仓库目录并 git init**

```bash
mkdir -p /Users/shanyulong/riki/repo/rn-storybook-demo
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git init -b main
```

预期：`Initialized empty Git repository in .../rn-storybook-demo/.git/`

- [ ] **Step 0.2: 写 `.gitignore`**

```
node_modules/
.expo/
storybook-static/
packages/storybook-host/.storybook/storybook.requires.ts
.DS_Store
*.log
dist/
coverage/
```

- [ ] **Step 0.3: 写 `.nvmrc`**

```
20
```

- [ ] **Step 0.4: 写 `README.md`**

```markdown
# rn-storybook-demo

验证 [react-native-doc-site-stack-research](https://github.com/) 推荐方案的最小 demo：Expo + Storybook for React Native (on-device) + Storybook for React Native Web (Vite) 共享同一份 stories。

## 跑命令

| 命令 | 用途 |
|---|---|
| `pnpm dev:web` | 浏览器 Storybook (Vite, http://localhost:6006) |
| `pnpm dev:device` | Expo dev server，终端 QR 用 Expo Go 扫看 on-device Storybook |
| `pnpm dev:app` | 业务占位 App（验证 ENV 切回非 SB 模式） |
| `pnpm build:web` | 产出 `packages/storybook-host/storybook-static/` 静态站 |
| `pnpm typecheck` | 全仓 tsc --noEmit |

详见 `docs/verification.md` 的人工验收清单。

## 技术栈

- pnpm 11 workspace monorepo
- Expo SDK 55, React 19.2, React Native 0.85
- Storybook 10.4 (`@storybook/react-native` + `@storybook/react-native-web-vite`)
- TypeScript 5

## 目录

- `packages/ui` — 私有包 `@myorg/ui`，5 个 atomic 组件 + stories 共居
- `packages/storybook-host` — Expo 工程，承载两套 Storybook 配置
```

- [ ] **Step 0.5: 写 `package.json`**

```json
{
  "name": "rn-storybook-demo",
  "version": "0.0.0",
  "private": true,
  "packageManager": "pnpm@11.1.2",
  "scripts": {
    "dev:web": "pnpm --filter storybook-host dev:web",
    "dev:device": "pnpm --filter storybook-host dev:device",
    "dev:app": "pnpm --filter storybook-host dev:app",
    "build:web": "pnpm --filter storybook-host build:web",
    "typecheck": "pnpm -r typecheck"
  }
}
```

- [ ] **Step 0.6: 写 `pnpm-workspace.yaml`**

```yaml
packages:
  - 'packages/*'
```

- [ ] **Step 0.7: 写 `tsconfig.base.json`**

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "resolveJsonModule": true,
    "noEmit": true,
    "lib": ["ESNext", "DOM"]
  }
}
```

- [ ] **Step 0.8: 验证目录结构**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
ls -la
```

预期看到：`.git/`, `.gitignore`, `.nvmrc`, `README.md`, `package.json`, `pnpm-workspace.yaml`, `tsconfig.base.json`

- [ ] **Step 0.9: 首次 commit**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add .
git commit -m "chore: 初始化 pnpm workspace 与根配置"
```

预期：commit 成功，落定 7 个文件。

---

## 任务 1: packages/ui 包结构 + barrel

**Files:**
- Create: `packages/ui/package.json`
- Create: `packages/ui/tsconfig.json`
- Create: `packages/ui/README.md`
- Create: `packages/ui/src/index.ts`（先放 5 行 export 占位，后续 task 实际创建组件）

- [ ] **Step 1.1: 创建 packages/ui 目录树**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
mkdir -p packages/ui/src/atoms/button packages/ui/src/atoms/input packages/ui/src/atoms/avatar
mkdir -p packages/ui/src/molecules/card packages/ui/src/molecules/list-item
ls packages/ui/src
```

预期看到 `atoms/` 和 `molecules/`。

- [ ] **Step 1.2: 写 `packages/ui/package.json`**

```json
{
  "name": "@myorg/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": {
    "typecheck": "tsc --noEmit"
  },
  "peerDependencies": {
    "react": "*",
    "react-native": "*"
  },
  "devDependencies": {
    "typescript": "*",
    "@types/react": "*"
  }
}
```

- [ ] **Step 1.3: 写 `packages/ui/tsconfig.json`**

```json
{
  "extends": "../../tsconfig.base.json",
  "include": ["src/**/*"]
}
```

- [ ] **Step 1.4: 写 `packages/ui/README.md`**

```markdown
# @myorg/ui

私有 workspace 包，5 个 atomic 组件 + stories 共居示例。

## 新增组件流程

1. 在 `src/atoms/` 或 `src/molecules/` 下新建 `<name>/` 目录
2. 创建 `<name>.tsx`（实现）+ `<name>.stories.tsx`（stories）+ `index.ts`（barrel）
3. 在 `src/index.ts` 加一行 `export ... from './<atoms|molecules>/<name>';`

两套 Storybook（on-device + web）会自动 pick 起新 stories。
```

- [ ] **Step 1.5: 写 `packages/ui/src/index.ts`（barrel，含全部 5 个 export 提前占位）**

```ts
export { Button, type ButtonProps } from './atoms/button';
export { Input, type InputProps } from './atoms/input';
export { Avatar, type AvatarProps } from './atoms/avatar';
export { Card, type CardProps } from './molecules/card';
export { ListItem, type ListItemProps } from './molecules/list-item';
```

> 此时 import 会报错，下一个 task 创建组件文件后才解决。

- [ ] **Step 1.6: commit**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add packages/
git commit -m "feat(ui): packages/ui 包结构与 barrel"
```

---

## 任务 2: 5 个组件实现（atoms × 3 + molecules × 2）

**Files:**
- Create: `packages/ui/src/atoms/button/button.tsx`
- Create: `packages/ui/src/atoms/button/index.ts`
- Create: `packages/ui/src/atoms/input/input.tsx`
- Create: `packages/ui/src/atoms/input/index.ts`
- Create: `packages/ui/src/atoms/avatar/avatar.tsx`
- Create: `packages/ui/src/atoms/avatar/index.ts`
- Create: `packages/ui/src/molecules/card/card.tsx`
- Create: `packages/ui/src/molecules/card/index.ts`
- Create: `packages/ui/src/molecules/list-item/list-item.tsx`
- Create: `packages/ui/src/molecules/list-item/index.ts`

- [ ] **Step 2.1: 写 `packages/ui/src/atoms/button/button.tsx`**

```tsx
import { Pressable, Text, StyleSheet } from 'react-native';

export type ButtonProps = {
  label: string;
  disabled?: boolean;
  onPress?: () => void;
};

export function Button({ label, disabled = false, onPress }: ButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.base,
        disabled && styles.disabled,
        pressed && !disabled && styles.pressed,
      ]}
    >
      <Text style={styles.text}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 8,
    backgroundColor: '#3b82f6',
    alignSelf: 'flex-start',
  },
  disabled: { backgroundColor: '#9ca3af' },
  pressed: { opacity: 0.8 },
  text: { color: 'white', fontWeight: '600' },
});
```

- [ ] **Step 2.2: 写 `packages/ui/src/atoms/button/index.ts`**

```ts
export * from './button';
```

- [ ] **Step 2.3: 写 `packages/ui/src/atoms/input/input.tsx`**

```tsx
import { TextInput, StyleSheet, View, Text } from 'react-native';

export type InputProps = {
  value: string;
  placeholder?: string;
  label?: string;
  onChangeText?: (text: string) => void;
};

export function Input({ value, placeholder, label, onChangeText }: InputProps) {
  return (
    <View style={styles.wrap}>
      {label ? <Text style={styles.label}>{label}</Text> : null}
      <TextInput
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        style={styles.input}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 4 },
  label: { fontSize: 12, color: '#6b7280' },
  input: {
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 6,
    paddingHorizontal: 10,
    paddingVertical: 8,
    minWidth: 200,
  },
});
```

- [ ] **Step 2.4: 写 `packages/ui/src/atoms/input/index.ts`**

```ts
export * from './input';
```

- [ ] **Step 2.5: 写 `packages/ui/src/atoms/avatar/avatar.tsx`**

```tsx
import { Image, View, StyleSheet, Text } from 'react-native';

export type AvatarProps = {
  uri?: string;
  size?: number;
  fallback?: string;
};

export function Avatar({ uri, size = 40, fallback = '?' }: AvatarProps) {
  if (uri) {
    return (
      <Image
        source={{ uri }}
        style={[styles.img, { width: size, height: size, borderRadius: size / 2 }]}
      />
    );
  }
  return (
    <View
      style={[
        styles.placeholder,
        { width: size, height: size, borderRadius: size / 2 },
      ]}
    >
      <Text style={styles.fallback}>{fallback}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  img: { backgroundColor: '#e5e7eb' },
  placeholder: {
    backgroundColor: '#e5e7eb',
    alignItems: 'center',
    justifyContent: 'center',
  },
  fallback: { color: '#6b7280', fontWeight: '600' },
});
```

- [ ] **Step 2.6: 写 `packages/ui/src/atoms/avatar/index.ts`**

```ts
export * from './avatar';
```

- [ ] **Step 2.7: 写 `packages/ui/src/molecules/card/card.tsx`**

```tsx
import { View, Text, StyleSheet } from 'react-native';
import type { ReactNode } from 'react';

export type CardProps = {
  title: string;
  children?: ReactNode;
};

export function Card({ title, children }: CardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      {children ? <View style={styles.body}>{children}</View> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: 'white',
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
    gap: 8,
    minWidth: 240,
  },
  title: { fontSize: 16, fontWeight: '600' },
  body: { gap: 6 },
});
```

- [ ] **Step 2.8: 写 `packages/ui/src/molecules/card/index.ts`**

```ts
export * from './card';
```

- [ ] **Step 2.9: 写 `packages/ui/src/molecules/list-item/list-item.tsx`**

```tsx
import { View, Text, StyleSheet } from 'react-native';
import { Avatar } from '../../atoms/avatar';

export type ListItemProps = {
  title: string;
  subtitle?: string;
  avatarUri?: string;
};

export function ListItem({ title, subtitle, avatarUri }: ListItemProps) {
  return (
    <View style={styles.row}>
      <Avatar uri={avatarUri} fallback={title.charAt(0)} />
      <View style={styles.text}>
        <Text style={styles.title}>{title}</Text>
        {subtitle ? <Text style={styles.sub}>{subtitle}</Text> : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    paddingVertical: 8,
  },
  text: { flex: 1 },
  title: { fontSize: 14, fontWeight: '500' },
  sub: { fontSize: 12, color: '#6b7280' },
});
```

- [ ] **Step 2.10: 写 `packages/ui/src/molecules/list-item/index.ts`**

```ts
export * from './list-item';
```

- [ ] **Step 2.11: commit**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add packages/ui/src
git commit -m "feat(ui): 5 个 atomic 组件实现 (button/input/avatar/card/list-item)"
```

---

## 任务 3: 5 份 stories 文件

**Files:**
- Create: `packages/ui/src/atoms/button/button.stories.tsx`
- Create: `packages/ui/src/atoms/input/input.stories.tsx`
- Create: `packages/ui/src/atoms/avatar/avatar.stories.tsx`
- Create: `packages/ui/src/molecules/card/card.stories.tsx`
- Create: `packages/ui/src/molecules/list-item/list-item.stories.tsx`

> 所有 stories 都从 `@storybook/react` import 类型——这是 on-device 和 web 两个 framework 都重新导出的核心包，写一次两边都能消费。

- [ ] **Step 3.1: 写 `packages/ui/src/atoms/button/button.stories.tsx`**

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './button';

const meta = { component: Button } satisfies Meta<typeof Button>;
export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = { args: { label: 'Primary' } };
export const Disabled: Story = { args: { label: 'Disabled', disabled: true } };
```

- [ ] **Step 3.2: 写 `packages/ui/src/atoms/input/input.stories.tsx`**

```tsx
import { useState } from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { Input } from './input';

const meta = { component: Input } satisfies Meta<typeof Input>;
export default meta;
type Story = StoryObj<typeof meta>;

export const WithLabel: Story = {
  args: { label: '邮箱', placeholder: 'you@example.com', value: '' },
  render: (args) => {
    const [v, setV] = useState(args.value);
    return <Input {...args} value={v} onChangeText={setV} />;
  },
};
```

- [ ] **Step 3.3: 写 `packages/ui/src/atoms/avatar/avatar.stories.tsx`**

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Avatar } from './avatar';

const meta = { component: Avatar } satisfies Meta<typeof Avatar>;
export default meta;
type Story = StoryObj<typeof meta>;

export const WithImage: Story = {
  args: { uri: 'https://i.pravatar.cc/100', size: 40 },
};
export const Fallback: Story = { args: { fallback: 'A', size: 40 } };
```

- [ ] **Step 3.4: 写 `packages/ui/src/molecules/card/card.stories.tsx`**

```tsx
import { Text } from 'react-native';
import type { Meta, StoryObj } from '@storybook/react';
import { Card } from './card';

const meta = { component: Card } satisfies Meta<typeof Card>;
export default meta;
type Story = StoryObj<typeof meta>;

export const Simple: Story = { args: { title: 'Hello' } };
export const WithBody: Story = {
  args: {
    title: 'With body',
    children: <Text>这是 card 的子内容</Text>,
  },
};
```

- [ ] **Step 3.5: 写 `packages/ui/src/molecules/list-item/list-item.stories.tsx`**

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ListItem } from './list-item';

const meta = { component: ListItem } satisfies Meta<typeof ListItem>;
export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { title: 'Alice', subtitle: 'iOS 工程师' } };
export const WithAvatar: Story = {
  args: {
    title: 'Bob',
    subtitle: 'Web 全栈',
    avatarUri: 'https://i.pravatar.cc/100?u=bob',
  },
};
```

- [ ] **Step 3.6: 验证 5 份 stories 都到位**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
find packages/ui/src -name '*.stories.tsx'
```

预期看到 5 行：`button.stories.tsx`, `input.stories.tsx`, `avatar.stories.tsx`, `card.stories.tsx`, `list-item.stories.tsx`。

- [ ] **Step 3.7: commit**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add packages/ui/src
git commit -m "feat(ui): 5 份 atomic 组件 stories"
```

---

## 任务 4: storybook-host Expo 工程脚手架

**Files:**
- Create: `packages/storybook-host/package.json`
- Create: `packages/storybook-host/app.json`
- Create: `packages/storybook-host/tsconfig.json`
- Create: `packages/storybook-host/index.ts`
- Create: `packages/storybook-host/app.tsx`
- Create: `packages/storybook-host/metro.config.js`
- Create: `packages/storybook-host/babel.config.js`

- [ ] **Step 4.1: 创建目录**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
mkdir -p packages/storybook-host
```

- [ ] **Step 4.2: 写 `packages/storybook-host/package.json`**

```json
{
  "name": "storybook-host",
  "version": "0.0.0",
  "private": true,
  "main": "index.ts",
  "scripts": {
    "dev:web": "storybook dev --config-dir .storybook-web --port 6006",
    "build:web": "storybook build --config-dir .storybook-web --output-dir storybook-static",
    "dev:device": "sb-rn-get-stories --config-path .storybook && EXPO_PUBLIC_STORYBOOK=1 expo start",
    "dev:app": "expo start",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@myorg/ui": "workspace:*",
    "expo": "^55.0.0",
    "react": "^19.2.0",
    "react-dom": "^19.2.0"
  },
  "devDependencies": {
    "@storybook/react-native": "^10.4.0",
    "@storybook/react-native-web-vite": "^10.4.0",
    "@storybook/addon-ondevice-controls": "^10.4.0",
    "@storybook/addon-ondevice-actions": "^10.4.0",
    "@storybook/addon-docs": "^10.4.0",
    "storybook": "^10.4.0",
    "vite": "^8.0.0",
    "typescript": "*",
    "@types/react": "*"
  }
}
```

> `react-native` / `react-native-web` / 三个 RN 必备包稍后用 `expo install` 装入，让 Expo 自己挑配套版本。

- [ ] **Step 4.3: 写 `packages/storybook-host/app.json`**

```json
{
  "expo": {
    "name": "rn-storybook-demo",
    "slug": "rn-storybook-demo",
    "version": "0.0.0",
    "orientation": "portrait",
    "platforms": ["ios", "android", "web"],
    "newArchEnabled": true
  }
}
```

- [ ] **Step 4.4: 写 `packages/storybook-host/tsconfig.json`**

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "jsx": "react-jsx"
  },
  "include": ["**/*.ts", "**/*.tsx", ".storybook/**/*", ".storybook-web/**/*"]
}
```

- [ ] **Step 4.5: 写 `packages/storybook-host/index.ts`**

```ts
import { registerRootComponent } from 'expo';
import App from './app';

registerRootComponent(App);
```

- [ ] **Step 4.6: 写 `packages/storybook-host/app.tsx`**

```tsx
import { Text, View } from 'react-native';
import { Button } from '@myorg/ui';
import StorybookUIRoot from './.storybook';

export default function App() {
  if (process.env.EXPO_PUBLIC_STORYBOOK === '1') {
    return <StorybookUIRoot />;
  }
  return (
    <View
      style={{
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        gap: 12,
      }}
    >
      <Text>业务占位 — 跑 pnpm dev:device 看 Storybook</Text>
      <Button label="来自 @myorg/ui" onPress={() => {}} />
    </View>
  );
}
```

> 此时 `import StorybookUIRoot from './.storybook'` 会报错，等任务 5 写完 `.storybook/index.tsx` 才解决。

- [ ] **Step 4.7: 写 `packages/storybook-host/metro.config.js`**

```js
const { getDefaultConfig } = require('expo/metro-config');
const { withStorybook } = require('@storybook/react-native/metro/withStorybook');
const path = require('path');

const config = getDefaultConfig(__dirname);
config.watchFolders = [path.resolve(__dirname, '../..')];

module.exports = withStorybook(config, {
  enabled: process.env.EXPO_PUBLIC_STORYBOOK === '1',
  configPath: path.resolve(__dirname, './.storybook'),
});
```

- [ ] **Step 4.8: 写 `packages/storybook-host/babel.config.js`**

```js
module.exports = {
  presets: ['babel-preset-expo'],
  plugins: [
    'react-native-reanimated/plugin',
  ],
};
```

> `react-native-reanimated/plugin` 必须是 plugins 数组的最末项（source §二 警告点之一）。当前数组就一个 plugin，已经满足；未来加新 plugin 时插在它前面。

- [ ] **Step 4.9: commit**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add packages/storybook-host
git commit -m "feat(host): storybook-host Expo 工程脚手架"
```

---

## 任务 5: on-device Storybook 配置 (.storybook/)

**Files:**
- Create: `packages/storybook-host/.storybook/main.ts`
- Create: `packages/storybook-host/.storybook/preview.tsx`
- Create: `packages/storybook-host/.storybook/storage.ts`
- Create: `packages/storybook-host/.storybook/index.tsx`

- [ ] **Step 5.1: 创建 `.storybook/` 目录**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
mkdir -p packages/storybook-host/.storybook
```

- [ ] **Step 5.2: 写 `packages/storybook-host/.storybook/main.ts`**

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

- [ ] **Step 5.3: 写 `packages/storybook-host/.storybook/preview.tsx`**

```tsx
import { View } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import type { Preview } from '@storybook/react';

const preview: Preview = {
  decorators: [
    (Story) => (
      <SafeAreaProvider>
        <View style={{ padding: 16, flex: 1 }}>
          <Story />
        </View>
      </SafeAreaProvider>
    ),
  ],
};

export default preview;
```

- [ ] **Step 5.4: 写 `packages/storybook-host/.storybook/storage.ts`**

```ts
import AsyncStorage from '@react-native-async-storage/async-storage';

export default AsyncStorage;
```

- [ ] **Step 5.5: 写 `packages/storybook-host/.storybook/index.tsx`**

```tsx
// @ts-expect-error storybook.requires.ts is generated by sb-rn-get-stories at build time
import { view } from './storybook.requires';
import storage from './storage';

export default view.getStorybookUI({ storage });
```

- [ ] **Step 5.6: commit**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add packages/storybook-host/.storybook
git commit -m "feat(host): .storybook on-device 配置"
```

---

## 任务 6: web Storybook 配置 (.storybook-web/)

**Files:**
- Create: `packages/storybook-host/.storybook-web/main.ts`
- Create: `packages/storybook-host/.storybook-web/preview.tsx`

- [ ] **Step 6.1: 创建 `.storybook-web/` 目录**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
mkdir -p packages/storybook-host/.storybook-web
```

- [ ] **Step 6.2: 写 `packages/storybook-host/.storybook-web/main.ts`**

```ts
import type { StorybookConfig } from '@storybook/react-native-web-vite';

const config: StorybookConfig = {
  framework: '@storybook/react-native-web-vite',
  stories: ['../../ui/src/**/*.stories.@(ts|tsx)'],
  addons: ['@storybook/addon-docs'],
};

export default config;
```

- [ ] **Step 6.3: 写 `packages/storybook-host/.storybook-web/preview.tsx`**

```tsx
import type { Preview } from '@storybook/react';

const preview: Preview = {};

export default preview;
```

- [ ] **Step 6.4: commit**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add packages/storybook-host/.storybook-web
git commit -m "feat(host): .storybook-web Vite 配置"
```

---

## 任务 7: 装依赖（pnpm install + expo install RN peers）

**Files:**
- Modify: `packages/storybook-host/package.json`（被 expo install 自动追加 RN deps）
- Modify: `pnpm-lock.yaml`（首次生成）

- [ ] **Step 7.1: 跑 pnpm install**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm install
```

预期：装好 expo / react / storybook 全家桶。允许出现 peer warning（RN 生态常态），但不应有 ERESOLVE 硬错。

- [ ] **Step 7.2: 检查 ERESOLVE**

如果上一步报 ERESOLVE 冲突（多见于 React 版本冲突），在 root `package.json` 末尾加：

```json
"pnpm": {
  "overrides": {
    "react": "19.2.6",
    "react-dom": "19.2.6"
  }
}
```

然后重跑 `pnpm install`。

- [ ] **Step 7.3: 用 expo install 装 RN 配套包**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo/packages/storybook-host
pnpm exec expo install react-native react-native-web @expo/metro-runtime react-native-reanimated react-native-gesture-handler react-native-safe-area-context @react-native-async-storage/async-storage @gorhom/bottom-sheet
```

预期：expo 自动选 SDK 55 兼容版本写入 `package.json`。

- [ ] **Step 7.4: 重跑 pnpm install 让 lockfile 同步新依赖**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm install
```

预期：完成无 ERESOLVE 错误（V1 验证项）。

- [ ] **Step 7.5: 跑 typecheck 看 ts 是否通过**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm typecheck
```

预期：`packages/ui` 通过；`packages/storybook-host` 可能因为 `./.storybook/storybook.requires` 还没生成报错（已在 §5 step 5.5 加 `@ts-expect-error` 抑制），其余通过。如其他文件报错，回相关 task 修。

- [ ] **Step 7.6: commit**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add package.json pnpm-lock.yaml packages/storybook-host/package.json
git commit -m "chore: 装齐依赖（pnpm install + expo install RN peers）"
```

---

## 任务 8: 跑 dev:device 验 V5/V6（on-device Storybook）

**Files:**
- Generated（不入 git）: `packages/storybook-host/.storybook/storybook.requires.ts`

- [ ] **Step 8.1: 手工跑 sb-rn-get-stories 生成 requires 文件**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo/packages/storybook-host
pnpm exec sb-rn-get-stories --config-path .storybook
ls .storybook/storybook.requires.ts
```

预期：生成 `storybook.requires.ts`，内容里能看到 5 个 `require('../../ui/src/atoms/.../*.stories.tsx')` 引用。

- [ ] **Step 8.2: 启动 dev:device**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm dev:device
```

预期：终端打印 Metro waiting + QR Code。如果报 Metro 缓存 / babel 错，跑 `pnpm --filter storybook-host expo start --clear` 重试。

- [ ] **Step 8.3: 用 Expo Go 扫 QR**

打开手机 Expo Go app（iOS App Store / Android Play Store 装），扫终端 QR。

预期：手机进入 on-device Storybook，看到 sidebar 列出 5 个组件（Button / Input / Avatar / Card / ListItem），可点开切 stories。**这就是 V5 验证通过**。

- [ ] **Step 8.4: 验 V6（改 controls 看实时变化）**

在手机上：
1. 选中 Button → Primary story
2. 打开 Controls panel → 改 `label` 为别的字符串、勾选 `disabled`
3. 看到画面实时变化

预期：画面响应。**V6 验证通过**。

- [ ] **Step 8.5: 退出 dev:device**

终端 `Ctrl+C` 关闭 Metro。

- [ ] **Step 8.6: 写 V5/V6 通过记录到临时备忘**

不入 git，仅口头确认。

---

## 任务 9: 跑 dev:web 验 V2/V3/V4（Web Storybook）

- [ ] **Step 9.1: 启动 dev:web**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm dev:web
```

预期：Vite 启动，终端打印 `Local: http://localhost:6006/`。如报 `react-native-web` 解析失败，回任务 7 step 7.3 补装。

- [ ] **Step 9.2: 验 V2（5 个组件 sidebar）**

浏览器打开 `http://localhost:6006`。

预期：sidebar 列出 5 个组件 + 各自 stories。**V2 验证通过**。

- [ ] **Step 9.3: 验 V3（controls 实时改）**

点 Button → Primary。底部 Controls panel 改 `label`、勾选 `disabled`。

预期：画面实时变。**V3 验证通过**。

- [ ] **Step 9.4: 验 V4（Autodocs Docs tab）**

点击顶部 Docs tab。

预期：能看到自动生成的 Button props 表（label / disabled / onPress）。**V4 验证通过**。

- [ ] **Step 9.5: 退出 dev:web**

终端 `Ctrl+C`。

---

## 任务 10: 跨链路验证（V7/V8/V9/V10）

- [ ] **Step 10.1: 准备验 V7 — 改 button.stories.tsx 加新 export**

编辑 `packages/ui/src/atoms/button/button.stories.tsx`，在文件末尾追加：

```tsx
export const LongLabel: Story = {
  args: { label: '一个长得多的 label，用来测试 wrap 行为' },
};
```

- [ ] **Step 10.2: 验 Web 端 HMR 自动出现新 story**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm dev:web
```

浏览器刷 `http://localhost:6006`，找到 Button → 应该多了一个 `LongLabel` story。

预期：Vite HMR 自动 pick 起新 story，显示在 sidebar。

终端 `Ctrl+C` 关掉。

- [ ] **Step 10.3: 验 on-device 端重跑后出现新 story**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm dev:device
```

Expo Go 重新连接。Button → 出现 `LongLabel` story。

预期：on-device SB 也看到新 story（证明两套 SB 共享同一份物理 stories 文件）。**V7 验证通过**。

终端 `Ctrl+C` 关掉。

- [ ] **Step 10.4: 验 V8（dev:app 业务占位）**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm dev:app
```

Expo Go 扫 QR。

预期：手机看到「业务占位 — 跑 pnpm dev:device 看 Storybook」文字 + 一个「来自 @myorg/ui」按钮。**V8 验证通过**（证明 ENV 路由 + 私有包 import 都通）。

终端 `Ctrl+C` 关掉。

- [ ] **Step 10.5: 验 V9（typecheck）**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm typecheck
```

预期：全部通过。**V9 验证通过**。

- [ ] **Step 10.6: 验 V10（build:web）**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
pnpm build:web
ls packages/storybook-host/storybook-static/
```

预期：`storybook-static/` 目录生成，含 `index.html`。

- [ ] **Step 10.7: 本地 serve 验证 build 产物可访问**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo/packages/storybook-host
pnpm dlx serve storybook-static -p 7007
```

浏览器开 `http://localhost:7007`，看到跟 dev:web 一样的 Storybook UI。

预期：5 个组件正常显示。**V10 验证通过**。

终端 `Ctrl+C` 关掉。

- [ ] **Step 10.8: 提交 V7 加的 story 改动**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add packages/ui/src/atoms/button/button.stories.tsx
git commit -m "test(ui): button 加 LongLabel story 用于验证 V7"
```

---

## 任务 11: 写 docs/verification.md 与最终 commit

**Files:**
- Create: `docs/verification.md`

- [ ] **Step 11.1: 创建 docs/ 目录**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
mkdir -p docs
```

- [ ] **Step 11.2: 写 `docs/verification.md`**

```markdown
# Verification Checklist

每次 implementation 完成后逐条手工验。任一条 fail = 没跑通。

- [x] V1: `pnpm install` 完成无 ERESOLVE 错误
- [x] V2: `pnpm dev:web` 起在 6006，浏览器打开看到 5 个组件 sidebar
- [x] V3: V2 中点 Button → Controls panel 改 label、disabled，画面实时变
- [x] V4: V2 中能切到 Docs tab 看到 Autodocs 自动生成的 Button props 表
- [x] V5: 终端 `pnpm dev:device`，QR 出现，Expo Go 扫描成功进入 on-device SB
- [x] V6: V5 中能看到同样 5 个组件，点 Button 能改 controls
- [x] V7: 改 `packages/ui/src/atoms/button/button.stories.tsx` 加一个 export → Web 端 Vite HMR 自动出现新 story；on-device 端 `Ctrl+C` 后重跑 `pnpm dev:device` 后出现新 story（证明两套 SB 共享同一份 stories；on-device 不要求 HMR）
- [x] V8: `pnpm dev:app`（不带 ENV），扫 QR 进真机看到「业务占位」屏 + Button 渲染
- [x] V9: `pnpm typecheck` 通过
- [x] V10: `pnpm build:web` 产出 `storybook-static/`，本地 `npx serve storybook-static` 能预览

## 备注

如某条 fail，按 spec §6 错误处理表逐项排查；多步无果再考虑 §7 回退路径（SB 降到 ^9 / Expo 降到 SDK 54 / 整套回 SDK 52 + SB 8.5）。
```

- [ ] **Step 11.3: commit**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git add docs/verification.md
git commit -m "docs: verification checklist 全部勾选"
```

- [ ] **Step 11.4: 看完整 git log 确认 commit 序列**

```bash
cd /Users/shanyulong/riki/repo/rn-storybook-demo
git log --oneline
```

预期看到大致 9 个 commit：
```
docs: verification checklist 全部勾选
test(ui): button 加 LongLabel story 用于验证 V7
chore: 装齐依赖（pnpm install + expo install RN peers）
feat(host): .storybook-web Vite 配置
feat(host): .storybook on-device 配置
feat(host): storybook-host Expo 工程脚手架
feat(ui): 5 份 atomic 组件 stories
feat(ui): 5 个 atomic 组件实现 (button/input/avatar/card/list-item)
feat(ui): packages/ui 包结构与 barrel
chore: 初始化 pnpm workspace 与根配置
```

- [ ] **Step 11.5: 总结上报**

向用户报告：

> demo 仓库已建在 `/Users/shanyulong/riki/repo/rn-storybook-demo`，10 条 verification 全部通过。下一步可考虑：
> - 给方案再加 Docusaurus 外壳验证「文档站质感升级」路径
> - 接 Chromatic 验证视觉回归
> - 把 demo 经验沉淀为 wiki 页（送回 ai-wiki/sources/inbox）

---

## 任务概览（依赖关系）

```
任务 0 (root 脚手架)
  └─ 任务 1 (packages/ui 骨架)
       └─ 任务 2 (5 组件实现)
            └─ 任务 3 (5 stories)
                 └─ 任务 4 (storybook-host 工程)
                      ├─ 任务 5 (.storybook on-device)
                      └─ 任务 6 (.storybook-web)
                           └─ 任务 7 (装依赖)
                                ├─ 任务 8 (验 V5/V6 on-device)
                                └─ 任务 9 (验 V2/V3/V4 web)
                                     └─ 任务 10 (验 V7/V8/V9/V10)
                                          └─ 任务 11 (docs/verification.md + 收尾)
```

任务 5/6 之间无依赖可并行，但顺序执行更稳。任务 8/9 之间无依赖（都依赖任务 7），但建议串行避免 Metro / Vite 端口和缓存竞态。
