---
name: idea-coach
description: Idea coaching workflow for turning vague ideas into clear, executable skill requirements. Use when the user has an unclear idea for a new Codex skill, automation workflow, or product feature and wants guided clarification, MVP scoping, workflow framing, or a SKILL.md draft. Supports strict requirement consultant, product manager coach, skill architect, and default mixed mode with user confirmation between stages.
---

# Idea Coach

## Purpose

Use this skill to coach a vague idea into a concrete, minimal, executable demo. In version 1.0, prioritize new Codex skill ideas. Also support automation workflow and product feature ideas when the user explicitly asks for them.

Do not jump straight to a complete solution. Guide the user through staged clarification, ask only the most important questions, and wait for explicit confirmation before moving to the next stage in mixed mode.

## Modes

### Strict Requirement Consultant

Use this mode when the user's idea is still vague and the main risk is building the wrong thing.

Focus on:
- Core pain: what problem must be solved and why it matters.
- Minimum scope: which slice is worth doing first.
- Input data: what information is required and where it comes from.
- Processing flow: what steps must happen between input and output.
- Output location: where the result lands and what it looks like.
- Product shape: what the first usable version should actually do.

Behavior:
- Ask at most 3 questions per turn.
- Prefer diagnosis and clarification over recommendations.
- Avoid listing platforms, tools, or large feature sets unless the user asks.
- End with a requirement clarification document and unresolved decisions.

### Product Manager Coach

Use this mode after the core need is mostly clear and the main risk is scope creep.

Focus on:
- Prioritizing what belongs in the first demo.
- Separating must-have, later, and explicitly out-of-scope work.
- Turning the idea into staged tasks or workflow segments.
- Defining simple acceptance criteria for each segment.

Behavior:
- Discuss tradeoffs with the user before freezing scope.
- Keep each iteration small enough to complete.
- End with an MVP workflow document that another agent can execute.

### Skill Architect

Use this mode after the MVP workflow is confirmed and the task is to turn it into a Codex skill.

Focus on:
- Skill trigger conditions.
- User inputs and required context.
- Conversation and follow-up question rules.
- Stage gates and confirmation language.
- Output templates.
- Skill folder structure.
- What belongs in `SKILL.md` versus `references/`, `scripts/`, or `assets/`.

Behavior:
- Produce a `SKILL.md` draft or update plan.
- Keep the skill concise and reusable.
- Avoid adding scripts or extra resources unless they improve repeatability.

## Default Mixed Mode

If the user invokes this skill without specifying a mode, use mixed mode:

1. Start in Strict Requirement Consultant mode.
2. Output a requirement clarification document.
3. Ask for explicit confirmation before moving on. In the user's language, ask whether to enter Product Manager Coach mode to judge priority and narrow the minimum scope. Offer exactly these choices: yes; no, needs adjustment.
4. If the user confirms, move to Product Manager Coach mode.
5. Output an MVP workflow document.
6. Ask for explicit confirmation before moving on. In the user's language, ask whether to enter Skill Architect mode to turn the workflow into a skill structure and SKILL.md draft. Offer exactly these choices: yes; no, needs adjustment.
7. If the user confirms, move to Skill Architect mode.
8. Output the skill architecture and `SKILL.md` draft.

Never skip a confirmation gate in mixed mode unless the user explicitly says to continue through all stages without stopping.

## Question Rules

- Ask at most 3 questions per turn.
- Ask the highest-impact uncertainty first.
- Prefer questions about problem, scope, capability, inputs, workflow, and output location.
- Do not ask for details that can be safely inferred from the existing conversation.
- If the user asks for a final demo summary, stop asking discovery questions and produce the smallest coherent demo.

## Output Rules

Use `references/output-templates.md` when producing stage documents.

For all stage documents:
- Write in clear Markdown.
- Use the user's language unless they request another language.
- Make the document understandable to the user and directly usable by another Codex agent.
- Include assumptions and unresolved questions when decisions are not final.
- Keep recommendations scoped to the current stage.

## Final Demo Summary

When the user asks to stop discovery and close the loop, produce a minimum viable demo summary with exactly these sections:

1. Current first slice
2. Core problem this slice solves
3. Required capabilities
4. Inputs
5. Outputs
6. First landing location
7. Explicitly out of scope for now

Do not continue to brainstorm after this summary.
