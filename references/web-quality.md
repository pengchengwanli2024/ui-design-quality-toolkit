# Web 实现与质量补充

用于现有项目的前端设计、改版与质量优化；它补充 Oil UI Pro 的视觉和体验判断。先读与本次变化相关的部分，不为小改动启动整站审计。

## 从设计决定走到实现

1. 沿用项目组件、设计变量和用户已确认的界面方向。查看目标浏览器/WebView、现有构建与检查命令、受影响路由和关键状态；未知的支持范围保持为未知，不按本机 Chrome 推断。
2. 按任务所需能力使用官方 `modern-web-guidance` 的 `search` / `retrieve`。按返回的真实 ID 检索，编译后的兼容性文字优先于源码里的宏。源码的 demo、expectations 用于理解实现和拟定检查点，不表示应用已通过验收。
3. 在页面中保留现有契约，再选择原生实现或渐进增强。新 API 的适用条件是满足目标浏览器和实际交互需求；已工作的组件不因“更新”而自动替换。核对框架版本、SSR、样式作用域和多实例 ID；按当前类型约定处理新属性，不为一个 API 放宽全局类型或构建目标。
4. 根据改动运行项目已有的 lint、类型检查、相关测试和必要构建；这些检查覆盖代码质量，Lighthouse 不能替代。实际查看目标视口并操作受影响流程；性能相关变化再按 `$lighthouse` 取得可比较的报告。

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

动效与颜色继续按 Oil UI Pro 和项目设计系统决定，并验证减少动态效果偏好、焦点和对比度。技术方案支持产品任务，不自动增加动画、卡片或依赖。

## 测量与验收

- 先确认实际页面、登录态、数据量、构建方式及适用设备。审计跳回登录页时，只能报告登录页的结果。
- 冷启动页面使用 Lighthouse navigation；已展开菜单、校验错误等状态可用 snapshot；SPA 过渡和交互期间的执行、布局偏移使用 timespan。后两者的可用指标与 navigation 不同，不补造缺失分数。
- 只有性能优化需要量化结论时，才在同一机器空闲状态下串行重复前后测量并看中位数/范围；不在同机并行跑 Lighthouse。目标和性能预算沿用项目约定，不把任意总分当作完成条件。
- 检查 Lighthouse 的运行错误、警告和失败 audit，修复拥有这些资源/元素的源代码，再按相同条件复测。用本仓库的 `scripts/summarize.py` 提取报告；它只核对已记录的设置，登录态和数据一致性仍需实际验证。
- LCP、CLS、TBT 等实验室结果与真实用户的 Core Web Vitals 分开表述；TBT 不能替代 INP。自动无障碍审计之外仍操作键盘、焦点、错误恢复和必要的辅助技术；分数不能证明 WCAG AA 或视觉质量。
- 交付只汇报本次改动、实际检查与证据、未验证项。只读审查不改代码；没有目标项目时不宣称项目质量已提升。

## 来源与更新边界

2026-11-17 核验：发行仓库 HEAD `64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65`；源码 HEAD `268fb9ea69b6bc172611ded2026957826ec5b9ec`；Lighthouse HEAD `546477ab94351299d5570f91ec0bb045a7e5aa31`。核验环境的官方插件为 1.0.1，Lighthouse CLI 为 13.6.0；这些是历史参考记录，后续执行应读取实际安装版本。

- [发行技能与按需检索](https://github.com/GoogleChrome/modern-web-guidance/tree/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65/skills/modern-web-guidance)
- [源码：响应式布局](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/css/responsive-design/guide.md)、[响应式表格](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/ui-atoms/responsive-table/guide.md)
- [源码：对话框](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/ui-components/dialog/guide.md)、[表单校验反馈](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/forms/validate-input-after-interaction/guide.md)
- [源码：图片优先级](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/performance/optimize-image-priority/guide.md)、[屏外渲染](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/performance/defer-rendering-heavy-content/guide.md)、[主线程长任务](https://github.com/GoogleChrome/modern-web-guidance-src/blob/268fb9ea69b6bc172611ded2026957826ec5b9ec/guides/performance/break-up-long-tasks/guide.md)
- [Lighthouse：测量波动](https://github.com/GoogleChrome/lighthouse/blob/546477ab94351299d5570f91ec0bb045a7e5aa31/docs/variability.md)、[页面与用户流程的审计模式](https://github.com/GoogleChrome/lighthouse/blob/546477ab94351299d5570f91ec0bb045a7e5aa31/docs/user-flows.md)

本文件是独立整合参考。上游技能和工具更新后应重新检查接口、入口与兼容性信息；本文不表示上游已包含本仓库的集成。
