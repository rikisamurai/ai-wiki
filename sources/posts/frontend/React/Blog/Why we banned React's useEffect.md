---
title: "No useEffect：Factory 团队的前端规则"
tags:
  - React
  - useEffect
  - best-practices
date: 2026-03-18
---

# No useEffect

> [!info] 原文
> [Alvin Sng (@alvinsng) on X](https://x.com/alvinsng/status/2033969062834045089) — Factory 团队分享的前端工程实践

Factory 团队有一条简单但重要的前端规则：==禁止直接使用 useEffect==。听起来很极端，但实践证明它让代码库更容易理解，也更难意外破坏。

## 为什么禁用 useEffect？

Factory 并非一开始就有这条规则，而是通过**生产环境的 bug** 总结出来的。大量 useEffect 的使用本质上是在补偿 React 已经提供了更好原语的场景：派生状态、事件处理器、数据请求抽象。

> [!warning] AI 编码时代更需要这条规则
> 当 Agent 在写代码时，useEffect 经常被"以防万一"地添加，而这恰恰是下一个竞态条件或无限循环的种子。禁用这个 Hook 迫使逻辑变得声明式和可预测。

## useEffect 带来的问题

- **脆弱性（Brittleness）**：依赖数组隐藏了耦合关系，一个看似无关的重构可能悄悄改变 Effect 行为
- **无限循环（Infinite loops）**：`state 更新 → 渲染 → effect → state 更新` 的循环很容易产生，尤其是依赖列表被逐步"修复"时
- **依赖地狱（Dependency hell）**：Effect 链（A 设置状态触发 B）是基于时间的控制流，难以追踪且容易退化
- **调试困难（Debugging pain）**：你最终会问"这为什么执行了？"或"这为什么没执行？"，却没有像 handler 那样清晰的入口点

## React 官方也这么认为

React 官方有一篇完整的指南：[You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)。

核心问题是：useEffect 将很多团队从**显式的事件驱动逻辑**转向了**隐式的同步逻辑**。你不再是响应一个清晰的事件，而是在通过依赖数组管理值和副作用之间的关系。

## 5 条替代规则

### Rule 1：派生状态，而非同步状态

大多数从其他 state 设置 state 的 Effect 都是不必要的，还会多一次渲染。

```typescript
// ❌ BAD: 两次渲染周期 — 先过期，再过滤
function ProductList() {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);

  useEffect(() => {
    setFilteredProducts(products.filter((p) => p.inStock));
  }, [products]);
}

// ✅ GOOD: 一次渲染内联计算
function ProductList() {
  const [products, setProducts] = useState([]);
  const filteredProducts = products.filter((p) => p.inStock);
}
```

循环陷阱示例：

```typescript
// ❌ BAD: total 在依赖中可能导致循环
function Cart({ subtotal }) {
  const [tax, setTax] = useState(0);
  const [total, setTotal] = useState(0);

  useEffect(() => { setTax(subtotal * 0.1); }, [subtotal]);
  useEffect(() => { setTotal(subtotal + tax); }, [subtotal, tax, total]);
}

// ✅ GOOD: 无需 Effect
function Cart({ subtotal }) {
  const tax = subtotal * 0.1;
  const total = subtotal + tax;
}
```

> [!tip] Smell Test
> - 你正要写 `useEffect(() => setX(deriveFromY(y)), [y])`
> - 你有只是镜像其他 state 或 props 的 state

### Rule 2：使用数据请求库

基于 Effect 的数据请求经常产生竞态条件和重复的缓存逻辑。

```typescript
// ❌ BAD: 竞态条件风险
function ProductPage({ productId }) {
  const [product, setProduct] = useState(null);

  useEffect(() => {
    fetchProduct(productId).then(setProduct);
  }, [productId]);
}

// ✅ GOOD: Query 库处理取消/缓存/过期
function ProductPage({ productId }) {
  const { data: product } = useQuery(['product', productId], () =>
    fetchProduct(productId)
  );
}
```

> [!tip] Smell Test
> - 你的 Effect 里有 `fetch(...)` 然后 `setState(...)`
> - 你在重新实现缓存、重试、取消或过期处理

### Rule 3：事件处理器，而非 Effect

如果用户点击了按钮，就在 handler 里完成工作。

```typescript
// ❌ BAD: Effect 作为动作中继
function LikeButton() {
  const [liked, setLiked] = useState(false);

  useEffect(() => {
    if (liked) { postLike(); setLiked(false); }
  }, [liked]);

  return <button onClick={() => setLiked(true)}>Like</button>;
}

// ✅ GOOD: 直接的事件驱动动作
function LikeButton() {
  return <button onClick={() => postLike()}>Like</button>;
}
```

> [!tip] Smell Test
> - State 被当作标志位，让 Effect 去执行真正的动作
> - 你在构建"设置标志 → Effect 运行 → 重置标志"的机制

### Rule 4：useMountEffect 用于一次性外部同步

`useMountEffect` 只是 `useEffect(..., [])` 的命名包装，让意图更明确，并防止组件中的临时 Effect 使用。

```typescript
function useMountEffect(callback: () => void | (() => void)) {
  useEffect(callback, []);
}
```

适用场景：DOM 集成（focus、scroll）、第三方 widget 生命周期、Browser API 订阅。

条件挂载模式：

```typescript
// ❌ BAD: Effect 内部守卫
function VideoPlayer({ isLoading }) {
  useEffect(() => {
    if (!isLoading) playVideo();
  }, [isLoading]);
}

// ✅ GOOD: 前置条件满足后再挂载
function VideoPlayerWrapper({ isLoading }) {
  if (isLoading) return <LoadingScreen />;
  return <VideoPlayer />;
}

function VideoPlayer() {
  useMountEffect(() => playVideo());
}
```

### Rule 5：用 key 重置，而非依赖编排

```typescript
// ❌ BAD: Effect 试图模拟重新挂载行为
function VideoPlayer({ videoId }) {
  useEffect(() => { loadVideo(videoId); }, [videoId]);
}

// ✅ GOOD: key 强制干净的重新挂载
function VideoPlayer({ videoId }) {
  useMountEffect(() => { loadVideo(videoId); });
}

function VideoPlayerWrapper({ videoId }) {
  return <VideoPlayer key={videoId} videoId={videoId} />;
}
```

> [!tip] Smell Test
> - 你在写一个唯一作用是"当 ID/prop 变化时重置本地状态"的 Effect
> - 你希望组件对每个实体表现得像一个全新实例

## 组件设计的强制函数

![[Pasted image 20260318190815.png]]

禁止直接使用 useEffect 成为更干净组件树设计的**强制函数**：

- 父组件拥有编排和生命周期边界
- 子组件可以假设前置条件已经满足
- 更简单的组件，更少的隐藏副作用

这基本上是 ==Unix 哲学应用于 React 组件==：每个单元做一件事，协调发生在清晰的边界。

## 选择你的 Bug

没有团队能做到零 bug，问题是你想要哪种失败模式：
![[Pasted image 20260318190942.png]]

| | useMountEffect | 直接 useEffect |
|---|---|---|
| 失败模式 | 二元且明显（执行了或没执行） | 逐渐退化，表现为 flaky 行为、性能问题或循环 |

## 如何采用这条规则

- 通过 **lint 规则** 强制执行
- 在 `AGENTS.md` 中为 AI Agent 提供清晰的指导
- 使用 Factory 的 Missions 产品批量修复现有违规
