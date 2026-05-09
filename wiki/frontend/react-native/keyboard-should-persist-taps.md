---
title: keyboardShouldPersistTaps + keyboardDismissMode
tags: [react-native, keyboard, scrollview]
date: 2026-05-09
sources:
  - "[[sources/posts/frontend/React/React Native/learning/rn-keyboard-pitfalls]]"
last-ingested: 2026-05-09
status: draft
---

RN 列表组件（`ScrollView` / `FlatList` / [[wiki/frontend/react-native/flash-list|FlashList]]）和键盘交互的两个核心 prop。配错就出现"点搜索建议没反应""滚动不收键盘"等典型 bug——是 RN 搜索/聊天场景最常见的 bug 来源之一。

> [!compare] 两个 prop 的取值
> | prop | 取值 | 行为 |
> | --- | --- | --- |
> | `keyboardShouldPersistTaps` | `"never"`（默认） | 键盘开着时第一次点击只用来收键盘，**点不到列表项** |
> | | `"handled"` | 子元素有 `onPress` 就直接触发，否则收键盘 |
> | | `"always"` | 怎么点都不收键盘 |
> | `keyboardDismissMode` | `"none"`（默认） | 滚动不影响键盘 |
> | | `"on-drag"` | 手指开始拖就收 |
> | | `"interactive"` | iOS 跟手收，可以拖回来；Android 等同 `on-drag` |

## 默认值的坑

新手最常遇到的"我点了搜索建议它怎么没反应"——根因就是 `keyboardShouldPersistTaps` 默认 `"never"`。键盘开着时第一次点击只用来 dismiss 键盘，列表项的 `onPress` 根本没触发。

**绝大多数搜索/输入场景应显式设 `"handled"`**：

```tsx
<FlatList
  data={suggestions}
  renderItem={renderItem}
  keyboardShouldPersistTaps="handled"   // 第一次点击就能选中建议词
  keyboardDismissMode="interactive"     // iOS 跟手收键盘
/>
```

## FlashList 上的额外坑

[[wiki/frontend/react-native/flash-list|FlashList]] 把这两个 prop 转发给底层 `ScrollView`，但因为 [[wiki/frontend/react-native/view-recycling|View 回收]]机制，`keyboardShouldPersistTaps="handled"` 在快速滚动时偶尔会让某些 cell 的 `onPress` 失效。社区建议在 cell 内层套 [[wiki/frontend/react-native/pressable-vs-touchable|Pressable]] 处理点击，而不是依赖外层 list 的事件转发。

> [!note] 配套上下文
> 这对 prop 在 [[wiki/frontend/react-native/rn-keyboard-pitfalls|RN 键盘坑点速查]] 的"标配防坑组合"里和 [[wiki/frontend/react-native/keyboard-avoiding-view|KeyboardAvoidingView]] 一起出场，是搜索 / 聊天场景的标配。

## 延伸阅读

- [ScrollView keyboardShouldPersistTaps](https://reactnative.dev/docs/scrollview#keyboardshouldpersisttaps)
- [ScrollView keyboardDismissMode](https://reactnative.dev/docs/scrollview#keyboarddismissmode)
