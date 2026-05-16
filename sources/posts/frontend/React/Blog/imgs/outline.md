---
type: mixed
density: balanced
style: blueprint
image_count: 3
language: zh-CN
---

## Illustration 1

**Position**: After section "一条数据链路"
**Purpose**: Visualize the core API DTO to Adapter to UI Model boundary, making the data ownership split obvious.
**Visual Content**: A left-to-right technical pipeline: external backend contract enters as API DTO, adapter transforms and guards it, UI Model exits as component-ready data.
**Filename**: 01-framework-dto-adapter-ui-model.png

## Illustration 2

**Position**: After section "以 distribution_area 为例"
**Purpose**: Summarize the three adapter operations from the concrete example: renaming, fallback, and derived calculation.
**Visual Content**: A central adapter workbench with three transformation cards showing `status_desc -> statusDesc`, default values, and `Boolean(goods)`.
**Filename**: 02-infographic-adapter-responsibilities.png

## Illustration 3

**Position**: After section "7. 何时不要这套分层"
**Purpose**: Help readers decide when this layering is useful and when it is over-design.
**Visual Content**: A decision-style comparison showing Good Fit vs Skip Adapter signals from the article.
**Filename**: 03-comparison-when-to-use-adapter.png
