---
title: iOS 中文输入法下 controlled TextInput 打断 composition
tags:
  - react-native
  - ios
  - text-input
date: 2026-04-23
---

> [!abstract] 一句话
> React Native 在 iOS 上把 `TextInput` 写成 controlled（带 `value={value}`）时，每次 `onChangeText` 都会通过 native bridge 把 JS 侧的 value 强制写回原生 `UITextField`，打断中文输入法的 composition session，导致选词无法完成。Workaround：去掉 `value` prop 改 uncontrolled，用 `ref` 命令式控制清空。

**现象**：搜索框 `TextInput` 用 `value={value}` 写成受控组件，iOS 中文输入时每次按键触发 `onChangeText` 都会重新渲染并把 JS 侧的 value 强制写回原生 `UITextField`，打断 IME 的 composition session——拼音选词面板还没等用户敲完拼音/选好候选词就被中断，结果就是中文根本打不进去（日文、韩文等其他 CJK 输入法同理）。

**根因**：React Native 的 controlled `TextInput` 架构决定的——每次 `onChangeText` 都会通过 native bridge 把 JS 侧的 value 强制同步回原生 `UITextField`，而 iOS IME 的 composition 需要 native 端在选词期间保持 text buffer 不变，强制同步直接把 buffer 覆盖掉，composition session 自然就断了。这个问题从 2016 年就有人报告，受限于 RN controlled input 的核心架构，官方至今未彻底修复，业内通用方案就是改成 uncontrolled。

**解决方案**：把 `TextInput` 改成 uncontrolled——

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

> [!tip] 受控 vs 非受控的取舍
> 改成 uncontrolled 之后，组件内部 text 由 native 端持有，JS 侧 state 只能"读"不能"写"。如果业务确实需要 JS 主动修改输入框内容（比如点击建议词回填），都要走 `ref.setNativeProps({ text: ... })` 这条命令式路径，不能再依赖 React 的声明式数据流。这个 trade-off 是 RN 现阶段 IME 兼容的代价。

**参考链接**：

- [facebook/react-native#18403](https://github.com/facebook/react-native/issues/18403) — "Controlled TextInput broken for Chinese (and other languages) in v0.54 on iOS"，最权威的根因描述
- [facebook/react-native#18455](https://github.com/facebook/react-native/issues/18455) — controlled TextInput 打断 composition 的核心 issue
- [facebook/react-native#18456 (PR)](https://github.com/facebook/react-native/pull/18456) — 官方尝试修复的 PR，未完全解决
- [facebook/react-native#19339](https://github.com/facebook/react-native/issues/19339) — uncontrolled 作为 workaround 的相关讨论
- [facebook/react-native#12599](https://github.com/facebook/react-native/issues/12599) — 2016 年最早的同类报告
- [简书：React Native iOS TextInput 中文输入问题](https://www.jianshu.com/p/21522f7a492e) — 中文文章，含代码示例
- [codeleading：相关讨论](https://codeleading.com/article/43371747111/) — 中文参考
