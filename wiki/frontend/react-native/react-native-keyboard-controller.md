---
title: react-native-keyboard-controller
tags: [react-native, keyboard, library]
date: 2026-05-09
sources:
  - "[[sources/posts/frontend/React/React Native/learning/rn-keyboard-pitfalls]]"
last-ingested: 2026-05-09
status: draft
---

RN 社区目前公认最完善的键盘处理库（[kirillzyusko/react-native-keyboard-controller](https://github.com/kirillzyusko/react-native-keyboard-controller)）。提供原生级动画、跟手交互、`KeyboardAwareScrollView` 一站式 API，是 [[wiki/frontend/react-native/keyboard-avoiding-view|KeyboardAvoidingView]] 在生产项目里的事实替代。

## 核心能力对比

> [!compare] 对比 RN 内置 KeyboardAvoidingView
> | 能力 | KeyboardAvoidingView（内置） | keyboard-controller |
> | --- | --- | --- |
> | 动画 | JS 驱动，可能掉帧 | native 驱动，与系统键盘 60fps 同步 |
> | 跟手交互 | 不支持（一次性顶上去） | 支持（手指拖键盘时布局连动） |
> | 嵌套 `ScrollView` | 经常抽风 | 提供 `KeyboardAwareScrollView` 一体化 |
> | iOS/Android 一致性 | 要 `Platform.OS` 分叉 | 抹平差异 |
> | 键盘事件 | iOS 才有 `keyboardWillShow` | 跨平台都有 will/did 系列 |

## 何时该换过来

来自 [[wiki/frontend/react-native/rn-keyboard-pitfalls|RN 键盘坑点速查]]的经验：

- 嵌套布局（`KeyboardAvoidingView` 套 `ScrollView` 套 `SafeAreaView`）开始出诡异问题
- 需要键盘动画跟手——比如聊天界面要键盘上下拖动时输入框平滑跟随
- 想在 Android 上也用 `keyboardWillShow` 类的"动画前"事件
- `keyboardVerticalOffset` 反复调还是顶不准

## 延伸阅读

- [react-native-keyboard-controller GitHub](https://github.com/kirillzyusko/react-native-keyboard-controller)
- [官方文档站](https://kirillzyusko.github.io/react-native-keyboard-controller/)
