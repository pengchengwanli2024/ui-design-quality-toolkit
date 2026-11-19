# Web 实现与质量补充

本文件提供 Web 技术判断、检索入口与 Lighthouse 使用细节。调用顺序和检查范围由 [SKILL.md](../SKILL.md#canonical-sequence) 统一决定；读到本文件时继续当前阶段，不重开一套设计、实施和验收流程。

## 技术资料使用

- 使用目标浏览器/WebView 的实际支持范围，未知时不按本机 Chrome 推断。原生实现和渐进增强都需保留项目契约与必要回退，不能为了 API 更新自动替换已工作的组件。
- 按需使用官方 `modern-web-guidance` 的 `search` / `retrieve`，基于返回的真实 ID 读取指南；在本轮相关客户端改动前完成查询。未变化能力可复用本任务已取回的同版本资料；出现新问题再查对应指南。
- 编译后的兼容性文字优先于源码里的宏；源码 demo/expectations 是参考条件，不是应用验收结果。核对框架版本、SSR、样式作用域和多实例 ID，按现有类型约定处理新属性，不为单个 API 放宽全局类型或构建目标。

## 按问题检索并验证

以下 ID 已在核验的上游源码中定位。以后使用时仍先检查已安装官方技能，再检索当前指南；不要把下表当作永不过期的兼容性数据库。

| 观察到的问题 | 相关 guide ID / 检索词 | 应落实的判断与检查 |
| --- | --- | --- |
| 组件放入侧栏后挤压、手机浏览器工具栏遮挡 | `responsive-design`；`responsive component layout` | 按容器宽度还是视口宽度变化选择查询方式；对需要随工具栏变化的区域考虑动态视口单位，并保留目标浏览器需要的回退。验证中文换行、缩放和真实可用高度。 |
| 表格窄屏不可读或无法滚动 | `responsive-table`；`responsive data table` | 保留表头与单元格关系；按数据比较任务选择滚动或重排。滚动容器具备可访问名称和键盘路径，固定表头不遮内容；不能用缩小字号掩盖溢出。 |
| 弹窗关闭后丢焦点、脏表单误关闭、提示框层级错乱 | `dialog`、`declarative-dialog-popover-control` | 先区分阻断式对话框、非模态面板与菜单/提示；适用时用原生机制，避免重复添加焦点陷阱。验证 Esc、可见关闭入口、返回焦点及未保存确认；对 `closedby` 的支持不足保留 `cancel` 保护。 |
| 未输入就全表报错、错误只靠颜色表示 | `validate-input-after-interaction` | 按已确认的业务校验展示错误；可用时采用 `:user-invalid`，保留旧浏览器和项目校验路径。错误文本与字段关联，`aria-invalid` 反映当前状态；客户端反馈不能替代服务端校验。 |
| 首屏大图加载慢、图片引发布局跳动 | `optimize-image-priority` | 先确认 LCP 候选。首屏关键图不懒加载，仅少量关键资源提升优先级；普通屏外图按需懒加载，预留尺寸或比例，复查真实网络与 LCP 资源。 |
| 长页面或复杂列表布局绘制昂贵 | `defer-rendering-heavy-content` | `content-visibility: auto` 只用于确认在初始视口外的独立重块，并配估计尺寸 `contain-intrinsic-size`。核验滚动跳动、查找和跨屏键盘可达性；需要可发现的隐藏内容不能随意改成 `content-visibility: hidden`。 |
| 点击后长时间无反馈、大循环阻塞主线程 | `break-up-long-tasks`、`schedule-tasks-by-priority` | 先用 trace 找到阻塞。分块让出主线程与任务优先级是不同问题；使用 `scheduler.yield()` / `postTask()` 时分别检测支持并保留回退。Promise 微任务拆分本身不保证给浏览器绘制机会。 |

## Lighthouse

是否测量以及基线/复测的时机见 [统一顺序](../SKILL.md#canonical-sequence)。如果已选择外部 Lighthouse 审计技能或项目已有审计工具，沿用它的当前测量阶段、配置和报告；不要额外运行下面示例形成第二套审计。

没有现成审计流程时，可使用独立安装的官方 Lighthouse CLI 和兼容 Chrome。以下为移动端 navigation 基线示例，替换实际 URL 和任务输出路径，在修改产品前运行：

```sh
mkdir -p ./reports
lighthouse 'http://localhost:3000/' --chrome-flags='--headless' --output=html --output=json --output-path='./reports/before' --enable-error-reporting=false
```

修复已体现在运行页面后，使用相同 URL、设备和配置另存复测报告，不覆盖基线：

```sh
lighthouse 'http://localhost:3000/' --chrome-flags='--headless' --output=html --output=json --output-path='./reports/after' --enable-error-reporting=false
```

桌面基线和复测都加 `--preset=desktop`。认证页面需授权登录态；独立 Chrome 进程不会继承活动浏览器会话。确认实际最终 URL、数据量、版本、构建、缓存策略和机器/网络负载；跳回登录页只能说明登录页结果。

### 模式和比较

- navigation 用于页面加载；snapshot 用于已展开菜单、错误态等当前 DOM；timespan 用于 SPA 过渡和交互期间的执行、布局偏移。后两者不提供全部 navigation 指标或总体性能分，不补造分数。
- 量化性能改善需在同条件下串行重复测量并看中位数/范围，不在同机并行跑 Lighthouse。项目已有预算优先，不把任意总分当作完成条件。
- 在工具包或已安装技能目录中，用实际报告的绝对路径解析；此脚本读取单个 LHR，不运行浏览器，不接受整份 user-flow 容器（需先选取其中一步的 LHR）：

```sh
python3 scripts/summarize.py /absolute/path/after.report.json --compare /absolute/path/before.report.json
```

`valid` 只表示报告执行有效，`partial` 暴露单项 audit 错误；退出 1 表示 Lighthouse 运行失败，退出 2 表示输入无效。脚本严格比较完整 `configSettings` 和部分页面/环境信息；设置不同时不生成差值，未知值、未知或不一致单位在 `skipped_metric_deltas` 中给出原因。`settings_match` 不证明相同登录态、数据、构建、实际缓存或稳定改善；警告、最终 URL 和比较条件仍需核验。

将运行错误、失败 audit 和受影响资源/元素返回当前实现与验证阶段；报告分数差值不等于问题已解决。LCP、CLS、TBT 等实验室结果与真实用户 Core Web Vitals 分开表述，TBT 不能替代 INP，自动无障碍分数也不证明完整 WCAG 合规或视觉质量。

## 来源与更新边界

2026-11-17 核验：发行仓库 HEAD `64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65`；源码 HEAD `268fb9ea69b6bc172611ded2026957826ec5b9ec`；Lighthouse HEAD `546477ab94351299d5570f91ec0bb045a7e5aa31`。核验环境的官方插件为 1.0.1，Lighthouse CLI 为 13.6.0；这些是历史参考记录，后续执行应读取实际安装版本。

- [发行技能与按需检索](https://github.com/GoogleChrome/modern-web-guidance/tree/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance)
- [源码：响应式布局](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/css/responsive-design/guide.md)、[响应式表格](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/ui-atoms/responsive-table/guide.md)
- [源码：对话框](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/ui-components/dialog/guide.md)、[表单校验反馈](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/forms/validate-input-after-interaction/guide.md)
- [源码：图片优先级](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/performance/optimize-image-priority/guide.md)、[屏外渲染](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/performance/defer-rendering-heavy-content/guide.md)、[主线程长任务](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/performance/break-up-long-tasks/guide.md)
- [Lighthouse：测量波动](https://github.com/GoogleChrome/lighthouse/blob/546477ab94351299d5570f91ec0bb045a7e5aa31/docs/variability.md)、[页面与用户流程的审计模式](https://github.com/GoogleChrome/lighthouse/blob/546477ab94351299d5570f91ec0bb045a7e5aa31/docs/user-flows.md)

本文件是独立整合参考。上游技能和工具更新后应重新检查接口、入口与兼容性信息；本文不表示上游已包含本仓库的集成。
