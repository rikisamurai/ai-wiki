---
title: iOS CJK 输入法被 controlled TextInput 打断
tags: [react-native, ios, text-input]
date: 2026-05-09
sources:
  - "[[sources/posts/frontend/React/React Native/learning/rn-ios-cjk-input-issue]]"
last-ingested: 2026-05-09
status: draft
---

React Native 在 iOS 上把 `TextInput` 写成 controlled（带 `value={value}`）时，每次 `onChangeText` 都会通过 native bridge 把 JS 侧 value 写回原生 `UITextField`，在一些版本和场景下会打断 IME 的 composition session，导致中文/日文/韩文选词异常。稳妥 workaround 是改成 [[wiki/frontend/react-native/textinput-controlled-vs-uncontrolled|uncontrolled]]，用 `ref` 命令式控制清空。

**现象**：搜索框 `TextInput` 用 `value={value}` 写成受控组件，iOS 中文输入下用户敲拼音/选词的过程可能被打断——每次按键触发 `onChangeText` 都把 JS state 的最新值同步回 `UITextField`，IME 还没等用户选完候选词就被覆盖。日文、韩文等其他 CJK IME 同理。

**根因**：iOS IME 的 composition 需要 native 端在选词期间保持 text buffer 不变。RN controlled TextInput 架构每次 `onChangeText` 都通过 native bridge 把 JS 侧 value 强制写回 `UITextField`，直接覆盖了 buffer，composition session 自然就断了。

> [!warning] 仍然要规避 controlled 风险
> 这个问题有长期历史（[#12599](https://github.com/react/react-native/issues/12599)）。其中 RN 0.54 的中文 controlled `TextInput` 回归（[#18403](https://github.com/react/react-native/issues/18403)）已被标记为 fixed，但 CJK IME + controlled input 仍容易受 RN 版本、平台实现和业务回写逻辑影响。生产搜索/聊天输入优先 uncontrolled。

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
- [#18403](https://github.com/react/react-native/issues/18403) — controlled TextInput broken for Chinese in v0.54 on iOS（当前标记为 fixed）
- [#18456 PR](https://github.com/react/react-native/pull/18456) — 相关修复尝试
- [#19339](https://github.com/react/react-native/issues/19339) — uncontrolled workaround 讨论
