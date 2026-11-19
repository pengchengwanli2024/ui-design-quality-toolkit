# UI Design Quality Toolkit

把界面设计、项目设计规范、现代 Web 实现与真实验证连接起来的 AI 编程技能和本地工具。

适合新页面、已有项目 UI 改版，以及需要同时关注交互、兼容性、性能和无障碍的前端优化。可以搭配用户独立安装的 Oil UI Pro；本仓库提供原创整合流程与报告工具。

## 包含内容

- `SKILL.md`：按任务范围组合设计、实现与验证流程。
- `references/design-md-library.md`：从 awesome-design-md 等参考中提炼项目规则，记录适用页面与证据缺口。
- `references/web-quality.md`：现代浏览器能力、兼容性、响应式、表单、图片和主线程问题的检索与验证入口。
- `references/unslop-refinement.md`：从 unslop 改编的去模板化诊断与分层精修方法，覆盖间距、色彩、图标、文案、字体、布局、组件细节、素材和动效。
- `assets/DESIGN.template.md`：项目设计规范的最小模板。
- `scripts/summarize.py`：本地解析 Lighthouse JSON，保留不可用分数，识别错误，检查比较条件与指标单位。
- `tests/`：报告工具的回归测试。

## 使用

让技能安装器从本仓库根目录安装，技能名为 `ui-design-quality`。Codex 用户也可以运行：

```sh
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo pengchengwanli2024/ui-design-quality-toolkit --path . --name ui-design-quality
```

安装 Oil UI Pro 时，请使用其作者提供的独立授权和安装流程。

## 与其他设计技能的边界

本仓库的 `ui-design-quality` 技能与
[app-ui-studio](https://github.com/pengchengwanli2024/app-ui-studio) 覆盖面高度重叠：
设计规范适配、Modern Web 质量检查、Lighthouse 报告对比在 app-ui-studio 内都有对应实现
（`references/design-system.md`、`references/modern-web.md`、`studio.py web-report --baseline`）。

因此**同一个宿主里只装一个**：

- 已经在用 app-ui-studio（Codex 或 Hermes）→ 不要再装本技能，否则两者抢同一触发词。
- 只想做轻量质量审计、不需要整套设计生产流程 → 只用本技能即可。

可以这样描述任务：

```text
用 ui-design-quality 配合已安装的 Oil UI Pro，检查并优化这个项目的 UI。
沿用项目品牌、现有组件和已确认方向，按问题选择设计参考与现代 Web 指南。
完成相关代码检查、实际交互和目标视口验证；性能相关改动保留前后审计证据。
```

用户提到“去 AI 味”“去模板感”或需要视觉精修时，会按需使用 unslop 整合参考：先记录具体问题，再按产品任务和既有规范修整。已确认的品牌、业务内容与功能状态继续作为约束；这条路径与上面的设计和质量流程共用入口。

只有设计文档分析时，不需要浏览器或 Lighthouse。正式界面的视觉与交互验证需要可运行页面和实际浏览器；真实审计还需用户自行安装 Lighthouse 与 Chrome。

## 报告解析

需要 Python 3.10 或以上，不安装第三方 Python 包，不联网，也不上传报告。

```sh
python3 scripts/summarize.py /absolute/path/after.report.json
python3 scripts/summarize.py /absolute/path/after.report.json --compare /absolute/path/before.report.json
```

`settings_match` 严格核对报告中记录的完整 `configSettings` 及页面、版本和模式信息；变动字段只显示名称，不输出额外请求头的值。登录状态、数据、构建和实际缓存状态仍需确认；有效报告和分数差值不表示问题已经修复。单位未知或不一致时不计算该指标差值。

运行测试：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

## 长期默认

可以在自己的全局或项目指令中加入：

> 界面设计和项目 UI 优化默认将 ui-design-quality 与已安装的 Oil UI Pro 结合使用，按任务影响面选用设计参考、Modern Web Guidance、项目代码检查与 Lighthouse 验证；保留现有品牌和已确认方向。

## 来源与许可

本仓库的原创整合文档、模板和代码使用 MIT 许可。[unslop 精修改编文档](references/unslop-refinement.md) 单独采用 CC BY 4.0，保留 Damir Sokolovsky（@heydamir）署名、原仓库链接和改编说明；许可全文见 [LICENSES/CC-BY-4.0.txt](LICENSES/CC-BY-4.0.txt)。方法来源和各项目关系见 [NOTICE.md](NOTICE.md)。

这是独立社区整合，不代表 Oil UI Pro、Google Chrome、VoltAgent 或任何参考品牌的官方产品。依赖工具和付费技能由用户按各自条件另行安装。
