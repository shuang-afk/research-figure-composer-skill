# Example Gallery

Use these saved SVG examples during the mandatory intake round. Show 3-6 relevant examples as Markdown links or image previews, then ask the user to choose the type, style, and any required content before generating the final figure.

## Saved Examples

| Type | Use for | Example |
|---|---|---|
| Bar chart | grouped bars, model comparison, ablation metrics | `assets/examples/bar.svg` |
| Trend line | time series, dose response, clinical follow-up | `assets/examples/line.svg` |
| Heatmap | omics matrix, feature by cohort, expression patterns | `assets/examples/heatmap.svg` |
| Mechanism diagram | pathway, biological mechanism, material mechanism | `assets/examples/mechanism.svg` |
| Workflow diagram | protocol, research workflow, method pipeline | `assets/examples/workflow.svg` |
| Model architecture | neural network, multimodal model, system architecture | `assets/examples/model-architecture.svg` |
| Data palette comparison | choose palettes for line/bar/scatter/heatmap figures | `assets/examples/palette-data.svg` |
| Diagram palette comparison | choose palettes for mechanism/workflow/architecture figures | `assets/examples/palette-diagram.svg` |

## Intake Message Template

Keep the intake to one round. Do not generate the final figure until the user answers, unless the user explicitly says to skip confirmation.

```text
你想生成哪一类图？我可以按下面这些样式做，最终都输出可编辑 SVG：

1. 柱状图 / 数据对比图 - 示例: assets/examples/bar.svg
2. 趋势图 / 时间序列图 - 示例: assets/examples/line.svg
3. 热图 / 组学矩阵图 - 示例: assets/examples/heatmap.svg
4. 机制图 - 示例: assets/examples/mechanism.svg
5. 流程图 / 方法路线图 - 示例: assets/examples/workflow.svg
6. 模型架构图 - 示例: assets/examples/model-architecture.svg

色系不要只用文字问，必须同时展示：
- 数据图色系对比: assets/examples/palette-data.svg
- 示意图色系对比: assets/examples/palette-diagram.svg

请告诉我：图类型、中文/英文、想选哪张色系示例里的哪一格、要表达的核心结论、是否有数据或节点内容。
```

## Recommended Defaults

- Unknown type: show all six examples and ask the intake question.
- Data comparison: recommend `bar.svg` with `nmi-pastel` or `semantic`.
- Clinical/time series: recommend `line.svg` with `clinical`.
- Mechanism/material: recommend `mechanism.svg` with `material`.
- Workflow: recommend `workflow.svg` with Nature line-art styling.
- Architecture: recommend `model-architecture.svg` with `nmi-pastel`.
- Palette choice must be visual: for data charts, show `palette-data.svg`; for diagrams, show `palette-diagram.svg`; for mixed requests, show both.
