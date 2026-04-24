---
title: React Native 键盘相关坑点总览
tags:
  - react-native
  - keyboard
  - learning
date: 2026-04-24
---

> [!abstract] 一句话
> RN 键盘相关 API 散在 `TextInput` / `ScrollView` / `KeyboardAvoidingView` / `Keyboard` / Android Manifest 五处，behavior 在 iOS/Android 经常分叉。这篇是踩坑总览，每条只讲"现象 + 根因 + 解法"，需要深入的单点（如 [[rn-ios-cjk-input-issue|iOS CJK IME composition]]）拆到独立笔记。

## TextInput 本身

- **iOS CJK IME 被 controlled `value` 打断** — 详见 [[rn-ios-cjk-input-issue|iOS 中文输入法下 controlled TextInput 打断 composition]]。根因是 controlled `value` 通过 native bridge 强制覆盖 buffer 打断 composition session；解法是改 uncontrolled。
- **`autoFocus` 在 iOS 上经常不弹键盘**：尤其在 `Modal` / 路由切换刚 mount 时——焦点拿到了，软键盘没起来。常见 hack 是在 `useEffect` 里 `setTimeout(() => ref.focus(), 100)` 手动再调一次。
- **`multiline` 下回车键被吞**：iOS 上 `multiline` + `returnKeyType="search"` 这类组合会让回车既不换行也不触发 onSubmit。要么去掉 `returnKeyType`，要么自己监听 `onKeyPress` 处理 `\n`。
- **`blurOnSubmit` 默认值不一致**：单行 `TextInput` 默认 `true`（提交后收键盘），multiline 默认 `false`（继续编辑）。需要反着来必须显式设。
- **`secureTextEntry` 切换后联想失效**：从密码框切回普通输入时 iOS 会保留 secure 状态导致 `autoCorrect` 失效，需要重新挂载组件（换 key）。

## ScrollView / FlatList / FlashList 与键盘交互

这块有两个相辅相成的属性，配错了就出现"点搜索建议没反应""滚动不收键盘"等典型 bug：

- **`keyboardShouldPersistTaps`**（点击列表项时键盘要不要先收起）
  - `"never"`（默认）：键盘开着时第一次点击只用来收键盘，**点不到列表项**——新手最常遇到的"我点了搜索建议它怎么没反应"的根因
  - `"handled"`：如果子元素有 `onPress` 就直接触发，否则收键盘——**绝大多数搜索/输入场景用这个**
  - `"always"`：怎么点都不收键盘
- **`keyboardDismissMode`**（滚动时键盘要不要收）
  - `"none"`（默认）：滚动不影响键盘
  - `"on-drag"`：手指开始拖就收
  - `"interactive"`（iOS 专属，Android 等同 `on-drag`）：跟手收，可以拖回来——体验最好
- **[[flash-list|FlashList]] 上的额外坑**：FlashList 把这两个 prop 转发给底层 `ScrollView`，但因为 View 回收机制，`keyboardShouldPersistTaps="handled"` 在快速滚动时偶尔会让某些 cell 的 `onPress` 失效。社区建议在 cell 内层套 `Pressable` 处理点击，而不是依赖外层 list 的事件转发。

## KeyboardAvoidingView 是个半成品

> [!warning] 复杂场景直接换库
> `KeyboardAvoidingView` 是 RN 内置的"够用版"，稍微复杂就开始抽风。生产项目推荐直接用 [react-native-keyboard-controller](https://github.com/kirillzyusko/react-native-keyboard-controller)——社区目前公认最完善方案，提供原生级动画、跟手交互、`KeyboardAwareScrollView` 一站式 API。

- **`behavior` iOS/Android 要分叉**：iOS 用 `"padding"` 大多数情况 OK，Android 通常不需要这个组件（靠 `android:windowSoftInputMode="adjustResize"` 系统级处理），强行套反而打架。常见写法：`behavior={Platform.OS === 'ios' ? 'padding' : undefined}`。
- **`keyboardVerticalOffset` 要手动算**：组件不知道头上有多高的 nav bar / status bar，offset 不对就会顶过头露出空白，或顶不够输入框还在键盘下。
- **嵌套 `ScrollView` / `SafeAreaView` 时表现混乱**：层级一深开始抽风，比如键盘起来时列表反而被压扁。

## Android 全局配置坑

- **`android:windowSoftInputMode`**（在 `AndroidManifest.xml` 的 `<activity>` 上）
  - `adjustResize`：键盘起来时 resize 整个 window，内容自动避让——**RN 默认推荐**
  - `adjustPan`：整个 window 上推，焦点输入框露出来但顶部内容被推到屏幕外
  - `adjustNothing`：什么都不做，输入框被键盘直接遮住
- **沉浸式 / edge-to-edge 模式下 `adjustResize` 失效**：开了 translucent status bar 或 edge-to-edge 后，Android 不再自动 resize，需要手动监听键盘高度调整布局。
- **Android 11+ WindowInsets API 行为变了**：旧的 `softInputMode` 在新版本上和 `setDecorFitsSystemWindows(false)` 一起用会有时序问题。

## Keyboard API 跨平台陷阱

- **事件命名 iOS/Android 不对齐**：iOS 有 `keyboardWillShow` / `keyboardWillHide`（动画**前**），Android 只有 `keyboardDidShow` / `keyboardDidHide`（动画**后**）。想做平滑过渡只能在 iOS 上用 will 系列。
- **键盘高度语义不一致**：`event.endCoordinates.height` 在 iOS 上**不**包含 safe area inset（Home Indicator 那块），Android 上有时会包含 nav bar 高度——精确布局时要分别校准。
- **`Keyboard.dismiss()` 偶尔不收**：在某些自定义键盘场景下（比如系统键盘 + 表情面板）只能通过 `ref.blur()` 强制收。

## 标配防坑组合（搜索 / 聊天场景）

```tsx
import { Platform, KeyboardAvoidingView, TextInput } from 'react-native';
import { FlashList } from '@shopify/flash-list';

<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : undefined}
  keyboardVerticalOffset={headerHeight}
  style={{ flex: 1 }}
>
  <FlashList
    data={suggestions}
    renderItem={({ item }) => <SuggestionItem item={item} />}
    keyboardShouldPersistTaps="handled"   // 第一次点击就能选中建议词
    keyboardDismissMode="interactive"     // iOS 跟手收键盘
    estimatedItemSize={56}
  />
  <TextInput
    defaultValue=""                       // 注意：uncontrolled，避开 CJK IME 坑
    onChangeText={setKeyword}
    placeholder="搜索"
  />
</KeyboardAvoidingView>
```

四个关键点：

1. `KeyboardAvoidingView` 仅在 iOS 启用，Android 走系统 `adjustResize`
2. 列表 `keyboardShouldPersistTaps="handled"` 让点击建议词不需要先收键盘
3. 列表 `keyboardDismissMode="interactive"` 让用户拖列表时跟手收键盘
4. 输入框用 `defaultValue` 而不是 `value`，避开中文输入法 composition 被打断的问题

## 延伸阅读

- [TextInput 官方文档](https://reactnative.dev/docs/textinput)
- [ScrollView keyboardShouldPersistTaps](https://reactnative.dev/docs/scrollview#keyboardshouldpersisttaps)
- [KeyboardAvoidingView 官方文档](https://reactnative.dev/docs/keyboardavoidingview)
- [react-native-keyboard-controller](https://github.com/kirillzyusko/react-native-keyboard-controller) — 社区推荐的完整解决方案
