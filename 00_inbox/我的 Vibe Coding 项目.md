---
type: "inbox"
status: "pending"
source: "web-clipper"
url: "https://x.com/idoubicc/status/2040821048577565144"
created: 2026-04-07
---
最近三个月，我用 Claude Code Vibe Coding 了几个项目，非常有意思，写篇文章记录一下。

## WorkAny

[workany.ai](https://workany.ai/)

在上一篇文章 [Vibe Coding 一周，我做了个桌面 Agent](https://idoubi.ai/blog/vibe-coding-workany) 写到，我第一次尝试全自动 Vibe Coding，发布了我的第一个 Agent 项目 WorkAny。

断断续续在迭代 WorkAny，修复了一些用户反馈的问题，Github 仓库 star 涨到了 1.4k。

![Image](https://pbs.twimg.com/media/HFJx4s8b0AAAGJV?format=jpg&name=large)

WorkAny 最初的版本基于 Claude Agent SDK 实现 Agent Runtime，依赖本地的 Claude Code，任务处理比较慢，还经常遇到一些模型不兼容的问题。

最近一段时间尝试了接入 DeepAgents、Pi 作为 Claude Agent SDK 的替代方案，效果始终不太理想，需要定制的工具很多，不能做到像 Claude Agent SDK 一样开箱即用。

这周把 WorkAny 的 Agent Runtime 换成了自己写的 Open Agent SDK，运行流畅了，好多问题也解决了。

## WorkAny Bot

[workany.bot](https://workany.bot/)

2 月份的时候，OpenClaw 特别火，掀起了全民养虾热潮，主要的需求和痛点是：

- 大家都在玩，很好奇，我也想试试
- 不敢在自己电脑跑，担心隐私和安全风险
- 不懂技术，搞不了虚拟机，折腾不来云服务器
- 希望长时间待机，但没预算，不想买 Mac Mini
- 不想学怎么配模型、Skills，只想开箱即用

我花了一个周末的时间，发布了 WorkAny Bot，提供 OpenClaw 云端托管服务。

用户不需要关心技术，只需要点几下 \`Next\`，付费开通服务，马上得到一个 \`[xxx.workany.bot](https://xxx.workany.bot/)\` 地址，打开就能看到 OpenClaw 的页面，接入到自己的 im 软件，开始养虾。

![Image](https://pbs.twimg.com/media/HFJyAZmaYAE2bwp?format=jpg&name=large)

WorkAny Bot 给不想自己折腾的用户提供了便利，让部分人快速用上了 OpenClaw。但在使用过程中，体验还是比不上在自己电脑上部署 OpenClaw。

云端的 Bot 在浏览器自动化、配置工具、定时任务等方面有很多限制，使用起来不够流畅。

## ClawHost

[clawhost.me](https://clawhost.me/)

我把 WorkAny Bot 背后的 OpenClaw 托管方案整理出来开源了。

这套方案的核心依赖 K8S 集群，在每个 Pod 部署一个 OpenClaw 实例，通过 PVC 挂载磁盘，对 .openclaw 目录进行持久化存储。

![Image](https://pbs.twimg.com/media/HFJyFH4bwAAbsza?format=jpg&name=large)

ClawHost 提供一个简单的管理面板，管理员创建 App 和 Bot，对外提供 Restful API，第三方 App 通过 API 创建 Bot 和管理 Bot 内配置。

![Image](https://pbs.twimg.com/media/HFJyHj6bEAANROc?format=jpg&name=large)

熟悉 K8S 运维的人可以使用这个方案，做自己的 OpenClaw 托管服务。企业可以私有化部署，挂载内部 Skills，为员工统一配置企业版龙虾。

## ChatClaw

[chatclaw.im](https://chatclaw.im/)

我觉得 OpenClaw 自带的 Web UI 有点丑。

功能很多，配置很杂，改起来很麻烦。而且对话的体验很不好。

![Image](https://pbs.twimg.com/media/HFJyKLnaMAAzihy?format=jpg&name=large)

于是我开源了 ChatClaw，一个基于 OpenClaw 的 Web UI，提供更美观的界面和更流畅的对话体验，主打多 Agent 协同对话/工作。

最近 OPC（一人公司） 很火，ChatClaw 从 OPC 的角度设计了整体架构：

OPC -> Companies -> Teams -> Agents -> Tasks

一个 OPC 可以创建多个公司，每个公司对应一个 OpenClaw Gateway，可以是本地的，也可以是云端的（比如：WorkAny Bot）。

![Image](https://pbs.twimg.com/media/HFJyMcLb0AA169k?format=jpg&name=large)

ChatClaw 的本质是一个 Web UI，只做界面交互，不做业务逻辑。依赖的是 OpenClaw 提供的 Agent Runtime，相当于给你的龙虾换个壳子。前提是，你得有自己的 OpenClaw。

## CoRich

1 月份的时候，我想做一个开源版本的桌面 Agent，对标 Cowork。

想了好几个产品名，其中一个是 CoRich，另一个是 WorkAny，后来选了 WorkAny 作为产品名，CoRich 这个名字就闲置了。

最近 Slack 被爆出批量删除中国团队账户，不允许中国公司使用了。

然后我就很想做个 Agent 版本的 Slack，让人与 AI 可以协同工作，共同完成任务。

我选择了 CoRich 做这个产品的名字，让 Claude Code 快速搭了一个架子，布局参考 Slack，允许创建多个 Workspace，邀请人类员工、创建 Agent 员工，在不同的 Channel 下对话或做任务。

这个产品的交互跟 ChatClaw 有点像，不同的点在于 ChatClaw 是基于 OpenClaw 的 Web UI，依赖 OpenClaw 作为 Agent Runtime，主要是给个人使用，不适合多人协作。

CoRich 跟 ChatClaw 的架构类似，把 Companies 换成了 Workspaces，同样支持 Agents、Teams、Tasks，区别在于 CoRich 允许邀请人类员工加入 Workspace，支持多人 + 多 Agent 协作。

![Image](https://pbs.twimg.com/media/HFJyQRXacAA0pIl?format=jpg&name=large)

目前，CoRich 还属于 Demo 阶段，还需要点时间完善基本功能。

## FastClaw

[fastclaw.ai](https://fastclaw.ai/)

我做了近两个月的 OpenClaw 托管服务，部署在阿里云国际站的 K8S 集群上，一个月接近 5k 美金的部署成本。

我分析了一下，部署成本高的原因主要有几点：

- OpenClaw 是单租户架构，我需要为每个用户单独用一个 Pod 隔离部署，挂载独立的存储空间
- OpenClaw 需要至少 1G 的运行内存，在 K8S 部署，每个 Pod 的 memory\_limit 不能低于 4G，不然很容易 OOM
- OpenClaw 针对一些复杂类任务（比如：写代码），会开独立的子进程去执行，进程开销很大。
- OpenClaw 启动依赖网关初始化、插件加载等多个串行步骤，从启动到可用需要 15-30 秒，没办法做到秒级启动。如果要保证用户云端的 Bot 一直在线，Pod 需要常驻，对于不经常使用的 Bot，是一种资源浪费

所以我得出的结论是，OpenClaw 是针对个人使用场景设计的助理类 Agent，不适合云端部署的多租户场景。上面提到的 CoRich 这种需要多人协作的产品，用 OpenClaw 做底层的 Agent Runtime 肯定不行。

于是我决定自己做一个 Agent 底层框架（操作系统）。

我开源了 FastClaw，定位是一个更好的 OpenClaw-Like Agent OS。

- 使用 Go 实现，单二进制分发（5MB），运行零依赖，秒级启动
- 运行时内存占用 ~20M，约为 OpenClaw 内存占用的 1/7
- 约 3000 行代码实现 OpenClaw 的核心功能，二次开发更简单
- 以 RPC 进程通信的方式运行插件，隔离风险，插件挂了不影响主进程，解决 OpenClaw Gateway 容易挂的问题
- 引入数据库实现持久化存储，用户会话隔离，天然适用云原生多租户部署场景
- 可视化引导安装，上手门槛更低。管理后台 Web UI 更清晰、操作更友好

![Image](https://pbs.twimg.com/media/HFJyUlFa4AA8CaK?format=jpg&name=large)

除了架构方面的优化和对云端多租户场景的适配，FastClaw 选择尽可能兼容 OpenClaw 的协议和生态：

- fastclaw.json 配置文件，采用跟 openclaw.json 一样的数据结构
- 支持 OpenClaw 的 plugins，支持 ClawHub 的 skills 等
- 跟 OpenClaw 类似的方式实现 memory、context、tools 等核心功能

目前的情况是，FastClaw 堆了很多功能，但是还没来得及完整测试。

有来自社区的开发者贡献了几个 FastClaw 插件，还没来得及整合，还需要时间打磨功能、发展生态。

## WeClaw

[weclaw.im](https://weclaw.im/)

半个月前，一向封闭的微信开放了 ClawBot 一级入口，允许用户接入自己的 OpenClaw，在微信 ClawBot 对话使用。

微信官方发布了一个 weixin-openclaw 插件，用户在电脑上运行这个插件，扫码登录后，可以连接电脑上的 OpenClaw。

我的工作电脑上没有安装 OpenClaw，但是我想通过微信 ClawBot 连接我电脑上的 Claude Code 做任务。

于是我开源了 WeClaw，定位是连接微信 ClawBot 与桌面 Agent 的桥接器。

在电脑上运行 weclaw 后，weclaw 自动探测到电脑上安装的 Agent，比如 Claude Code / Codex / Gemini / OpenClaw 等，再通过 ACP / CLI / HTTP 三种方式，与 Agent 实现连接。

用户可以在微信 ClawBot 通过自定义指令切换 Agent 对话，可以把消息同时发给多个 Agent。

![Image](https://pbs.twimg.com/media/HFJyYQdbUAA2_vD?format=jpg&name=large)

有个高频使用 weclaw 的朋友给我看了他的一个工作流，挺有意思的：

在微信 ClawBot 语音输入内容 -> 微信自动转文字 -> 发给电脑上的 weclaw -> weclaw 转发给电脑上的 Claude Code -> Claude Code 根据输入内容，提取关键信息 -> Claude Code 调用 Skills，把结构化内容输出到第三方软件

![Image](https://pbs.twimg.com/media/HFJyaDhasAAN-NU?format=jpg&name=large)

WeClaw 这个项目的价值在于，你可以在微信 ClawBot 连接任何你常用的 Agent，定制指令实现自定义工作流。

## AnyClaw

[anyclaw.tools](https://anyclaw.tools/)

有了 WeClaw 之后，我日常会通过微信 ClawBot 查很多信息，做很多任务。

只靠大模型的能力，很多任务实际上是不太容易完成的。

为了补充大模型挂载外部信息的能力，这两年出来了很多解决方案，比如 RAG / MCP / Skills 等。

Skills 的解决方案是写一堆 Markdown 文档加一些脚本，让 Agent 渐进式读取提示词，在合适的时机调用合适的技能，辅助大模型完成任务。

Skills 比起 MCP 是一个很大的创新，不需要把一堆工具在每次对话都塞进模型上下文，节约了 Token。

后面大家发现，用命令行工具，可以进一步优化上下文，因为命令行工具 --help 输出的信息，能告知模型可用的工具列表，还不需要传递额外的描述内容。

于是，很多厂商又从开放 Skills 转成了开放 CLI 工具。

我开源了 AnyClaw，定位是给 Agent 用的技能补充包。

这个项目主要想做三件事：

- 做转换器。把互联网上的 OpenAPI Schema / 自定义的脚本、Pipeline / 网站 / 桌面 App 等，一键转换成 CLI 工具
- 做扩展坞。输入是 CLI，输出是 MCP / Skills，让不同类型的 Agent 都能理解工具，在合适的时机自动发现并调用工具
- 做工具箱。把常用的工具收集起来，放到工具箱，让 Agent 可以搜索、安装、调用工具

比如我针对域名搜索场景写了个 \`query-domains\` 工具，通过 anyclaw 命令三步调用：

> anyclaw search domain anyclaw install query-domains anyclaw query-domains search "[workany.ai](https://workany.ai/)"

![Image](https://pbs.twimg.com/media/HFJygUsbMAAutH-?format=jpg&name=large)

除了 anyclaw 内置的工具，你还可以添加第三方仓库提供的工具，比如：

> anyclaw repo add [https://github.com/larksuite/cli](https://github.com/larksuite/cli) --name feishu-cli anyclaw repo update anyclaw search docs --repo feishu-cli

把 AnyClaw 自身的 SKILL.md 发给 Claude Code，然后就可以通过 WeClaw 给 Claude Code 发消息，调用 AnyClaw 内置的工具查信息了。

![Image](https://pbs.twimg.com/media/HFJykbBboAA632I?format=jpg&name=large)

AnyClaw 目前对于工具的编写、转换、导入等功能已经比较完整了。工具箱内置的工具还比较少，还需要时间积累，也需要发展生态，通过社区的力量集成更多的工具。

## ClawRouter

我去年做过一段时间 MCPRouter，把一些流行的 MCP 服务器托管起来，整合下游服务的 API Key，再对上游提供统一的接入和计费。

用了一段时间 OpenClaw 之后，我发现要让自己的龙虾做更多的事情，比如画图、生成音乐等，需要给龙虾配置各种工具，但是我又不想去各个提供工具的服务商平台申请 API Key 和绑卡充值。

于是我把 MCPRouter 改成了 ClawRouter，把之前托管的 MCP 服务器平移了过来，后面还想接入模型、Skills，以及 AnyClaw 整合的 CLI 工具。

ClawRouter 的定位是 Tools 版本的 OpenRouter。

![Image](https://pbs.twimg.com/media/HFJymvzagAEFXsW?format=jpg&name=large)

目前 ClawRouter 整合的工具还不够多，还在内部测试，没有发布上线。

## Clawork

玩过一段时间 MoltBook，Agent 自由社交，非常前沿。有人觉得 Web 4.0 要来了，Agent 互联网已开启。

于是我在想，既然 Agent 能自由社交，Agent 是不是也可以自由交易。

我给我的 Agent 配置了最贵的模型和最好的工具，我的 Agent 能够高效完成各类复杂的任务，但是我的成本消耗也很大。

如果我的 Agent 可以在网上接单，帮助其他人实现他们的一些需求，是不是既创造了价值，又能赚到钱，帮助我平摊成本。

于是我做了 Clawork，定位是 Agent 众包平台。可以由人类，或者人类的 Agent 在平台上发布任务，设置预算。

其他人的 Agent 可以通过接口发现任务，竞标做任务，完成任务后可以获得对应的 Token 报酬。

人类在平台提现，把 Agent 赚到的 Token 换成现金提取出来。

Clawork 可以先做成 Agent 版本的 Upwork，走竞标模式。后面可以往 Agent 版本的 Uber 方向发展，做平台派单模式。

有交易的平台，就会有很大的商业价值。我很看好这个方向，但是又感觉有点太超前，不太容易落地。

![Image](https://pbs.twimg.com/media/HFJyp9JaEAE2MBv?format=jpg&name=large)

Clawork 初期的核心功能已经完成，本地测试跑通了完整的双边交易流程，但是还有一些问题没有想明白，所以还没有发布上线。

## ClawBaby

最近一段时间看到了很多有意思的桌宠项目，有的跑在 Dock 栏上，有的跑在刘海屏上，还有的在桌面上跑来跑去。

最近 Claude Code 推出了一个 \`/buddy\` 指令，可以在 Claude Code 对话框添加一个桌宠。

我让 Claude Code 给我写了两个版本，一个版本用 tauri 写的，让一个龙虾头像在桌面游走，监听 Agent 在做的任务，做实时互动。另一个版本用 Swift 写的，跑在 Mac 的刘海屏，可以投喂、互动，就像是在玩宠物养成游戏。

![Image](https://pbs.twimg.com/media/HFJysNsaIAAUT0L?format=jpg&name=large)

单纯觉得这类项目好玩，谈不上多有价值，反正也不需要我花什么时间，顺手就让 Claude Code 做了。😄

## Open Agent SDK

本周 AI 行业有个大事件，Claude Code 源码泄露了。

Twitter 上有一波人用 AI 去分析 Claude Code 的源码，再写成解读文章，拿到了很多流量。

另一波人选择在 Claude Code 源码基础上补齐工具链，做成可直接运行的开源版 Claude Code，吸引了很多关注。

我选择了在 Claude Code 源码基础上，抽出来一个 SDK，用于替换 Claude Agent SDK

使用 claude-agent-sdk 做过 Agent 产品的都知道，其本质是在 claude code 的基础上套了一层壳，做成 sdk 给第三方接入，可以加速 Agent 产品的开发，但是弊端也很明显：

- claude-agent-sdk 依赖 claude code，而 claude code 是不开源的，一切都是黑盒调用，出了问题你没法修
- claude-agent-sdk 接到的 query，需要创建 claude code 进程去处理，开销很大，不适合云端规模化调用

我让 Claude Code 分析了一遍 claude-code-sourcemap 源码，把逻辑全部抽离出来，写了个 open-agent-sdk：

- 完全兼容 claude-agent-sdk 的接口形式，只需换个包名即可快速替换
- 完全开源，你可以接入到你的 Agent 后做定制化修改，不再是黑盒调用
- 函数调用，不依赖本地 cli 进程，没有额外的开销，云端 Agent 高并发不愁

使用 open-agent-sdk 的一个调用示例：

```typescript
import { createAgent } from '@codeany/open-agent-sdk';
const agent = createAgent({
  apiType: 'openai-completions',
  model: 'gpt-4o',
  apiKey: 'sk-...',
  baseURL: 'https://api.openai.com/v1',
});
const result = await agent.prompt('What files are in this project?');
console.log(result.text);
```

> 帖子发出去之后，反响特别好，拿到了 321k 访问，Github 仓库一周涨了 2k star，真神奇。

![Image](https://pbs.twimg.com/media/HFJxe_0agAAgh5_?format=jpg&name=large)

我让 Claude Code 参考 open-agent-sdk-typescript，实现了 go / rust / python 三个语言的版本，一共开源了四个语言版本的 open-agent-sdk

然后我又让 Claude Code 修改 WorkAny 的源码，引入 open-agent-sdk-typescipt，替换掉原来依赖的 claude-agent-sdk

在 WorkAny 跑了几个任务，响应很快，效果很好。用自己的 SDK 实现了 Agent Runtime 功能，不再依赖 Claude Code，哪里不爽改哪里。

## CodeAny

[codeany.ai](https://codeany.ai/)

泄露出来的 Claude Code 源码有近 50 万行代码，除了 Agent 运行逻辑，还有很多周边代码值得学习和研究。

我让 Claude Code 继续扫描 claude-code-sourcemap 仓库，把 cli 和 UI 部分的逻辑抽离出来，用 go 重写，做一个新的终端 Agent：CodeAny

在 CodeAny 引入了 open-agent-sdk-go 作为 Agent Runtime

经过多次的扫描、测试、补齐功能，CodeAny 基本复刻了 Claude Code 的核心功能，实现了 Claude Code 的大部分指令。

在 CodeAny 接入 OpenRouter 上的 xiaomi-mimo 模型，响应速度非常快，跑了几个任务，效果还不错。

![Image](https://pbs.twimg.com/media/HFJxarVbIAAuGp0?format=jpg&name=large)

比起 Claude Code，CodeAny 的运行速度更快，内存占用更低，而且完全开源，可以定制功能。继续迭代，也许能逐步替代掉 Claude Code，作为日常使用的 Coding 工具。

## CCOnline

既然拿到了 Claude Code 的源码，我在想，能不能跟托管 OpenClaw 一样，我也搞一个托管 Claude Code 的服务？

于是我做了 CCOnline，定位是一个跑在云端的 Claude Code，内置模型 + Skills，帮助用户完成一些日常的任务。

跟 ClawHost 的托管方案不一样，我尝试用 e2b 来做隔离容器，每个用户分配一个默认的 Workspace，每个 Workspace 对应一个 e2b 容器，用户的项目文件通过对象存储挂载。

比起 K8S Pod 的隔离方案，e2b 隔离性更好，毫秒级启动，无需常驻，运维方便。也许成本会比用 K8S Pod 的方案低。

![Image](https://pbs.twimg.com/media/HFJxTupaEAAhnMW?format=jpg&name=large)

CCOnline 目前还在技术实验阶段，我没想明白纯云端的 Claude Code 有什么价值，目标群体和使用场景分别是什么。

## 总结

用一个表格整理了以上提到的几个项目👇

![Image](https://pbs.twimg.com/media/HFJyzMqaIAEHezn?format=png&name=large)

这些项目全部由 Claude Code 完成，我负责提需求、测试、再提需求，未参与过代码编写工作，总体投入时间不多。

我甚至很少打开编辑器，很多时候是走在路上，灵感来了，拿出手机，通过 Discord 把想法发给 OpenClaw，让 OpenClaw 调用 Claude Code 去实现。

等有时间打开电脑，我再去验收一下，有不满意的地方，再发消息给 OpenClaw 让他指挥 Claude Code 去修改。

全自动 Vibe Coding 近三个月，我有几点很深的感触：

1.我的编程习惯彻底被颠覆了，角色定位也发生了很大的变化。我不再把自己当做一个程序员，而是项目经理 + 系统架构师 + 测试工程师。

2\. AI 治好了我的强迫症和代码洁癖，我不再关注代码，只关注实现的功能完整性。

3\. AI 变得智能了，我的效率更高了，但是注意力更加不集中了。同时开很多个窗口做不同的项目，没有把哪个项目做得特别好

4.测试资源极度缺乏，AI 做得很快，但是我没有足够的时间去验收，也不知道功能完不完整，有没有什么 bug

5.用 AI 复刻一个项目变得极度容易，我不明白这个时代产品的护城河在哪里

6.技术落地的能力差异被 AI 彻底抹平，擅长搞流量和商业变现的能力变得极其重要

7.知识面的广度和架构设计能力，是这个时代重要且稀缺的能力

8.我时常感到迷茫，不知道做这些所谓“产品”的意义在哪里

也许控制注意力，在一个方向持续做深，才是正确的事情。

> Attention is all you need.