---
title: RN TextInput controlled vs uncontrolled
tags: [react-native, text-input, pattern]
date: 2026-05-09
sources:
  - "[[sources/posts/frontend/React/React Native/learning/rn-ios-cjk-input-issue]]"
last-ingested: 2026-05-09
status: draft
---

React Native `TextInput` 有 controlled（`value` prop）和 uncontrolled（`defaultValue` + `ref`）两种模式。Web React 几乎只用 controlled，但 RN 在 iOS 上 controlled 会 [[wiki/frontend/react-native/ios-cjk-ime-textinput|打断 CJK IME composition]]，所以生产场景常常要主动选 uncontrolled。

> [!compare] 两种模式
> | 维度 | controlled (`value={x}`) | uncontrolled (`defaultValue` + `ref`) |
> | --- | --- | --- |
> | text buffer 持有方 | JS state | native（`UITextField` / `EditText`） |
> | 每次按键 | `onChangeText` → 写回 JS → 同步回 native | `onChangeText` → 仅写 JS state，不回写 native |
> | iOS CJK IME | **打断 composition**（[[wiki/frontend/react-native/ios-cjk-ime-textinput|根因]]） | OK |
> | 编程式改值 | 改 state 即可 | 必须 `ref.clear()` 或 `ref.setNativeProps({ text })` |
> | 心智模型 | React 声明式 | 类 DOM 命令式 |

**何时选哪种**：

- **默认 uncontrolled**：搜索框、聊天输入、登录表单——任何会被中文/日文/韩文用户输入的场景。
- **可以 controlled**：纯英文/数字输入、密码框、不允许 IME 介入的场景（验证码、PIN）；以及业务需要"每按一键就立刻校验/格式化并回显"的强联动场景（哪怕代价是 CJK 不友好）。

**命令式改值常见姿势**：

```tsx
const inputRef = useRef<TextInput>(null);

inputRef.current?.clear();                          // 清空
inputRef.current?.setNativeProps({ text: '回填' });  // 强制写入（点击建议词回填用）
inputRef.current?.focus();                          // 拉起键盘
inputRef.current?.blur();                           // 收键盘
```

> [!note] setNativeProps 是 escape hatch
> `setNativeProps` 绕过 React diff 直接改 native props，性能好但要小心和 React state 不一致——它本质上是 RN 给"必须命令式"的场景留的逃生口。同类逃生口还有 `Animated` 的原生驱动、`findNodeHandle`（已 deprecated）等。

## 延伸阅读

- [[wiki/frontend/react-native/react-native-core-components|RN 核心组件]] — `TextInput` 在组件矩阵中的位置
- [TextInput 官方文档](https://reactnative.dev/docs/textinput)
- [setNativeProps 官方文档](https://reactnative.dev/docs/direct-manipulation)
