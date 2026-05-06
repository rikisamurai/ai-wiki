---
title: CSF（Component Story Format）
tags: [storybook, react-native, conventions]
date: 2026-05-06
sources:
  - "[[sources/posts/frontend/React/React Native/react-native-doc-site-stack-research]]"
last-ingested: 2026-05-06
status: draft
---

Component Story Format 是 [[wiki/frontend/react-native/storybook-react-native|Storybook]] 的 story 编写约定：基于 ES6 模块——一个 `default export` 描述组件元信息，多个 `named export` 描述具体 story。**story 文件与组件文件同目录**（co-location），用 TypeScript 的 `Meta` / `StoryObj` 泛型获得 args 类型推导。CSF 文件只在开发期存在，不会进 production bundle。

> [!note] "args" = props
> Storybook 用通用术语 "args" 描述 story 接收的参数。在 React/RN 里 args 就是 React props，传进 controls panel 后可以浏览器/真机上实时调。

## 最小 CSF 3 + TypeScript

```ts
import type { Meta, StoryObj } from '@storybook/react-native';
import { Button } from './Button';

const meta = { component: Button } satisfies Meta<typeof Button>;
export default meta;

type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { label: 'Click me', variant: 'primary' },
};

export const Disabled: Story = {
  args: { label: 'Disabled', disabled: true },
};
```

每个 named export 是一个 story，args 即组件 props。Storybook controls panel 自动从 props 类型推断出输入控件（boolean → switch、enum → select、string → text input）。

## 三层注解：global / component / story

CSF 的 `parameters` 与 `decorators` 可在三个层面声明，下层覆盖上层：

- **global**：`.storybook/preview.ts` 里全局生效（如统一 backgrounds、theme provider）
- **component**：`meta` 的字段，对该组件所有 story 生效
- **story**：单个 export 的字段，仅该 story 生效

> [!example] decorator 提供共享上下文
> ```ts
> const meta = {
>   component: Button,
>   decorators: [
>     (Story) => <View style={{ padding: 16 }}><Story /></View>,
>     (Story) => <ThemeProvider><Story /></ThemeProvider>,
>   ],
> } satisfies Meta<typeof Button>;
> ```
> 常用于注入 theme、provider、padding，避免每个 story 重复 wrap。

## 配置入口

在 `.storybook/main.ts` 里声明 stories 路径：

```ts
const config = {
  stories: ['../packages/ui/src/**/*.stories.@(ts|tsx)'],
  addons: [
    '@storybook/addon-ondevice-controls',
    '@storybook/addon-ondevice-actions',
  ],
};
export default config;
```

> [!warning] Metro 端必须包 withStorybook
> RN 端 `unstable_allowRequireContext` 是动态 stories glob 的前提，详见 [[wiki/frontend/react-native/storybook-react-native|Storybook for RN]] 的关键配置坑。

## 与组件组织

CSF 文件与组件文件**同目录**，是社区公认的 atomic design 落地形态：

```
packages/ui/src/
├── Button/
│   ├── Button.tsx
│   └── Button.stories.tsx
├── Input/
│   ├── Input.tsx
│   └── Input.stories.tsx
```

[[wiki/frontend/react-native/react-native-component-docs-stack|monorepo 架构]] 推荐做法是 stories 写在 `packages/ui` 内、`storybook-host` 通过 glob 吸进来，**两套 Storybook**（web + on-device）共享同一批 story 文件，不写两遍。

## 延伸阅读

- [Writing stories | React Native Storybook](https://storybookjs.github.io/react-native/docs/intro/writing-stories/)
- [Component Story Format 规范](https://storybook.js.org/docs/api/csf)
