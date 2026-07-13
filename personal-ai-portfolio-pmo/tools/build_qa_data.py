import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCX = Path(r"C:\Users\YamD\Desktop\项目面试问答 - 副本V2.docx")
OUT = ROOT / "assets" / "qa-data.json"
SOURCE_OUT = ROOT / "docs" / "qa-source-extracted.txt"

RECOMMENDED_QUESTIONS = {
    "找什么样的公司和岗位": "你在找什么样的公司和岗位？",
    "你的优势是什么": "你的优势是什么？",
    "带来什么价值": "你能为我们带来什么？",
}

REPLACEMENT_ANSWERS = {
    "你的海外项目和跨文化经验能带来什么价值？": (
        "我能带来的价值，首先是把复杂、分散、涉及多方协作的工作，整理成可推进、可跟踪、可复盘的项目机制。\n\n"
        "在 PMO 和流程优化场景中，我可以支持项目拆解、节点推进、风险识别、会议与行动项跟踪、SOP 梳理、流程复盘，以及管理信息的结构化输出，帮助团队减少信息断层和执行偏差。\n\n"
        "同时，我具备 MBA 商业分析训练和 AI 工具化实践，能够把调研资料、项目文档和业务问题整理成更清晰的判断依据，并在会议纪要、资料对比、风险清单、知识沉淀和工作流自动化等环节引入 AI，提高信息处理和协作效率。\n\n"
        "海外项目与跨文化背景则是我的加分项，尤其适合涉及跨部门、跨地区或出海业务的协作场景。我的定位不是替代业务负责人做决策，而是帮助团队把目标、流程、信息和协作机制连接起来，让项目更稳地推进。"
    ),
}

MODULE_RULES = [
    ("Timeline", ("经历", "稳定", "上一份", "离职", "MBA", "跳槽", "职业规划", "多久")),
    ("Thinking Model", ("思考", "结构化", "SOP", "流程", "AI", "跨文化", "总部", "海外团队", "目标岗位")),
    ("Capabilities", ("优点", "缺点", "优势", "短板", "技能", "管理方式", "工作观", "团队观")),
    ("Cases", ("项目", "案例", "Skill", "AI 实战", "流程优化", "主导")),
    ("Writing", ("公众号", "书籍", "业余爱好")),
    ("Contact", ("薪资", "公司和岗位", "录用", "加班", "上级", "同事", "团队")),
]

QUESTION_PREFIXES = (
    "请你",
    "请在",
    "讲一个",
    "陈述",
    "说说",
    "谈谈",
    "为什么",
    "你对",
    "你能",
    "你会",
    "你有",
    "你最",
    "你的",
    "能举",
)

ANSWER_SKIP_PREFIXES = (
    "建议回答",
    "推荐回答",
    "回答举例",
    "考察点",
    "Tips",
    "固定回答：",
)

KEYWORD_LINE_PATTERN = re.compile(r"^[（(]\s*关键词\s*[:：]\s*(.*?)\s*[）)]\s*$")

CONNECTOR_PATTERN = re.compile(
    r"对于|关于|我们|你们|自己|什么样|为什么|是不是|有没有|会不会|能不能|"
    r"和|与|及|或|对|在|给|为|的|了|吗|呢|是|有|能|可以|怎么|如何|什么|哪些|"
    r"一个|一下|请|你|谈谈|说说|讲讲|陈述|认为|觉得|看待|看法"
)

STOPWORDS = {
    "",
    "问题",
    "回答",
    "你",
    "我",
    "工作",
    "公司",
    "岗位",
    "事情",
    "方面",
    "比较",
    "后续",
    "现在",
    "目前",
    "这个",
    "那个",
    "简单",
    "点大",
}

DOMAIN_TERMS = (
    "AI",
    "非AI",
    "MBA",
    "SOP",
    "HR",
    "PMO",
    "中文",
    "英文",
    "自我介绍",
    "介绍",
    "背景",
    "思考",
    "Temu",
    "POD",
    "出海",
    "出海业务",
    "业务",
    "岗位",
    "公司",
    "价值",
    "贡献",
    "经历",
    "跨度",
    "稳定",
    "稳定性",
    "离职",
    "在职",
    "换工作",
    "上一份工作",
    "空窗",
    "职业规划",
    "海外",
    "海外项目",
    "跨文化",
    "跨文化协作",
    "马来西亚",
    "中国",
    "中马",
    "文化差异",
    "企业文化",
    "结构化",
    "信息结构化",
    "判断",
    "案例",
    "项目",
    "流程优化",
    "流程",
    "支持",
    "SOP",
    "知识档案",
    "加班",
    "看法",
    "观点",
    "压力",
    "业绩压力",
    "销售",
    "薪资",
    "工资",
    "团队",
    "管理",
    "领导",
    "上级",
    "同事",
    "老板",
    "优势",
    "短板",
    "缺点",
    "优点",
    "技能",
    "公众号",
    "书籍",
    "成功",
    "失败",
    "猎头",
    "外贸",
    "招聘",
    "候选人",
    "合规",
    "风险",
    "跳槽",
    "学历",
    "能力",
    "录用",
    "入职",
    "不适合",
)

def extract_docx_blocks(path):
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    blocks = []
    for child in root.find("w:body", ns):
        tag = child.tag.split("}")[-1]
        if tag == "p":
            text = "".join(t.text or "" for t in child.findall(".//w:t", ns)).strip()
            if text:
                blocks.append(text)
        elif tag == "tbl":
            for tr in child.findall(".//w:tr", ns):
                cells = [
                    "".join(t.text or "" for t in tc.findall(".//w:t", ns)).strip()
                    for tc in tr.findall("./w:tc", ns)
                ]
                if any(cells):
                    blocks.append(" | ".join(cells))
    return blocks


def clean_question_label(text):
    text = re.sub(r"^[一二三四五六七八九十\d]+[、.]\s*", "", text).strip()
    return text


def is_question(text):
    value = text.strip()
    if not value or len(value) > 190:
        return False
    if value.startswith(("比如", "具体项目", "横向补充", "第一", "第二", "第三", "第四", "最终")):
        return False
    if any(value.startswith(prefix) for prefix in QUESTION_PREFIXES):
        return True
    if "？" in value or "?" in value:
        return True
    return False


def split_question_variants(question):
    text = clean_question_label(question)
    pieces = re.split(r"\s*/\s*|？|\?", text)
    variants = [piece.strip(" /") for piece in pieces if piece.strip(" /")]
    return dedupe(variants)


def keyword_line(text):
    match = KEYWORD_LINE_PATTERN.match(text.strip())
    return match.group(1).strip() if match else ""


def normalize(text):
    return re.sub(r"[\s，。！？、；：,.!?;:\-_/（）()“”\"'‘’【】\[\]]+", "", str(text or "").lower())


DOMAIN_TERM_KEYS = {normalize(term) for term in DOMAIN_TERMS}


def dedupe(items):
    seen = set()
    result = []
    for item in items:
        key = normalize(item)
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def split_terms(value):
    parts = re.split(r"[、,，;；]+", str(value or ""))
    return dedupe([part.strip() for part in parts if part.strip()])


def split_core_terms(text):
    chunks = re.split(r"[\s+/，。！？、；：,.!?;:\-_/（）()“”\"'‘’【】\[\]]+", str(text or ""))
    parts = []
    for chunk in chunks:
        parts.extend(CONNECTOR_PATTERN.split(chunk))
    result = []
    for part in parts:
        token = normalize(part)
        if token in STOPWORDS:
            continue
        if len(token) >= 3 or token in DOMAIN_TERM_KEYS:
            result.append(part.strip())
    return dedupe(result)


def phrase(*parts):
    return "+".join(part for part in parts if part)


def add_pair_keywords(keywords, terms):
    priority = [
        "AI",
        "MBA",
        "SOP",
        "出海",
        "业务",
        "岗位",
        "公司",
        "价值",
        "经历",
        "跨度",
        "稳定性",
        "离职",
        "跳槽",
        "海外",
        "跨文化",
        "马来西亚",
        "中国",
        "文化差异",
        "结构化",
        "信息结构化",
        "判断",
        "案例",
        "项目",
        "流程优化",
        "流程",
        "加班",
        "薪资",
        "团队",
        "领导",
        "同事",
        "压力",
        "猎头",
        "外贸",
        "合规",
        "风险",
    ]
    present = [term for term in priority if normalize(term) in {normalize(t) for t in terms}]
    for idx, first in enumerate(present):
        for second in present[idx + 1 :]:
            keywords.append(phrase(first, second))


def question_keywords(question):
    variants = split_question_variants(question)
    keywords = []
    all_text = " ".join([question, *variants])
    normalized_all = normalize(all_text)
    is_non_ai_question = "非ai" in normalized_all

    for term in DOMAIN_TERMS:
        if term == "AI" and is_non_ai_question:
            continue
        if normalize(term) in normalized_all:
            keywords.append(term)

    for variant in variants:
        keywords.extend(split_core_terms(variant))

    if is_non_ai_question:
        keywords = [keyword for keyword in keywords if normalize(keyword) != "ai"]

    add_pair_keywords(keywords, keywords)

    if "自我介绍" in normalized_all:
        keywords.extend(["自我介绍", "个人介绍", "背景"])
        if "中文" in normalized_all:
            keywords.extend(["中文+自我介绍", "中文介绍"])
        if "英文" in normalized_all:
            keywords.extend(["英文+自我介绍", "英文介绍", "English intro"])
    if "离职" in normalized_all or "换工作" in normalized_all or "上一份工作" in normalized_all:
        keywords.extend(["在职", "离职", "上一份工作", "换工作", "为什么离职"])
    if "经历" in normalized_all and ("跨度" in normalized_all or "稳定" in normalized_all):
        keywords.extend(["经历+跨度", "职业跨度", "稳定性", "经历不线性", "为什么跨度大"])
    if "公司" in normalized_all and "岗位" in normalized_all:
        keywords.extend(["公司+岗位", "找公司", "找岗位", "岗位选择", "择业标准", "选择公司标准"])
    if "价值" in normalized_all:
        keywords.extend(["价值", "能带来什么", "创造价值", "为什么选你", "贡献"])
    if "跳槽" in normalized_all:
        keywords.extend(["跳槽", "跳槽+看法", "跳槽+怎么看", "如何看待跳槽", "职业调整"])
    if "加班" in normalized_all:
        keywords.extend(["加班", "加班+看法", "加班+怎么看", "加班+观点"])
    if "流程优化" in normalized_all and "案例" in normalized_all:
        keywords.extend(["流程优化", "流程优化+案例", "流程优化支持+案例", "流程优化+项目"])
    if "mba" in normalized_all and ("帮助" in normalized_all or "有什么用" in normalized_all or "结构化" in normalized_all):
        keywords.extend(["MBA", "MBA+帮助", "MBA+有什么用", "MBA后+项目", "结构化+案例", "结构化+项目", "结构化+判断", "信息结构化+案例"])
    if "ai" in normalized_all and "业务" in normalized_all:
        keywords.extend(["AI+业务", "AI+业务场景", "AI+出海业务", "AI+业务价值"])
    if is_non_ai_question:
        keywords.extend(["非AI", "非AI+项目", "非AI+经验", "非AI+项目经验", "非AI项目"])
    elif "ai" in normalized_all and ("案例" in normalized_all or "实战" in normalized_all):
        keywords.extend(["AI+案例", "AI+实战案例", "AI项目", "AI案例"])
    if "马来西亚" in normalized_all and "中国" in normalized_all:
        keywords.extend(["中马文化差异", "马来西亚+中国", "马来西亚+文化差异", "企业文化差异"])
    if "薪资" in normalized_all:
        keywords.extend(["薪资", "期望薪资", "工资", "薪酬"])
    if "书籍" in normalized_all:
        keywords.extend(["书籍", "喜欢的书", "读书", "书单"])

    return dedupe(keywords)


def module_for(question):
    for module, terms in MODULE_RULES:
        if any(term in question for term in terms):
            return module
    return "About"


def recommended_for(question):
    return any(key in question for key in RECOMMENDED_QUESTIONS)


def clean_answer(lines):
    cleaned = []
    for line in lines:
        text = line.strip()
        if not text:
            continue
        if keyword_line(text):
            continue
        skip_line = False
        for prefix in ANSWER_SKIP_PREFIXES:
            if text.startswith(prefix):
                text = text[len(prefix) :].strip(" ：:")
                if not text:
                    skip_line = True
                break
        if skip_line:
            continue
        cleaned.append(text)
    return "\n\n".join(cleaned).strip()


def main():
    blocks = extract_docx_blocks(DOCX)
    SOURCE_OUT.write_text("\n".join(blocks), encoding="utf-8")

    positions = [idx for idx, block in enumerate(blocks) if is_question(block)]
    data = []
    for order, start in enumerate(positions, start=1):
        question = clean_question_label(blocks[start])
        end = positions[order] if order < len(positions) else len(blocks)
        answer_lines = blocks[start + 1 : end]
        supplied_keywords = []
        for line in answer_lines:
            value = keyword_line(line)
            if value:
                supplied_keywords.extend(split_terms(value))
        answer = REPLACEMENT_ANSWERS.get(question, clean_answer(answer_lines))
        variants = split_question_variants(question)
        if "带来什么价值" in question:
            variants.append("你能为我们带来什么")
            variants = dedupe(variants)
        data.append(
            {
                "id": order,
                "question": question,
                "variants": variants,
                "keywords": dedupe(supplied_keywords) or question_keywords(question),
                "module": module_for(question),
                "recommended": recommended_for(question),
                "answer": answer,
            }
        )

    missing = [item["id"] for item in data if not item["answer"]]
    recommended = [item["question"] for item in data if item["recommended"]]
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"source={DOCX}")
    print(f"wrote {OUT}")
    print(f"items={len(data)} missing_answers={missing}")
    print(f"recommended={recommended}")


if __name__ == "__main__":
    main()
