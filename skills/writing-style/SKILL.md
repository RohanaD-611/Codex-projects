---
name: writing-style
description: Apply the user's personal Chinese writing style for WeChat Official Account essays, personal essays, opinion pieces, reflective writing, and article editing. Use when the user asks to write, rewrite, polish, continue, title, outline, or edit content in their own voice, especially for 公众号, 个人随笔, 观点表达, 职业观察, AI/职场/商业反思, or when they mention personal writing style.
---

# Writing Style Skill

## Purpose

Use this skill to write or edit in the user's personal essay style. The style is primarily based on Chinese originals. For English writing, transfer the thinking structure, tone, pacing, and restraint, but do not claim to reproduce a native English personal style unless the user later provides English samples.

The target voice is reflective, orderly, concrete, and mildly critical. It should feel like a person thinking through a problem in public: honest about uncertainty, observant about social reality, and unwilling to hide behind trend templates or empty slogans.

## Source Priority

When style rules conflict, follow this order:

1. The user's current explicit request.
2. The rules in this `SKILL.md`.
3. `references/style-profile.md` for detailed style diagnosis.
4. General writing best practices.

Do not preserve awkward wording just because it sounds informal. Keep the user's calm, reflective voice while improving clarity and rhythm.

## Trigger Conditions

Use this skill when the user asks for:

- Writing, rewriting, polishing, expanding, shortening, outlining, titling, or continuing Chinese essays.
- WeChat Official Account articles that should read like personal essays rather than traffic-oriented posts.
- Personal opinion pieces about AI, career planning, work, hiring, business ethics, self-positioning, or social observation.
- "按我的风格写", "用我的写作风格", "像我自己写的", "微信公众号", "个人随笔", "观点表达".

Do not use this skill for:

- Formal resumes, cover letters, interview reports, or job application materials unless the user explicitly asks to add a personal essay tone.
- Purely academic, legal, technical API, or documentation writing that requires a different genre.
- Viral marketing copy, short-video scripts, hard-selling sales pages, or exaggerated growth-hacking formats.

## Core Voice

Write with these qualities:

- Calm introspection: start from a concrete moment, confusion, conversation, video, question, or small observation.
- Ordered thinking: gradually move from personal feeling to a larger pattern, then return to practical judgment.
- Moderate skepticism: point out contradictions in work, business, AI, or social narratives without becoming loud or performative.
- Human-centered judgment: care about people, dignity, trust, energy, meaning, and the real cost of systems.
- Plain but thoughtful wording: avoid ornamental language, but allow a few memorable phrases when they emerge naturally.
- Self-aware uncertainty: allow "我好像", "我突然反应过来", "后来我发现", "这可能", "不一定", "说不定".

The writing should not sound like a consultant report, motivational account, public-intellectual performance, or viral content template.

## Chinese Writing Rules

### 1. Opening

Prefer one of these openings:

- A direct personal state: "快30了，我还在反复问自己..."
- A recent observation or conversation: "最近跟 HR 朋友聊天..."
- A topic plus a concrete reference: "说到 AI 时代的职业规划..."
- A meme, quote, or public phrase, followed by personal interpretation.

Avoid opening with:

- "在当今时代..."
- "随着社会的发展..."
- "你是否也曾..."
- "今天我们来聊聊..."
- Over-polished hooks, suspense bait, or forced pain-point questions.

### 2. Structure

Use a progression like:

1. Concrete entry point.
2. First reaction or confusion.
3. Wider observation.
4. A counterintuitive turn or reframing.
5. Practical implication.
6. A restrained closing image, sentence, or judgment.

For longer articles, use short section headings. Headings should be simple and slightly reflective, such as:

- "另一个被忽略的历史坐标"
- "一个被长期误用的职业逻辑"
- "如何追随人才？"
- "回到 AI 时代"
- "提升自己？"
- "一些代沟"

Do not overuse numbered listicles. Numbers are acceptable when clarifying steps or arguments, but the article should still feel like an essay.

### 3. Paragraph Rhythm

Use many short paragraphs. One idea per paragraph.

Mix:

- Short one-sentence paragraphs for turning points.
- Medium explanatory paragraphs for context.
- Occasional longer paragraphs when building social or historical background.

Use sentence rhythm that alternates between:

- "我以为..."
- "但..."
- "后来..."
- "真正..."
- "比起 A，B 更..."
- "当你 A 时，你把...；当你 B 时，你把..."

### 4. Vocabulary Preferences

Prefer words and phrases in these families:

- 思考与定位：方向、具体方向、聚焦点、个人定位、判断力、方法论、结构、反馈、复盘、调整、最小成本、MVP、真实反馈。
- 情绪与身体反应：迷茫、内耗、空空的、难受、有能量、不舒服、身体反应、幸福感缺失。
- 职业与组织：人才、流动、连接、网络、协作、岗位、组织、公司、团队、上级、工作成果。
- 社会观察：现实情况、代沟、环境、底气、信任、尊重、价值、长期、短期、责任、温度。
- 判断转折：反直觉、真正有用的是、这带来一个提示、我突然反应过来、换一个算法、回到这个问题。

Use "AI" naturally with spaces when near Chinese if needed, such as "AI 跟我说". Keep common English terms like MVP, HR, KPI, CEO, pass when they sound natural in context.

### 5. Sentence Patterns

Use these patterns often:

- "我以为 A，但后来发现 B。"
- "它说的都对，但也不痛不痒。"
- "比起 A，B 显得更..."
- "真正 X 的，不是 A，而是 B。"
- "当你 A 时，你...；当你 B 时，你..."
- "这看起来 A，但如果换一个算法，B。"
- "问题不在于 A，而在于 B。"
- "你不会因为 A 而安全，但你会因为 B 而安全。"

Do not make every sentence symmetrical. Use these as rhythm anchors, not templates.

### 6. Tone Boundaries

Allowed:

- Mild irony.
- Honest self-questioning.
- Direct social criticism.
- Plain emotional words.
- Specific dissatisfaction with workplaces, systems, and empty advice.

Avoid:

- Shouting, scolding, or internet quarrel tone.
- Dense moral judgment without evidence.
- Fake certainty.
- Overly soft "治愈系" comfort.
- Grand slogans.
- Excessive academic abstraction.

### 7. Punctuation

Use Chinese punctuation by default:

- Use Chinese commas, periods, question marks, semicolons, quotation marks.
- Use Chinese quotation marks "..." for most quoted concepts, unless preserving existing title style like 「炸薯条」.
- Use em dash-like separator only for date signatures or a strong final note, such as "—— 2026.6.1".
- Use question marks in headings when the section is genuinely questioning, such as "提升自己？"
- Avoid excessive exclamation marks. Usually use none.
- Avoid emojis.

Keep dates compact when signing off, for example "—— 2026.6.3".

## English Transfer Rules

If the user asks for English writing:

- Keep the same reflective structure: concrete observation, inner reaction, broader pattern, reframing, restrained conclusion.
- Use plain, modern English. Prefer "I used to think...", "What changed was...", "The real issue is not..., but...".
- Avoid marketing language, overconfident thought-leadership tone, and LinkedIn-style inspiration.
- State clearly if the user asks for "my exact English style" that there are no English samples yet, so the result is a transfer of Chinese style rather than a fully learned English voice.

## Prohibited List

Do not use these unless the user explicitly asks for a different style:

- "在这个快节奏的时代"
- "随着 AI 的飞速发展"
- "你是否也有这样的困惑"
- "普通人如何逆袭"
- "干货满满"
- "建议收藏"
- "看完这篇你就懂了"
- "底层逻辑" as a filler phrase
- "赋能", "抓手", "闭环", "颗粒度", "打法", "矩阵" unless quoting workplace jargon critically
- "松弛感", "向内求", "长期主义" as trendy decoration
- Emoji, exaggerated exclamation, clickbait titles, and forced golden sentences.

## Workflow

When writing from scratch:

1. Identify the concrete entry point: personal experience, observation, conversation, video, quote, or question.
2. Define the core tension: what seems true at first, and what the user wants to complicate.
3. Build an essay arc from personal observation to broader judgment.
4. Keep paragraphs short and transitions visible.
5. End with a restrained but memorable thought, not a slogan.

When polishing existing text:

1. Preserve the user's argument and lived details.
2. Remove generic AI phrasing, empty transitions, and inflated wording.
3. Improve paragraph rhythm and sentence clarity.
4. Add concrete contrast or reframing only where it strengthens the user's original point.
5. Do not turn the piece into a listicle unless the user asks.

When generating titles:

- Prefer clear, reflective titles over traffic bait.
- Good title shapes:
  - "关于 X，我看过的最好答案"
  - "找 AI 算命，它说我还没..."
  - "X 困境"
  - "从 X 开始"
- Avoid overpromising, "爆款", and direct fear hooks.

## Output Rules

- Default output language follows the user's request.
- For Chinese essays, produce clean Markdown unless the user asks for another format.
- If the piece is for WeChat Official Account, keep it readable in mobile paragraphs: shorter paragraphs, visible section breaks, no dense blocks.
- Do not explain that you used this skill unless the user asks.
- If the user's topic lacks concrete entry point, ask at most 2 questions or make a conservative assumption and state it briefly.

