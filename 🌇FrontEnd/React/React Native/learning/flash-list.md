---
title: FlashList
tags:
  - learning
  - react-native
date: 2026-04-09
---

**一句话**：FlashList 是 Shopify 开源的高性能 React Native 列表组件，通过 View 回收机制替代 FlatList，解决长列表滚动时出现白屏/空白单元格的问题。

**为什么需要它**：React Native 自带的 FlatList 在渲染大量数据时，快速滚动会出现"白屏闪烁"——因为 FlatList 在滚动时销毁屏幕外的 View 再重新创建，来不及渲染就看到空白。FlashList 借鉴了 Android RecyclerView 的思路，不销毁 View 而是**回收复用**，已经渲染过的 View 直接拿来填充新数据，所以滚动更快、更流畅。

**核心概念**：

- **View 回收（Recycling）** — 滚出屏幕的 View 不会被销毁，而是放进"回收池"，滚入新内容时直接复用这个 View、只更新数据。这是 FlashList 性能优于 FlatList 的根本原因
- **estimatedItemSize** — 告诉 FlashList 每个 item 大概多高（单位 px），用于在实际渲染前预估布局。不需要精确，给个大致值就行。v2 已经不再需要这个参数
- **getItemType** — 当列表中有多种类型的 item 时（比如商品卡片、分割线、广告位），通过这个函数告诉 FlashList 不同类型，这样同类型的 View 才会互相回收，避免回收错误类型导致闪烁
- **drawDistance** — 控制屏幕外预渲染的距离（px），值越大提前渲染越多内容，滚动更不容易白屏，但会多消耗一些内存

**基本用法**：

```tsx
import { FlashList } from '@shopify/flash-list'

const MyList = () => {
  const data = [{ id: '1', title: 'Item 1' }, { id: '2', title: 'Item 2' }]

  return (
    <FlashList
      data={data}
      renderItem={({ item }) => <Text>{item.title}</Text>}
      estimatedItemSize={50}
      keyExtractor={(item) => item.id}
    />
  )
}
```

API 和 FlatList 几乎一致，迁移时只需要：
1. 把 `import { FlatList }` 改成 `import { FlashList }`
2. 加上 `estimatedItemSize` 属性
3. 如果有多种 item 类型，加上 `getItemType`

**在项目中的使用**：

项目中大量使用 FlashList 替代 FlatList，以下是几个典型场景：

- `redbook/market-promotion/src/containers/my-submission/components/NoteList.tsx` — 笔记列表，使用了 `estimatedItemSize={114}`、`onViewableItemsChanged` 做曝光埋点、`onEndReached` 做分页加载
- `redbook/armor/components/cart-v3-flashlist/views/seller-sections/index.tsx` — 购物车商品列表，使用了 `getItemType` 区分不同类型的 section item、`drawDistance` 预渲染一屏内容、`viewabilityConfigCallbackPairs` 做精细化曝光控制
- `redbook/armor/packages/lancer-life/src/containers/red-card-list/` — 红卡列表，注释中明确写到"使用 FlashList 替代 SectionList 提升性能"

项目还有一个内部 fork 版本 `@xhs/flash-list`（版本 1.7.4-red.5），在 `pnpm-lock.yaml` 中可以看到，用于做一些定制化适配。

**常见坑 / 注意事项**：

- **必须设置 estimatedItemSize**（v1）：不设置会有 warning，且性能会下降。给一个列表中最常见 item 的高度就好
- **getItemType 很重要**：如果列表有多种 item（比如 header + 商品 + footer），不设置 `getItemType` 会导致不同类型的 View 互相回收，出现布局错乱或闪烁
- **不要在 renderItem 里用 index 作为 key**：和 FlatList 一样的规则，但在 FlashList 中违反这个规则的后果更明显（回收复用时数据错位）
- **嵌套滚动场景**：项目中购物车使用了 `NestedScrollView` 作为 `renderScrollComponent`，这是因为 FlashList 嵌套在其他 ScrollView 里时需要特殊处理
- **v2 只支持新架构**：FlashList v2 完全基于 React Native 新架构（Fabric），不支持旧架构。如果项目还没迁移新架构，只能用 v1

**延伸阅读**：

- [FlashList GitHub](https://github.com/Shopify/flash-list)
- [FlashList 官方文档](https://shopify.github.io/flash-list/)
- [从 FlatList 迁移指南](https://shopify.github.io/flash-list/docs/migrating-from-flatlist)
