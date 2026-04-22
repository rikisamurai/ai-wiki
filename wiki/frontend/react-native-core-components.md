---
title: React Native 核心组件
tags: [react-native, reference]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/React/React Native/learning/react-native-core-components]]"
last-ingested: 2026-04-22
status: draft
---

React Native 内置的一组跨平台 UI 组件和系统 API——RN 不能用 HTML 标签，所有界面都靠这些"基础积木"组合。本页是一份分类速查；性能/选型类的细节单独成页（如 [[wiki/frontend/flash-list|FlashList]]、[[wiki/frontend/pressable-vs-touchable|Pressable vs TouchableOpacity]]）。

> [!note] Web ↔ RN 心智映射
> `<div>` → `View`、`<span>/<p>` → `Text`、`<img>` → `Image`、`<input>` → `TextInput`、CSS → `StyleSheet`。**裸文字必须包 Text**，`<View>Hello</View>` 直接崩。

## 基础组件

| 组件 | Web 类比 | 用途 |
| --- | --- | --- |
| `View` | `<div>` | 容器，默认 flexbox |
| `Text` | `<span>` | 显示文字的唯一方式 |
| `Image` | `<img>` | 必须显式 width/height，否则不显示 |
| `TextInput` | `<input>` | 通过 `onChangeText` 取值 |
| `ScrollView` | `overflow: scroll` | 一次性渲染所有子元素，仅适合内容量小的场景 |
| `StyleSheet` | CSS | 创建样式对象，含校验和性能优化 |

## 列表组件

- `FlatList` — 内置虚拟滚动列表
- `SectionList` — 带分组标题的 FlatList
- 推荐：用 [[wiki/frontend/flash-list|FlashList]] 替代二者，[[wiki/frontend/view-recycling|View 回收]] 机制更不易白屏

> [!warning] ScrollView 不要装长列表
> 几百条数据用 ScrollView 会一次性渲染全部，严重卡顿。门槛大约几十条以上就该切 FlatList / FlashList。

## 交互组件

| 组件 | 选型建议 |
| --- | --- |
| `TouchableOpacity` | 历史项目最常用 |
| `Pressable` | 0.63+ 推荐，API 更灵活 |
| `Button` | 仅原型 |
| `Switch` | boolean 输入 |

详见 [[wiki/frontend/pressable-vs-touchable|Pressable vs TouchableOpacity]]。

## 布局与反馈

`Modal` / `ActivityIndicator` / `KeyboardAvoidingView` / `RefreshControl` / `StatusBar` / `Alert`（API 非组件）。

## 工具 API

| API | 用途 |
| --- | --- |
| `Dimensions` | 静态获取屏幕宽高，**旋转不更新**——用 `useWindowDimensions()` Hook 替代 |
| `PixelRatio` | 设备像素密度，处理 1px 边框 |
| `Linking` | 外链跳转 + 监听 DeepLink |
| `Animated` | 内置动画库 |
| `Platform` | 平台分支（`Platform.OS === 'ios'`） |

## 平台专属

- **Android**：`BackHandler`、`ToastAndroid`、`PermissionsAndroid`、`DrawerLayoutAndroid`
- **iOS**：`ActionSheetIOS`

## 常见坑

- 裸文字必须包 `<Text>`
- `Image` 必须显式尺寸
- `Dimensions` 静态、不响应旋转 → 用 `useWindowDimensions()`
- `ScrollView` 不要装长列表

## 延伸阅读

- [Core Components and APIs - React Native](https://reactnative.dev/docs/components-and-apis)
- [Animated 动画指南](https://reactnative.dev/docs/animated)
