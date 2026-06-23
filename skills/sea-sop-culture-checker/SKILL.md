---
name: sea-sop-culture-checker
description: Analyze Chinese headquarters SOPs, KPIs, policies, workflows, and management rules for Southeast Asia rollout risks. Use when users need clause-level cultural conflict pre-checks, Hofstede-based China-vs-Southeast-Asia comparison, red/yellow/green risk heatmaps, and business-ready Chinese-English localized rewrites for overseas subsidiaries.
---

# Southeast Asia SOP/KPI Culture Checker

## Purpose

Use this skill to pre-check whether Chinese headquarters SOPs, KPIs, policies, workflows, or management notices may create cultural friction when rolled out in Southeast Asian subsidiaries.

The output should help business teams see which clauses are likely to trigger resistance, misunderstanding, silence, avoidance, loss of trust, or execution distortion, then rewrite those clauses into practical Chinese and English local rollout language.

This is a management communication and localization aid. It is not a legal compliance review, academic research conclusion, or individual employee assessment.

## Required References

Before every SOP/KPI analysis, read these files:

1. `references/hofstede-sea-country-profiles.md`
2. `references/sop-risk-mapping-rules.md`
3. `references/output-templates.md`

Do not analyze Southeast Asian cultural risk from generic memory alone. Use the reference files as the primary rule base.

## Inputs

Required:

- Chinese SOP, KPI, policy, workflow, management notice, or performance rule text.
- Target Southeast Asian country or countries.

Optional:

- Business context, such as factory, sales, customer service, HR, retail, operations, regional management, or general management policy.
- Desired output language. Default to Chinese-English bilingual.
- Single-country analysis or multi-country comparison.

If the target country is missing, ask one concise follow-up question before analysis.

If the business context is missing, proceed with "general management policy" as the default context.

## Supported Countries

Primary scope:

- Vietnam
- Thailand
- Indonesia
- Malaysia
- Singapore
- Philippines
- Cambodia
- Laos
- Myanmar
- Brunei

Use China as the headquarters comparison baseline when relevant.

## Workflow

### Step 1: Confirm Scope

Summarize:

- target country or countries;
- business context;
- document type;
- output language.

If the input is sufficient, proceed directly. Do not over-question.

### Step 2: Split Clauses

Break the SOP/KPI into clause-level items.

For each clause, identify:

- original clause;
- instruction verbs;
- management action;
- intended headquarters control objective;
- clause type.

Common instruction verbs include:

- 必须
- 严禁
- 不得
- 每日汇报
- 立即整改
- 统一执行
- 未完成扣罚
- 需审批
- 责任到人
- 排名通报
- 强制参加
- 限时完成

### Step 3: Map Cultural Risks

Use `references/hofstede-sea-country-profiles.md` and `references/sop-risk-mapping-rules.md`.

For each clause, map likely risks to:

- Power Distance
- Individualism vs Collectivism
- Masculinity
- Uncertainty Avoidance
- Long Term Orientation
- Indulgence
- direct vs indirect communication
- face-saving and psychological safety
- autonomy and local manager authority

Use two comparison layers:

1. Absolute reading: low, medium, or high score range for the target country.
2. China-baseline gap: how far the target country differs from China on the same dimension.

Avoid absolute claims. Phrase findings as risk signals, likely interpretations, or implementation concerns.

### Step 4: Assign Risk Level

Use three levels:

- Red: high risk. The clause may trigger resistance, silence, avoidance, loss of trust, or execution distortion. Rewrite before rollout.
- Yellow: medium risk. The clause can be retained but needs explanation, softer wording, manager enablement, or implementation guardrails.
- Green: low risk. The clause is generally safe, with minor localization if needed.

Every red or yellow item must include a specific reason tied to the clause and target country profile.

### Step 5: Generate Rewrites

For each relevant clause, produce:

1. Original clause
2. Headquarters rigid version
3. Localized soft-landing Chinese version
4. Localized soft-landing English version
5. Rollout note for managers

The localized version must preserve the headquarters management intent while reducing unnecessary command tone, punishment framing, public pressure, or mistrust signals.

### Step 6: Produce Final Report

Use `references/output-templates.md`.

The final report must include:

- title;
- executive summary;
- target country cultural profile;
- red/yellow/green risk heatmap;
- clause-level analysis;
- bilingual rewrite draft;
- rollout suggestions;
- HR/legal review reminder.

## Output Rules

Write in Chinese by default.

For English rewrites:

- use clear business English;
- avoid machine-translation style;
- avoid overly legalistic wording unless the original clause requires it;
- preserve enforceability where needed.

For risk explanations:

- be concrete;
- tie each risk to a clause;
- avoid stereotypes;
- distinguish cultural risk from legal, compensation, process, or operational issues.

## Disclaimer

Hofstede cultural dimensions are used as a management reference and early-warning framework only. They should not be treated as deterministic descriptions of individuals, legal advice, or academic research conclusions. Final rollout should be reviewed by local HR, legal, and business managers.
