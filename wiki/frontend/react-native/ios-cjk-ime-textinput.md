---
title: iOS CJK 输入法被 controlled TextInput 打断
tags: [react-native, ios, text-input]
date: 2026-05-09
sources:
  - "[[sources/posts/frontend/React/React Native/learning/rn-ios-cjk-input-issue]]"
last-ingested: 2026-05-09
status: draft
---

React Native 在 iOS 上把 `TextInput` 写成 controlled（带 `value={value}`）时，每次 `onChangeText` 都会通过 native bridge 把 JS 侧 value 强制写回原生 `UITextField`，打断 IME 的 composition session，导致中文/日文/韩文选词无法完成。Workaround 是改成 [[wiki/frontend/react-native/textinput-controlled-vs-uncontrolled|uncontrolled]]，用 `ref` 命令式控制清空。

**现象**：搜索框 `TextInput` 用 `value={value}` 写成受控组件，iOS 中文输入下用户敲拼音/选词的过程会被打断——每次按键触发 `onChangeText` 都会把 JS state 的最新值同步回 `UITextField`，IME 还没等用户选完候选词就被中断，结果中文根本打不进去。日文、韩文等其他 CJK IME 同理。

**根因**：iOS IME 的 composition 需要 native 端在选词期间保持 text buffer 不变。RN controlled TextInput 架构每次 `onChangeText` 都通过 native bridge 把 JS 侧 value 强制写回 `UITextField`，直接覆盖了 buffer，composition session 自然就断了。

> [!warning] 这个问题官方修不了
> 从 2016 年就有人报告（[#12599](https://github.com/facebook/react-native/issues/12599)），受限于 RN controlled input 的核心架构，至今没有彻底修复。业内通用方案就是改 uncontrolled。

**解决方案**：把 `TextInput` 改成 [[wiki/frontend/react-native/textinput-controlled-vs-uncontrolled|uncontrolled]]——

- 移除 `value` prop（如需初始值用 `defaultValue`）
- 用 `ref` 拿到组件实例，需要清空时调 `.clear()` 或 `.setNativeProps({ text: '' })`
- 业务 state 仍可在 `onChangeText` 里维护，只是不再回写到组件

```tsx
import { useRef, useState } from 'react';
import { TextInput, TouchableOpacity, Text } from 'react-native';

const SearchBar = () => {
  const inputRef = useRef<TextInput>(null);
  const [keyword, setKeyword] = useState('');

  const handleClear = () => {
    inputRef.current?.clear();
    setKeyword('');
  };

  return (
    <>
      <TextInput
        ref={inputRef}
        defaultValue=""
        onChangeText={setKeyword}
        placeholder="搜索"
      />
      <TouchableOpacity onPress={handleClear}>
        <Text>清空</Text>
      </TouchableOpacity>
    </>
  );
};
```

> [!tip] 代价：失去声明式回写能力
> 改 uncontrolled 之后，组件内部 text 由 native 持有，JS 侧 state 只能"读"不能"写"。如果业务确实需要 JS 主动改输入框内容（比如点击建议词回填），都要走 `ref.setNativeProps({ text: ... })` 这条命令式路径，不能再依赖 React 声明式数据流。这是 RN 现阶段 IME 兼容的代价。

## 延伸阅读

- 在 [[wiki/frontend/react-native/react-native-core-components|RN 核心组件]] 矩阵中，`TextInput` 是 `<input>` 的对应物
- [#18403](https://github.com/facebook/react-native/issues/18403) — controlled TextInput broken for Chinese in v0.54 on iOS（最权威根因描述）
- [#18455](https://github.com/facebook/react-native/issues/18455) — composition 被打断的核心 issue
- [#18456 PR](https://github.com/facebook/react-native/pull/18456) — 官方未完全解决的修复尝试
- [#19339](https://github.com/facebook/react-native/issues/19339) — uncontrolled workaround 讨论
