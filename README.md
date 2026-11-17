# UI Design Quality Toolkit

把界面设计、项目设计规范、现代 Web 实现与真实验证连接起来的 AI 编程技能和本地工具。

适合新页面、已有项目 UI 改版，以及需要同时关注交互、兼容性、性能和无障碍的前端优化。可以搭配用户独立安装的 Oil UI Pro；本仓库提供原创整合流程与报告工具。

## 包含内容

- `SKILL.md`：按任务范围组合设计、实现与验证流程。
- `references/design-md-library.md`：从 awesome-design-md 等参考中提炼项目规则，记录适用页面与证据缺口。
- `references/web-quality.md`：现代浏览器能力、兼容性、响应式、表单、图片和主线程问题的检索与验证入口。
- `assets/DESIGN.template.md`：项目设计规范的最小模板。
- `scripts/summarize.py`：本地解析 Lighthouse JSON，保留不可用分数，识别错误，检查比较条件与指标单位。
- `tests/`：报告工具的回归测试。

## 使用

让技能安装器从本仓库根目录安装，技能名为 `ui-design-quality`。Codex 用户也可以运行：

```sh
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo pengchengwanli2024/ui-design-quality-toolkit --path . --name ui-design-quality
```

安装 Oil UI Pro 时，请使用其作者提供的独立授权和安装流程。

可以这样描述任务：

```text
用 ui-design-quality 配合已安装的 Oil UI Pro，检查并优化这个项目的 UI。
沿用项目品牌、现有组件和已确认方向，按问题选择设计参考与现代 Web 指南。
完成相关代码检查、实际交互和目标视口验证；性能相关改动保留前后审计证据。
```

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

本仓库的原创整合文档、模板和代码使用 MIT 许可。方法来源和各项目关系见 [NOTICE.md](NOTICE.md)，具体参考链接在相应文档中。

这是独立社区整合，不代表 Oil UI Pro、Google Chrome、VoltAgent 或任何参考品牌的官方产品。依赖工具和付费技能由用户按各自条件另行安装。
