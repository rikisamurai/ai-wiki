---
title: KeyboardAvoidingView
tags: [react-native, keyboard]
date: 2026-05-09
sources:
  - "[[sources/posts/frontend/React/React Native/learning/rn-keyboard-pitfalls]]"
last-ingested: 2026-05-09
status: draft
---

RN 内置的"键盘起来时把内容顶上去"组件。是一个**够用版半成品**——简单场景能用，稍微复杂（嵌套 `ScrollView` / `SafeAreaView`、自定义 nav bar 高度）就开始抽风。生产项目通常直接换 [[wiki/frontend/react-native/react-native-keyboard-controller|react-native-keyboard-controller]]。

> [!warning] 要不要用它的判断标准
> 单层布局（一个 `View` 套 `TextInput` + 按钮）→ 用 `KeyboardAvoidingView` 够了。
> 多层嵌套 / 列表 / 自定义 header → 直接换 keyboard-controller，不要在内置组件上反复调 offset。

## 三个常见配置坑

- **`behavior` iOS/Android 要分叉**：iOS 用 `"padding"` 大多数情况 OK，Android 通常**不需要**这个组件——靠 `android:windowSoftInputMode="adjustResize"` 系统级处理（参见 [[wiki/frontend/react-native/rn-keyboard-pitfalls|RN 键盘坑点速查]]的 Android 全局配置一节）。强行套反而打架。常见写法：

  ```tsx
  behavior={Platform.OS === 'ios' ? 'padding' : undefined}
  ```

- **`keyboardVerticalOffset` 要手动算**：组件不知道头上有多高的 nav bar / status bar，offset 不对就会顶过头露出空白，或顶不够输入框还在键盘下。一般要把 `headerHeight + safeAreaInset.top` 喂给它。

- **嵌套 `ScrollView` / `SafeAreaView` 时表现混乱**：层级一深开始抽风，比如键盘起来时列表反而被压扁。这是切换到 keyboard-controller 的最常见动机。

## 标配模板

```tsx
<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : undefined}
  keyboardVerticalOffset={headerHeight}
  style={{ flex: 1 }}
>
  <FlashList ... />
  <TextInput ... />
</KeyboardAvoidingView>
```

> [!note] 复杂场景的接力
> 一旦你发现自己在反复调 `keyboardVerticalOffset`，或者要给嵌套结构加各种 hack——那就是该换 [[wiki/frontend/react-native/react-native-keyboard-controller|keyboard-controller]] 的信号。

## 延伸阅读

- [KeyboardAvoidingView 官方文档](https://reactnative.dev/docs/keyboardavoidingview)
