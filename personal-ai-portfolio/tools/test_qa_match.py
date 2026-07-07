import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "qa-data.json"

CONNECTOR_PATTERN = re.compile(
    r"对于|关于|我们|你们|自己|什么样|为什么|是不是|有没有|会不会|能不能|"
    r"和|与|及|或|对|在|给|为|的|了|吗|呢|是|有|能|可以|怎么|如何|什么|哪些|"
    r"一个|一下|请|你|谈谈|说说|讲讲|陈述|认为|觉得|看待|看法"
)

STRONG_SINGLE_KEYWORDS = {
    "ai",
    "mba",
    "sop",
    "pmo",
    "跳槽",
    "加班",
    "薪资",
    "书籍",
    "公众号",
    "离职",
    "稳定性",
    "跨文化",
    "流程优化",
    "信息结构化",
    "文化差异",
    "合规",
    "招聘",
    "猎头",
    "外贸",
    "学历",
    "薪酬",
    "工资",
    "优点",
    "缺点",
    "优势",
    "短板",
    "贡献",
}

WEAK_SINGLE_KEYWORDS = {
    "项目",
    "案例",
    "业务",
    "岗位",
    "公司",
    "工作",
    "团队",
    "管理",
    "价值",
    "流程",
    "支持",
    "看法",
    "观点",
}


def normalize(value):
    return re.sub(r"[\s，。！？、；：,.!?;:\-_/（）()“”\"'‘’【】\[\]]+", "", str(value or "").lower())


def keyword_parts(value):
    chunks = re.split(r"[\s+，。！？、；：,.!?;:\-_/（）()“”\"'‘’【】\[\]]+", str(value or "").lower())
    parts = []
    for chunk in chunks:
        parts.extend(CONNECTOR_PATTERN.split(chunk))
    return [normalize(part) for part in parts if len(normalize(part)) >= 2]


def score_phrase(query, phrase):
    query = normalize(query)
    phrase = normalize(phrase)
    if not phrase:
        return 0
    if query == phrase:
        return 12
    if query in phrase and len(query) >= 4:
        return 8
    if phrase in query and len(phrase) >= 4:
        return 6
    return 0


def is_part_matched(normalized_query, query_parts, part):
    return part in normalized_query or any(part.find(query_part) >= 0 for query_part in query_parts)


def score_keyword(query, keyword):
    normalized_query = normalize(query)
    query_parts = keyword_parts(query)
    normalized_keyword = normalize(keyword)
    score = score_phrase(query, normalized_keyword)
    parts = keyword_parts(keyword)

    if len(parts) >= 2:
        matched_count = sum(1 for part in parts if is_part_matched(normalized_query, query_parts, part))
        if matched_count == len(parts):
            score += 12 + len(parts)
        elif matched_count >= 2:
            score += 5 + matched_count * 2
    elif len(parts) == 1:
        part = parts[0]
        if (
            is_part_matched(normalized_query, query_parts, part)
            and part not in WEAK_SINGLE_KEYWORDS
            and (len(part) >= 3 or part in STRONG_SINGLE_KEYWORDS)
        ):
            score += 10 if part in STRONG_SINGLE_KEYWORDS else 7

    return score


def keyword_matched(query, keyword):
    normalized_query = normalize(query)
    query_parts = keyword_parts(query)
    normalized_keyword = normalize(keyword)
    parts = keyword_parts(keyword)
    if score_phrase(query, normalized_keyword) > 0:
        return True
    if len(parts) >= 2:
        return sum(1 for part in parts if is_part_matched(normalized_query, query_parts, part)) >= 2
    if len(parts) == 1:
        return is_part_matched(normalized_query, query_parts, parts[0])
    return False


def find_answer(data, query):
    best_match = None
    best_score = 0
    for item in data:
        score = 0
        for phrase in [item["question"], *item.get("variants", [])]:
            score += score_phrase(query, phrase)
        matched_keyword_count = 0
        for keyword in item.get("keywords", []):
            score += score_keyword(query, keyword)
            if keyword_matched(query, keyword):
                matched_keyword_count += 1
        if matched_keyword_count >= 2:
            score += 8 + matched_keyword_count
        if score > best_score:
            best_score = score
            best_match = item
    return (best_match, best_score) if best_score >= 6 else (None, best_score)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    print(f"count={len(data)}")
    print("recommended=" + " | ".join(item["question"] for item in data if item["recommended"]))

    queries = [
        "你对跳槽怎么看",
        "对于流程优化，你有什么案例？",
        "你对于加班是什么看法？",
        "AI 在业务场景中可以怎么使用？",
        "mba有什么帮助",
        "mba 帮助",
        "mba 有什么用",
        "mba后 项目",
        "结构化 案例",
        "结构化 项目",
        "中马文化差异",
        "你最喜欢的书籍",
        "你的优点",
        "你的优点是什么",
        "别人是怎么评价你的？",
        "经历看起来跨度有点大，为什么？",
        "你在找什么样的公司和岗位？",
        "你能为我们带来什么价值？",
    ]

    for query in queries:
        match, score = find_answer(data, query)
        question = match["question"] if match else "NO_MATCH"
        print(f"{query} => {question} ({score})")


if __name__ == "__main__":
    main()
