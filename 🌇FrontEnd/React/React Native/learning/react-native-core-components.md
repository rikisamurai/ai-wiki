---
title: React Native 核心组件
tags:
  - learning
  - react-native
date: 2026-04-09
---

**一句话**：React Native 内置了一组跨平台 UI 组件和系统 API，它们是构建所有 RN 界面的基础积木——就像 Web 中的 `<div>`、`<span>`、`<img>` 一样。

**为什么需要了解它们**：RN 不能直接使用 HTML 标签，所有 UI 都由这些核心组件组合而成。掌握它们才知道"拿什么来搭界面"，以及什么时候该用第三方组件（比如 [[flash-list|FlashList]]）替代。

**基础组件**

| 组件 | Web 类比 | 说明 |
|------|---------|------|
| `View` | `<div>` | 最基础的容器，用于布局（默认 flexbox） |
| `Text` | `<span>` | 显示文字的唯一方式，不能把裸文字直接放在 `View` 里 |
| `Image` | `<img>` | 显示图片，支持网络图片、本地资源、base64 |
| `TextInput` | `<input>` | 文本输入框，通过 `onChangeText` 获取输入 |
| `ScrollView` | `overflow: scroll` 的 `<div>` | 可滚动容器，适合内容量少的场景 |
| `StyleSheet` | CSS stylesheet | 创建样式对象，提供校验和性能优化 |

```tsx
import { View, Text, Image, StyleSheet } from 'react-native';

const Profile = () => (
  <View style={styles.container}>
    <Image source={{ uri: 'https://example.com/avatar.png' }} style={styles.avatar} />
    <Text>Hello World</Text>
  </View>
);

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center' },
  avatar: { width: 80, height: 80, borderRadius: 40 },
});
```

**列表组件**

| 组件 | 说明 |
|------|------|
| `FlatList` | 高性能长列表，只渲染可见区域（类似虚拟滚动） |
| `SectionList` | 带分组标题的 FlatList |

> [!tip] ScrollView vs FlatList
> `ScrollView` 会一次性渲染所有子元素，适合内容少的页面。数据量大（几十条以上）必须用 `FlatList`，否则会卡顿。项目中更常用的是第三方的 [[flash-list|FlashList]]，性能更好。

```tsx
import { FlatList } from 'react-native';

<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <Text>{item.name}</Text>}
/>
```

**交互组件**

| 组件 | 说明 |
|------|------|
| `TouchableOpacity` | 点击时透明度变化的可触摸区域，项目中最常用的点击容器 |
| `Pressable` | 更灵活的触摸组件（0.63+ 推荐），支持 pressed 状态自定义样式 |
| `Button` | 最简单的按钮，样式固定，通常只用于快速原型 |
| `Switch` | 开关控件，渲染一个 boolean 输入 |

```tsx
import { TouchableOpacity, Text } from 'react-native';

<TouchableOpacity onPress={() => console.log('tapped')} activeOpacity={0.7}>
  <Text>点击我</Text>
</TouchableOpacity>
```

**布局与反馈**

| 组件 | 说明 |
|------|------|
| `Modal` | 在当前页面上方弹出浮层 |
| `ActivityIndicator` | 加载中的旋转菊花 |
| `KeyboardAvoidingView` | 键盘弹起时自动调整布局，避免输入框被遮挡 |
| `RefreshControl` | 放在 ScrollView/FlatList 中实现下拉刷新 |
| `StatusBar` | 控制顶部状态栏（颜色、是否隐藏等） |
| `Alert` | 弹出系统原生对话框（不是组件，是 API 调用） |

```tsx
import { Alert } from 'react-native';

Alert.alert('提示', '确认删除？', [
  { text: '取消', style: 'cancel' },
  { text: '删除', onPress: () => handleDelete(), style: 'destructive' },
]);
```

**工具 API**

| API | 说明 |
|-----|------|
| `Dimensions` | 获取屏幕宽高（`Dimensions.get('window')`） |
| `PixelRatio` | 获取设备像素密度，用于处理 1px 边框等精细场景 |
| `Linking` | 打开外部链接、DeepLink 跳转，也能监听 App 被外部链接唤起 |
| `Animated` | 动画库，支持弹性、衰减、时间等多种动画类型 |
| `Platform` | 判断当前平台（`Platform.OS === 'ios'`），做平台差异处理 |

```tsx
import { Dimensions, Platform, PixelRatio } from 'react-native';

const { width, height } = Dimensions.get('window');
const isIOS = Platform.OS === 'ios';
const hairlineWidth = 1 / PixelRatio.get(); // 最细的一条线
```

**平台专属**

- **Android**：`BackHandler`（监听返回键）、`ToastAndroid`（Toast 提示）、`PermissionsAndroid`（运行时权限申请）、`DrawerLayoutAndroid`（抽屉布局）
- **iOS**：`ActionSheetIOS`（底部弹出菜单 / 分享面板）

**在项目中的使用**

项目中最常用的核心组件是 `View`、`Text`、`Image`、`StyleSheet`、`TouchableOpacity` 和 `Animated`，几乎每个页面都会 import：

- `wakanda-rn-monorepo/apps/wassabi-rn/src/pages/Home/App.tsx` — 使用 View、StyleSheet、StatusBar、Platform
- `wakanda-rn-monorepo/apps/wassabi-rn/src/pages/Home/renderer.tsx` — 使用 View、Animated、ActivityIndicator 实现带加载动画的渲染器
- `wakanda-comp-rn/packages/vbm-coupon-card/src/components/CouponCardContainerRight/CouponCardContainerRight.tsx` — 使用 View、Text、TouchableOpacity、Image 构建卡片组件
- `wakanda-rn-monorepo/shared/utils/useScreenDimensions.ts` — 使用 Dimensions 封装屏幕尺寸 Hook

> [!note]
> 项目中没有直接使用 `FlatList`，长列表场景用的是性能更好的第三方 [[flash-list|FlashList]]。`Button`、`Switch`、`Pressable` 也很少出现，交互按钮主要用 `TouchableOpacity` 或自封装组件。

**常见坑 / 注意事项**

- **裸文字报错**：所有文字必须包在 `<Text>` 里，`<View>Hello</View>` 会直接崩溃
- **Image 必须指定尺寸**：网络图片不会自动撑开，不给 width/height 就什么都看不到
- **ScrollView 不要装长列表**：几百条数据用 ScrollView 会一次性全部渲染，导致严重卡顿
- **Dimensions 是静态值**：屏幕旋转后不会自动更新，需要用 `useWindowDimensions()` Hook 代替
- **TouchableOpacity vs Pressable**：新代码推荐用 `Pressable`，但项目中历史代码大量使用 `TouchableOpacity`，保持一致即可

**延伸阅读**

- [Core Components and APIs - React Native](https://reactnative.dev/docs/components-and-apis)
- [FlatList 详解](https://reactnative.dev/docs/flatlist)
- [Animated 动画指南](https://reactnative.dev/docs/animated)
