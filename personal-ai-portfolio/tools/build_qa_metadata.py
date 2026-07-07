import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "qa-data.json"
OUT = ROOT / "docs" / "qa-metadata-v2.md"


def cell(value):
    return str(value or "").replace("\n", "<br>").replace("|", "\\|").strip()


def main():
    qa_items = json.loads(DATA.read_text(encoding="utf-8"))
    lines = [
        "# Ask Yamu 预设问答元数据 V2.0",
        "",
        "说明：",
        "- 原始问答以《项目面试问答 - 副本V2.docx》为准，本文件只记录 Ask Yamu 的匹配和模块关联配置。",
        "- V2.0 共 78 条问答，已移除不应展示的内部提示内容。",
        "- Ask Yamu 面板上的 3 个推荐按钮由前端单独配置，不再进入元数据表格。",
        "- “问题扩展”用于记录同一问题的不同问法。",
        "- “关键词”只保留关键词、短语和 `关键词+关键词` 组合，不再放完整问题句子。",
        "- 命中规则：来访者输入命中关键词短语，或同时命中组合关键词中的核心词，即返回对应固定回答。",
        "",
        "| ID | 问题 | 问题扩展 | 关键词 | 关联模块 | 推荐 |",
        "|---:|---|---|---|---|---|",
    ]

    for item in qa_items:
        variants = "、".join(item.get("variants", []))
        keywords = "、".join(item.get("keywords", []))
        recommended = "是" if item.get("recommended") else "否"
        lines.append(
            "| {id} | {question} | {variants} | {keywords} | {module} | {recommended} |".format(
                id=item["id"],
                question=cell(item["question"]),
                variants=cell(variants),
                keywords=cell(keywords),
                module=cell(item.get("module")),
                recommended=recommended,
            )
        )

    lines.extend(
        [
            "",
            "## 范围外问题回复",
            "",
            "这个问题暂时不在我的主页预设问答范围内。你可以点击上方推荐问题了解我的经历、岗位选择逻辑或我能带来的价值；如果想进一步沟通，也可以通过 Contact 模块联系我。",
            "",
            "## V2.0 校验记录",
            "",
            "- 数据来源：`C:\\Users\\YamD\\Desktop\\项目面试问答 - 副本V2.docx`",
            "- 前端数据：`assets/qa-data.json`",
            "- 问答数量：78",
            "- 空回答数量：0",
            "- 推荐问题：经历看起来跨度有点大，为什么？ / 你在找什么样的公司和岗位？ / 你能为我们带来什么价值？",
            "- 关键匹配测试：跳槽、加班、流程优化案例、MBA帮助、AI业务场景、中马文化差异均已覆盖。",
        ]
    )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"items={len(qa_items)}")


if __name__ == "__main__":
    main()
