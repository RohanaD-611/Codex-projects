---
name: writing-style
description: Apply the user's personal Chinese writing style 2.0 for WeChat Official Account essays, personal essays, AI-use diaries, reflective opinion pieces, article rewriting, polishing, continuation, titling, and outlining. Use when the user asks to write in their own voice, revise AI-generated prose to sound like them, reduce AI flavor, make writing more daily and coherent, or write about AI, Codex skills, career planning, work, business ethics, personal positioning, or social observation. Primary language is Chinese; English output should transfer structure and tone only because no English samples exist.
---

# Writing Style Skill 2.0

## Purpose

Use this skill to write or edit in the user's personal essay style. The style is mainly Chinese, suited for WeChat Official Account articles, personal essays, AI-use diaries, reflective notes, and opinion pieces.

The writing should feel like the user is thinking through a real problem in daily life, not presenting a polished report. It should have order, but not be stiff; judgment, but not a lecturing tone; personal texture, but not scattered diary fragments.

具体文章风格详见 `references/reference.md`。Every time this skill is used for writing, rewriting, polishing, or style diagnosis, read `references/reference.md` first and use it as the primary sample reference. Use `references/style-profile.md` only as a secondary diagnosis file.

## Source Priority

When style rules conflict, follow this order:

1. The user's current explicit request and revision feedback.
2. `references/reference.md` primary sample articles.
3. This `SKILL.md`.
4. `references/style-profile.md`.
5. General writing best practices.

Do not overfit to individual sample sentences. Preserve the user's way of thinking, paragraph rhythm, and everyday wording before copying surface phrases.

## Core Voice

Write with these qualities:

- Daily and concrete: begin from a real behavior, confusion, conversation, search path, platform habit, work scene, or recent thought.
- Reflective but readable: let the reader see how the idea gradually becomes clear.
- Ordered but soft: the article should have a clear line of thought, but paragraphs should feel naturally connected instead of stacked like notes.
- Personally honest: allow uncertainty, hesitation, wasted time, trial and error, and later correction.
- Mildly critical: question AI, workplace, career, business, or content templates without turning the piece into a rant.
- Human-centered: care about time, energy, dignity, trust, useful feedback, and whether a tool actually helps a person think.

The voice should not sound like a consultant report, product update, public-intellectual speech, viral post, or AI-generated summary.

## 2.0 Corrections

These rules override earlier habits:

- Do not default to one sentence per paragraph. Write by complete meaning units. A paragraph may contain several connected sentences when they express one thought.
- Use short standalone sentences only for real turns, pauses, or emphasis. Do not use them as the default rhythm.
- Reduce mechanical contrast patterns such as "不是...而是..." and "从...到...". Use them only when they are truly the cleanest expression.
- Avoid vague abstraction such as "它其实还是空的". Replace it with concrete description, for example "它只是一个没有明确线索的头绪", "我还不知道第一步应该从哪里拆", or "它听起来像方向，但还没有落到可执行的步骤里".
- When writing about a process, do not pile up steps. Connect the process to the user's inner reason: why this step appeared, what uncertainty it solved, what changed after it.
- When writing about AI or Codex skills, keep the tool in the background unless the tool itself is the subject. The article should still read like a person's use diary, not a feature manual.

## Openings

Prefer openings with life texture and a problem path. Good openings often start from how the user actually thinks or searches:

- "当我有一个想法需要思考能不能落地的时候，会习惯性去找各种各样的平台聊天、咨询，比如 AI、小红书、知乎，然后自己将所有的信息整合在一起，分析解决方案和步骤是什么。"
- "有时候我甚至搞不清楚自己想要什么，一通乱查后再进行聚焦，等收集到很多信息以后才发现，这个方向可能一开始就不太适合。"
- "今天我突然想到，为什么不用一个想法 skill 辅助我思考呢？"
- "最近我发现，比起让 AI 直接给我答案，我更需要它先帮我把问题问清楚。"

Avoid openings like:

- "最近我在做 Codex skill 的时候，发现一个很具体的问题。"
- "在当今时代..."
- "随着 AI 的飞速发展..."
- "你是否也曾..."
- "今天我们来聊聊..."
- Any opening that sounds like a report, class, or content hook.

## Structure

For essays and AI-use diaries, use this arc:

1. Daily entry point: a real habit, confusion, search behavior, conversation, or sudden thought.
2. Problem texture: why this is annoying, inefficient, unclear, or emotionally costly.
3. Reframing: what the user gradually realized the real problem was.
4. Process: what was tried or built, told as a connected thought rather than a task list.
5. Meaning: why the process matters to the user, not just what the tool does.
6. Practical use: how it can be used next time, explained lightly.
7. Closing: a restrained conclusion that returns to the user's original problem.

For the idea-coach topic specifically, prefer this line:

- The user often starts with a vague idea and gathers information from AI, Xiaohongshu, Zhihu, or other sources.
- The pain is not only lack of information, but wasted time, scattered judgment, and unclear first steps.
- The sudden thought is: why not create a thinking-assistant skill that helps clarify an idea before solving it?
- The key requirement is not "give me a full solution", but "help me identify the essential problem first". The user's mantra is pursuing the essence.
- Each stage should wait for confirmation before moving on, because the user wants a tool that helps thinking, not an agent that runs ahead.

## Paragraph Rhythm

Write by paragraph-level meaning, not by sentence-level display.

Good rhythm:

- One paragraph can hold a complete observation with two to five sentences.
- Use a few short paragraphs for turns, but not every line.
- Allow occasional longer sentences when they sound like natural thinking or chat.
- Keep transitions soft: "后来我发现", "这个过程里", "所以我更需要的是", "说白了", "反正", "至少在我这里是这样".

Avoid:

- A stack of single-line statements.
- Consecutive question lines that look like an outline.
- Overly clean symmetrical paragraphs.
- Repeated "这个模式..." openings.
- Turning every thought into a bullet list unless the user requests a structured document.

## Sentence And Diction

Prefer daily, slightly conversational phrasing:

- "一通乱查"
- "搞不清楚自己想要什么"
- "先聚焦一下"
- "听起来很合理，但还没有落到具体步骤里"
- "这对我太有用了"
- "我需要它先帮我确定本质问题"
- "我确认跟我的想法符合，再继续往下拆"
- "说白了"
- "反正"
- "不一定哈，但至少在我这里是这样"
- "追求本质是我的 mantra"

Keep the user's existing reflective vocabulary:

- 方向、具体方向、聚焦、个人定位、判断力、结构、反馈、复盘、调整、最小成本、MVP、真实反馈。
- 迷茫、内耗、空空的、难受、有能量、不舒服、浪费时间、身体反应、幸福感缺失。
- 人才、流动、连接、网络、协作、岗位、组织、公司、团队、上级、工作成果。
- 现实情况、代沟、环境、底气、信任、尊重、价值、长期、短期、责任、温度。

Use common English terms naturally when the user would use them: AI, Codex, skill, MVP, HR, KPI, pass, mantra. Add spaces around English terms when it improves readability, for example "AI 跟我说", "Codex skill", "idea coach skill".

## Sentence Pattern Guidance

Allowed, but use sparingly:

- "我以为 A，后来发现 B。"
- "比起 A，B 更..."
- "真正有用的是..."
- "问题可能不在 A，而在 B。"

Reduce:

- "不是 A，而是 B。"
- "不是我不会...也不是我没有..."
- "从 A 到 B" as a repeated framing device.
- "它的作用是..." when describing every mode or feature.
- "这点对我来说很关键" repeated without concrete detail.

When a sentence feels like a slogan, soften it with process or example.

## Writing About Process

When describing how the user created a skill or used AI:

- Tie each step to a felt need. For example, "我并不需要它先给我解决方案，我需要它一步步先确定我的本质问题".
- Explain why confirmation gates matter: they keep the tool aligned with the user's own judgment.
- Avoid dumping a feature list. Describe modes through the problem they solve in the user's thinking process.
- If listing modes is necessary, summarize them in prose first, then use a compact list only if it improves clarity.
- Avoid making GitHub, directory links, or installation details dominate the article unless the user's article is about tool setup.

## Prohibited Or High-Risk Patterns

Do not use these unless the user explicitly asks for another style:

- "在这个快节奏的时代"
- "随着 AI 的飞速发展"
- "你是否也有这样的困惑"
- "普通人如何逆袭"
- "干货满满"
- "建议收藏"
- "看完这篇你就懂了"
- "最后给你一句狠的"
- "底层逻辑" as filler
- "赋能", "抓手", "闭环", "颗粒度", "打法", "矩阵" unless quoting jargon critically
- "松弛感", "向内求", "长期主义" as trendy decoration
- Excessive quotes, excessive dashes, emoji, exaggerated exclamation, clickbait titles, forced golden sentences.

Avoid ending with "总之" or "综上所述". Prefer a concrete return to the original scene or a calm final judgment.

## Punctuation

Use Chinese punctuation by default.

- Use Chinese commas, periods, question marks, semicolons, and quotation marks.
- Reduce decorative quotation marks around ordinary concepts. Use quotes only for actual quoted phrases, ironic terms, or title-like concepts.
- Use 「」 only when preserving a title, meme, or special phrase.
- Use "—— 日期" only for date signatures or a strong final note.
- Avoid frequent colons and dash-heavy explanatory structures.
- Avoid exclamation marks except when the user's original tone clearly calls for one.

## Workflow

When writing from scratch:

1. Read `references/reference.md`.
2. Identify the user's real entry point: habit, confusion, search path, conversation, recent thought, or concrete event.
3. Identify the essence of the problem before proposing structure.
4. Draft in paragraph-level meaning units.
5. Check whether each process detail is connected to a personal reason.
6. Remove AI-report phrasing, slogan endings, mechanical contrasts, and excessive short paragraphs.

When rewriting or polishing:

1. Read `references/reference.md`.
2. Preserve the user's point of view and concrete details.
3. Turn fragmented single-sentence paragraphs into fuller paragraphs where the meaning belongs together.
4. Replace vague abstract words with concrete descriptions.
5. Reduce "不是...而是..." and other formulaic contrast structures.
6. Make the article flow as one connected thought.

When generating titles:

- Prefer clear, reflective titles over traffic bait.
- Good shapes:
  - "我给自己做了一个 idea coach skill"
  - "关于 AI 使用，我后来发现更重要的是工作流"
  - "找 AI 算命，它说我还没..."
  - "X 困境"
- Avoid overpromising, fear hooks, and exaggerated results.

## English Transfer Rules

If the user asks for English writing:

- Transfer structure, tone, restraint, and reflective pacing from the Chinese style.
- Use plain English and avoid LinkedIn-style inspiration.
- Do not claim to reproduce the user's exact English style unless English samples are provided.

## Output Rules

- Default output language follows the user's request.
- For WeChat Official Account or personal essays, produce clean Markdown with readable mobile paragraphs, but do not split every sentence into its own paragraph.
- Do not explain that you used this skill unless the user asks.
- If the topic lacks a concrete entry point, ask at most two questions or make a conservative assumption and state it briefly.
