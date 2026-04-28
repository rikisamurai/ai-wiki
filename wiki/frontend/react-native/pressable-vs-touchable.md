---
title: Pressable vs TouchableOpacity
tags: [react-native, best-practices]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/React/React Native/learning/react-native-core-components]]"
last-ingested: 2026-04-22
status: draft
---

React Native 里两种主流的可点击容器选型。`TouchableOpacity` 是老 API，按下时只能改变透明度；`Pressable`（0.63+）是新一代，提供 `pressed` 状态、长按、hover 等更细的回调。新代码推荐 Pressable，但既有项目里 TouchableOpacity 仍占多数——一致性优先于"新即好"。详见 [[wiki/frontend/react-native/react-native-core-components|RN 核心组件]]。

> [!compare] 选型对照
> | 维度 | TouchableOpacity | Pressable |
> | --- | --- | --- |
> | 引入 | 老 API，至今广泛存在 | RN 0.63+ |
> | 反馈 | 仅按下变透明 | 任意样式可基于 `pressed` 切换 |
> | 状态回调 | `onPress` / `onLongPress` | + `onPressIn` / `onPressOut` / `onHoverIn` 等 |
> | hit slop / 延迟 | 支持但 API 散 | 集中在 `hitSlop` / `pressRetentionOffset` |
> | 选用建议 | 历史项目延续 | 新组件首选 |

## 何时切换

- **新组件**：默认 Pressable
- **存量项目**：保持 TouchableOpacity 一致性，不要为了"新"而散乱混用
- **需要按下态自定义**（背景色、缩放、阴影变化）：必须 Pressable，TouchableOpacity 做不到

> [!example] Pressable 按下态
> ```tsx
> <Pressable
>   onPress={onTap}
>   style={({ pressed }) => [
>     styles.btn,
>     pressed && { backgroundColor: '#eee' },
>   ]}
> >
>   <Text>点击我</Text>
> </Pressable>
> ```
> TouchableOpacity 只能用 `activeOpacity` 改透明度，无法换背景色。

**反例**：

- **滥用 Button**：内置 `Button` 样式固定，仅适合原型；生产代码几乎不用
- **混用风格**：同一页面一会 TouchableOpacity 一会 Pressable，维护成本高于新 API 的收益

**关联**：[[wiki/frontend/react-native/react-native-core-components|RN 核心组件]] / [[wiki/frontend/react-native/flash-list|FlashList]]（长列表里 Pressable 是事实标准）
