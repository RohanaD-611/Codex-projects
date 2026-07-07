import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "qa-data.json"
OUT = ROOT / "app.js"


def main():
    qa_items = json.loads(DATA.read_text(encoding="utf-8"))
    app = f"""const qaItems = {json.dumps(qa_items, ensure_ascii=False, indent=2)};

const recommendedLabels = {{
  3: "经历看起来跨度有点大，为什么？",
  5: "你在找什么样的公司和岗位？",
  46: "你能为我们带来什么价值？",
}};

const fallbackAnswer = "这个问题暂时无法由 DeepSeek API 回答，也没有命中本地预设问答。你可以换一种更具体的问法，或通过 Contact 模块联系我。";

const chatToggle = document.querySelector("#chatToggle");
const chatPanel = document.querySelector("#chatPanel");
const chatClose = document.querySelector("#chatClose");
const chatQuestions = document.querySelector("#chatQuestions");
const chatAnswer = document.querySelector("#chatAnswer");
const chatForm = document.querySelector("#chatForm");
const chatInput = document.querySelector("#chatInput");

const apiChatEndpoint = window.location.protocol === "file:" ? "http://localhost:8787/api/chat" : "/api/chat";
const chatHistory = [];

const connectorPattern = /对于|关于|我们|你们|自己|什么样|为什么|是不是|有没有|会不会|能不能|和|与|及|或|对|在|给|为|的|了|吗|呢|是|有|能|可以|怎么|如何|什么|哪些|一个|一下|请|你|谈谈|说说|讲讲|陈述|认为|觉得|看待|看法/g;

const strongSingleKeywords = new Set([
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
]);

const weakSingleKeywords = new Set([
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
]);

function normalizeText(value) {{
  return String(value || "")
    .toLowerCase()
    .replace(/[\\s，。！？、；：,.!?;:\\-_/（）()“”"'‘’【】\\[\\]]/g, "");
}}

function keywordParts(value) {{
  return String(value || "")
    .toLowerCase()
    .split(/[\\s+，。！？、；：,.!?;:\\-_/（）()“”"'‘’【】\\[\\]]+/)
    .flatMap((part) => part.split(connectorPattern))
    .map((part) => normalizeText(part))
    .filter((part) => part.length >= 2);
}}

function setPanelOpen(isOpen) {{
  chatPanel.classList.toggle("open", isOpen);
  chatToggle.setAttribute("aria-expanded", String(isOpen));
  if (isOpen) {{
    window.setTimeout(() => chatInput?.focus(), 60);
  }}
}}

function setAnswer(text) {{
  chatAnswer.textContent = text;
}}

function cleanAnswerText(text) {{
  return String(text || "")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/__([^_]+)__/g, "$1")
    .replace(/^\s{0,3}#{1,6}\s+/gm, "")
    .replace(/^\s*[-*]\s+/gm, "")
    .replace(/`([^`]+)`/g, "$1")
    .trim();
}}

function renderAnswer(item, sourceButton) {{
  document
    .querySelectorAll(".chat-questions button")
    .forEach((node) => node.classList.toggle("active", node === sourceButton));
  setAnswer(item.answer || fallbackAnswer);
}}

function scorePhrase(normalizedQuery, normalizedPhrase) {{
  if (!normalizedPhrase) return 0;
  if (normalizedQuery === normalizedPhrase) return 12;
  if (normalizedPhrase.includes(normalizedQuery) && normalizedQuery.length >= 4) return 8;
  if (normalizedQuery.includes(normalizedPhrase) && normalizedPhrase.length >= 4) return 6;
  return 0;
}}

function isPartMatched(normalizedQuery, queryParts, part) {{
  return normalizedQuery.includes(part) || queryParts.some((queryPart) => part.includes(queryPart));
}}

function scoreKeyword(normalizedQuery, queryParts, keyword) {{
  const normalizedKeyword = normalizeText(keyword);
  let score = scorePhrase(normalizedQuery, normalizedKeyword);
  const parts = keywordParts(keyword);

  if (parts.length >= 2) {{
    const matchedCount = parts.filter((part) => isPartMatched(normalizedQuery, queryParts, part)).length;
    if (matchedCount === parts.length) {{
      score += 12 + parts.length;
    }} else if (matchedCount >= 2) {{
      score += 5 + matchedCount * 2;
    }}
  }} else if (parts.length === 1) {{
    const part = parts[0];
    if (
      isPartMatched(normalizedQuery, queryParts, part) &&
      !weakSingleKeywords.has(part) &&
      (part.length >= 3 || strongSingleKeywords.has(part))
    ) {{
      score += strongSingleKeywords.has(part) ? 10 : 7;
    }}
  }}

  return score;
}}

function keywordMatched(normalizedQuery, queryParts, keyword) {{
  const normalizedKeyword = normalizeText(keyword);
  const parts = keywordParts(keyword);
  if (scorePhrase(normalizedQuery, normalizedKeyword) > 0) return true;
  if (parts.length >= 2) {{
    return parts.filter((part) => isPartMatched(normalizedQuery, queryParts, part)).length >= 2;
  }}
  if (parts.length === 1) {{
    return isPartMatched(normalizedQuery, queryParts, parts[0]);
  }}
  return false;
}}

function findAnswer(query) {{
  const normalizedQuery = normalizeText(query);
  if (!normalizedQuery || normalizedQuery.length < 2) return null;
  const queryParts = keywordParts(query);

  let bestMatch = null;
  let bestScore = 0;

  qaItems.forEach((item) => {{
    let score = 0;

    [item.question, ...(item.variants || [])].forEach((phrase) => {{
      score += scorePhrase(normalizedQuery, normalizeText(phrase));
    }});

    let matchedKeywordCount = 0;
    (item.keywords || []).forEach((keyword) => {{
      score += scoreKeyword(normalizedQuery, queryParts, keyword);
      if (keywordMatched(normalizedQuery, queryParts, keyword)) {{
        matchedKeywordCount += 1;
      }}
    }});
    if (matchedKeywordCount >= 2) {{
      score += 8 + matchedKeywordCount;
    }}

    if (score > bestScore) {{
      bestScore = score;
      bestMatch = item;
    }}
  }});

  return bestScore >= 6 ? bestMatch : null;
}}

async function askDeepSeek(query) {{
  const response = await fetch(apiChatEndpoint, {{
    method: "POST",
    headers: {{
      "Content-Type": "application/json",
    }},
    body: JSON.stringify({{
      message: query,
      history: chatHistory.slice(-6),
    }}),
  }});

  const payload = await response.json().catch(() => ({{}}));
  if (!response.ok || !payload.answer) {{
    throw new Error(payload.error || "DeepSeek API request failed");
  }}
  return cleanAnswerText(payload.answer);
}}

qaItems
  .filter((item) => item.recommended)
  .forEach((item) => {{
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = recommendedLabels[item.id] || item.question;
    button.addEventListener("click", () => renderAnswer(item, button));
    chatQuestions.append(button);
  }});

chatForm.addEventListener("submit", async (event) => {{
  event.preventDefault();
  const query = chatInput.value.trim();
  if (!query) return;

  document
    .querySelectorAll(".chat-questions button")
    .forEach((node) => node.classList.remove("active"));

  chatInput.value = "";
  chatInput.disabled = true;
  setAnswer("正在调用 DeepSeek 生成回答...");

  try {{
    const answer = await askDeepSeek(query);
    chatHistory.push({{ role: "user", content: query }});
    chatHistory.push({{ role: "assistant", content: answer }});
    setAnswer(answer);
  }} catch (error) {{
    const match = findAnswer(query);
    setAnswer(match ? match.answer : fallbackAnswer);
  }} finally {{
    chatInput.disabled = false;
    chatInput.focus();
  }}
}});

chatToggle.addEventListener("click", () => {{
  setPanelOpen(!chatPanel.classList.contains("open"));
}});

chatClose.addEventListener("click", () => {{
  setPanelOpen(false);
}});

document.addEventListener("keydown", (event) => {{
  if (event.key === "Escape") {{
    setPanelOpen(false);
  }}
}});
"""
    OUT.write_text(app, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
