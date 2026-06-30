---
name: idea-coach
description: Idea coaching and specification-driven development workflow for turning vague ideas into clear, executable requirements. Use when the user has an unclear idea for a new Codex skill, automation workflow, product feature, or coding task and wants guided clarification, MVP scoping, a verifiable specification, workflow framing, or a SKILL.md draft. Supports strict requirement consultant, product manager coach, skill architect, default mixed mode, and a Spec gate before writing or modifying code.
---

# Idea Coach

## Purpose

Use this skill to coach a vague idea into a concrete, minimal, executable demo. In version 2.0, prioritize new Codex skill ideas, and add specification-driven development for ideas that will become code. Also support automation workflow and product feature ideas when the user explicitly asks for them.

Do not jump straight to a complete solution. Guide the user through staged clarification, ask only the most important questions, and wait for explicit confirmation before moving to the next stage in mixed mode.

When the result requires writing or modifying code, create a structured, verifiable specification before implementation. Treat the specification as a development brief that states the problem, proposed solution, constraints, non-goals, and success criteria.

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
- Preparing the material needed for a Specification Document when code may be written later.

Behavior:
- Discuss tradeoffs with the user before freezing scope.
- Keep each iteration small enough to complete.
- End with an MVP workflow document that another agent can execute.
- If the next step may involve code, include or request the missing details required for a verifiable specification.

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
- If the skill will direct an agent to write or modify code, include a Spec gate before implementation.

## Specification-Driven Development

Use specification-driven development when the user's idea may lead to writing or modifying code, building an app, changing UI, creating automation scripts, or implementing a technical workflow.

Before code, produce a Specification Document with these sections:

1. Problem Statement: state the user experience or problem in one clear sentence.
2. Proposed Solution: describe functionality, quantity, interaction, visual behavior, and any concrete numbers.
3. Technical Constraints: state the required or inferred technical stack, environment, dependencies, file locations, device targets, and implementation limits.
4. Non-goals: state what should not be built, changed, optimized, or explored in the current slice.
5. Success Criteria: state how completion will be verified, including mobile usability, workflow closure, tests, screenshots, or manual checks when relevant.

Spec behavior:
- Do not write or modify code before the user confirms the Specification Document, unless the user explicitly asks to skip the Spec gate.
- Ask at most 3 follow-up questions if the spec is missing critical information.
- If details are unknown but can be safely inferred, write them as assumptions instead of blocking.
- Make success criteria concrete enough that another Codex agent can verify the result.
- For UI work, include responsive behavior and whether mobile must work.
- For automation work, include trigger, input source, output destination, and failure handling.
- For skill work, include trigger conditions, conversation rules, output templates, and file structure.

## Default Mixed Mode

If the user invokes this skill without specifying a mode, use mixed mode:

1. Start in Strict Requirement Consultant mode.
2. Output a requirement clarification document.
3. Ask for explicit confirmation before moving on. In the user's language, ask whether to enter Product Manager Coach mode to judge priority and narrow the minimum scope. Offer exactly these choices: yes; no, needs adjustment.
4. If the user confirms, move to Product Manager Coach mode.
5. Output an MVP workflow document.
6. If the confirmed MVP may involve writing or modifying code, output a Specification Document before any implementation-oriented work.
7. Ask for explicit confirmation before moving on. In the user's language, ask whether the Specification Document is confirmed and whether to enter Skill Architect mode to turn the workflow into a skill structure and SKILL.md draft. Offer exactly these choices: yes; no, needs adjustment.
8. If no code is involved, ask for explicit confirmation before moving on. In the user's language, ask whether to enter Skill Architect mode to turn the workflow into a skill structure and SKILL.md draft. Offer exactly these choices: yes; no, needs adjustment.
9. If the user confirms, move to Skill Architect mode.
10. Output the skill architecture and `SKILL.md` draft.

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

For Specification Documents:
- Include Problem Statement, Proposed Solution, Technical Constraints, Non-goals, and Success Criteria.
- Write success criteria as verifiable checks, not vague quality claims.
- Include assumptions and open questions only when needed.

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
