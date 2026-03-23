---
title: CDP 视角下的 Browser 控制边界
tags:
  - browser-use
  - cdp
date: 2026-03-23
---

# CDP 视角下的 Browser 控制边界

> [!info] 文章来源
> 原文：[CDP 视角下的 Browser 控制边界](https://supercodepower.com/what-can-cdp-do-in-browser-use)

## 能力边界总览

如果把人类对电脑的所有操作记为全集，那么各层级可操作的范围如下：

- **Computer**：所有操作的全集
- **Browser**：App 层权限，出于安全限制了许多能力（如直接操作本地文件）
- **CDP**：专注于 Debug 能力，浏览器的非调试信息（如收藏网页）无权限访问
- **Puppeteer**：基于 CDP 构建，但未用到全部 CDP API，能力是 CDP 的子集


在 Browser-Use 场景中，CDP 是有能力边界的。了解它擅长什么、不擅长什么，对架构设计和演化方向有很大意义。

支持难度分类：

- **直接支持**：Puppeteer 有封装好的现成 API
- **间接支持**：需要组合多个 Puppeteer/CDP API 实现
- **不能支持**：CDP 完全做不到

---

## 一、浏览器功能

### Tabs（标签页管理）

- **必要性**：高 | **支持度**：间接支持

Tabs 是非常重要的功能，但 CDP 的 Tabs API 能力较弱，Puppeteer 也没有做相关抽象封装。实现「新建/更新/切换/关闭」需要组合多个 CDP API 间接实现。

![[Pasted image 20260323215327.png]]

> [!warning] 限制
> 如果 Tabs 被用户拖拽改变了显示顺序，CDP 无法感知这一变化。

### Navigate（页面导航）

- **必要性**：高 | **支持度**：直接支持

Navigate 包括 back/forward/refresh/goto 4 个基础功能。Puppeteer 基于 CDP 的 `Page.getNavigationHistory` 和 `Page.navigateToHistoryEntry` 做了良好封装，可直接使用。

![[Pasted image 20260323215345.png]]

> [!note] 注意
> 输入框的联想记录无法通过 CDP 获取。
>
> ![[Pasted image 20260323215403.png]]

### 扩展程序（浏览器插件）

- **必要性**：中 | **支持度**：直接支持

可以在初始化 Browser 时通过 Puppeteer API 直接注入插件。比如 ad-block 可以屏蔽广告 DOM，让网页更干净，方便模型定位。

### 内部设置页

- **必要性**：中 | **支持度**：直接支持

`chrome://` 协议开头的页面（如 `chrome://history/`、`chrome://downloads/`）都是以网页为载体的，CDP 可以捕获。只要知道 URI 就可以直接 navigate 过去。

| History Page                         | History Page Screenshot              |
| ------------------------------------ | ------------------------------------ |
| ![[Pasted image 20260323215429.png]] | ![[Pasted image 20260323215440.png]] |

### 设置菜单 & 其它 App 级功能

- **支持度**：不支持

CDP 无法感知设置菜单，但其导航到的都是 `chrome://` 协议页面，可以直接 navigate。

其他 App 级功能（Google 账号登录弹窗、标签页分组、阅读模式等）属于甜品功能，AI 场景中越简单越健壮，无需支持。

---

## 二、快捷键

- **必要性**：高 | **支持度**：间接支持

### 跨平台问题

Windows/Linux 的常用快捷键比较统一，但 macOS 使用 Command（`Meta`）而非 Ctrl。当 LLM 发出快捷键 action 指令时，需要先判断 OS 再做适配：

```javascript
hotkey("ctrl+A") --> isMacOS? --- true ---> keyboard('Meta+KeyA')
                         └------- false --> keyboard('Control+KeyA')
```

还有更多差异需要适配，比如：
- 查看历史记录：macOS `Command+Y`，Windows/Linux `Ctrl+H`
- 退出浏览器：macOS `Command+Q`，Windows/Linux `Alt+F` → `X`
- 导航到上个页面：macOS `Command+[`，Windows/Linux `Alt+LeftArrow`

> [!tip] 建议
> 只提供基础适配，遇到具体问题再修，否则是个无底洞。

### CDP 下的 macOS 特殊问题

CDP 发送的键盘指令并非真正的系统键盘指令，作用域限制在 Chrome 和 Page 内部。在 macOS 上直接发送 `Meta+KeyA` 不会执行全选操作（这个 bug 从 2017 年至今仍存在）。
具体原因比较复杂，可以参考 [#776](https://github.com/puppeteer/puppeteer/issues/776) 和 [#1313](https://github.com/puppeteer/puppeteer/issues/1313)，核心原因如下：

> The first bug here is that we **don't** send nativeKeyCodes, so no real OSX events get made. When sending the nativeKeyCodes, "a" is keyCode 0 and protocol decides not to send a falsey keyCode. After these are fixed, OSX **doesn't** like to perform keyboard shortcuts unless the application has the foreground. And lastly, if Chromium has the foreground, we send the nativeKeyCode, and protocol processes it, the shortcut gets captured by the address bar **instead of** the page.
> 
> [https://github.com/puppeteer/puppeteer/issues/776#issuecomment-329589760](https://github.com/puppeteer/puppeteer/issues/776#issuecomment-329589760)



曲线救国方案：使用 `Input.dispatchKeyEvent` 的 `commands` 参数：

```javascript
await page.keyboard.down("KeyA", { commands: ["SelectAll"] });
await page.keyboard.up("KeyA"); // macOS 下生效
```

常见编辑类快捷键的 CDP commands 映射：

| 操作 | macOS | Windows/Linux | CDP commands |
| --- | --- | --- | --- |
| 复制 | Command + C | Ctrl + C | Copy |
| 粘贴 | Command + V | Ctrl + V | Paste |
| 剪切 | Command + X | Ctrl + X | Cut |
| 撤销 | Command + Z | Ctrl + Z | Undo |
| 恢复 | Shift + Command + Z | Ctrl + Y | Redo |
| 全选 | Command + A | Ctrl + A | SelectAll |

其他高权限快捷键可以做**功能映射**：
- 查看历史记录 → `Page.goto('chrome://history/')`
- 退出浏览器 → `Browser.close()`
- 导航到上个页面 → `Page.goBack()`

---

## 三、网页功能

### 截图

- **必要性**：高 | **支持度**：直接支持

CDP 的 `Page.captureScreenshot` 只能截到网页本身（绿框内容），外部 Chrome UI 截不到（红框内容）。

![[Pasted image 20260323215935.png]]

> [!warning] 注意
> 部分 VLM 模型训练时使用完整 Chrome 截图。直接用 CDP 截图传给 VLM，可能导致 action 坐标错位。

### 基础交互

- **必要性**：高 | **支持度**：间接支持

Click、drag、keyboard 等行为，Puppeteer 提供了原子方法可直接组合使用，并支持各种 DOM 回调执行 action 操作。

### Dialog 弹窗

- **必要性**：高 | **支持度**：间接支持

CDP 可以感知 4 类弹窗（Alert、Confirm、Prompt、Beforeunload），弹窗唤起后会中断网页所有行为，必须响应关闭才能继续。

| Alert                                | Confirm                              |
| ------------------------------------ | ------------------------------------ |
| ![[Pasted image 20260323220000.png]] | ![[Pasted image 20260323220007.png]] |

| Prompt                               | Beforeunload                         |
| ------------------------------------ | ------------------------------------ |
| ![[Pasted image 20260323220017.png]] | ![[Pasted image 20260323220029.png]] |

### 右键菜单

- **必要性**：低 | **支持度**：间接支持

CDP 无法感知系统级右键菜单，但菜单内的功能基本可通过其他方式实现。网页内**自定义右键菜单**（DOM 绘制的）可以被 CDP 截图捕获：

### Input 选择器

- **必要性**：高 | **支持度**：间接支持

HTML 大部分表单功能都支持，但使用系统控件的选择器（Select、Date、Time、Color）无法被 CDP 截图捕获：


> [!tip] 迂回方案
> 可以通过 JS 注入替换系统控件为 DOM 控件，间接实现截图需求。
>


### 文件上传/下载

- **必要性**：高 | **支持度**：直接支持

上传：使用 `uploadFile` API 和 `FileChooser` 类。下载：通过 CDP 的 `Browser.setDownloadBehavior`、`Browser.downloadProgress`、`Browser.downloadWillBegin` 和 `Browser.cancelDownload` 组合实现。

> [!warning] 注意
> 文件下载时需注意下载目录的权限问题。

### 打印

- **必要性**：中 | **支持度**：直接支持

`Page.pdf()` 可直接调用。

### 其它 Page 级功能

- **支持度**：不支持

书签、翻译、搜索、二维码等甜品功能在 Browser-Use 场景基本用不到，CDP 也不支持。

---

## 总结

CDP 有明显的能力边界，但已足够支持 **95% 的业务功能**。最重要的是把相关功能打磨好，才能最大程度放大 AI 的能力。

| 分类 | 功能 | 必要性 | 支持度 |
| --- | --- | --- | --- |
| 浏览器 | Tabs 管理 | 高 | 间接支持 |
| 浏览器 | Navigate 导航 | 高 | 直接支持 |
| 浏览器 | 扩展程序 | 中 | 直接支持 |
| 浏览器 | 内部设置页 | 中 | 直接支持 |
| 浏览器 | 设置菜单 | 低 | 不支持 |
| 快捷键 | 编辑类快捷键 | 高 | 间接支持（commands） |
| 快捷键 | 功能类快捷键 | 中 | 功能映射 |
| 网页 | 截图 | 高 | 直接支持 |
| 网页 | 基础交互 | 高 | 间接支持 |
| 网页 | Dialog 弹窗 | 高 | 间接支持 |
| 网页 | Input 选择器 | 高 | 间接支持 |
| 网页 | 文件上传/下载 | 高 | 直接支持 |
| 网页 | 打印 | 中 | 直接支持 |
| 网页 | 右键菜单 | 低 | 间接支持 |
| 网页 | 书签/翻译等 | 低 | 不支持 |
