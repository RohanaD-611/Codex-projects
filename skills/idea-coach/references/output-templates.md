# Idea Coach Output Templates

Use these templates for stage outputs. Keep them readable for the user and executable for another Codex agent. Translate section headings and confirmation prompts into the user's language unless the user requests another language.

## Requirement Clarification Document

````markdown
# Requirement Clarification

## 1. Idea Snapshot
- Original idea:
- Intended user:
- Current uncertainty:

## 2. Core Pain
- Problem to solve:
- Why it matters:
- What failure looks like:

## 3. Minimum Scope
- Best first slice:
- Why this slice first:
- Success signal:

## 4. Input Data
- Required information:
- Source:
- Missing information:

## 5. Processing Flow
1.
2.
3.

## 6. Output Location And Shape
- Landing location:
- Output format:
- Who reviews or uses it:

## 7. Initial Product Shape
- First usable version should:
- It should not:

## 8. Assumptions
-

## 9. Open Decisions
-

## Confirmation Gate
Ask whether to enter Product Manager Coach mode to judge priority and narrow the minimum scope. Offer exactly these choices: yes; no, needs adjustment.
````

## MVP Workflow Document

````markdown
# MVP Workflow

## 1. Confirmed Direction
- Goal:
- Target user:
- First slice:

## 2. Priority Decision
- Must have:
- Should do later:
- Not doing now:

## 3. Workflow Segments

### Segment 1:
- Purpose:
- Input:
- Processing:
- Output:
- Acceptance criteria:

### Segment 2:
- Purpose:
- Input:
- Processing:
- Output:
- Acceptance criteria:

## 4. Minimum Demo Definition
- Demo starts when:
- Demo ends when:
- Demo is successful if:

## 5. Risks And Constraints
-

## 6. Open Decisions
-

## Confirmation Gate
Ask whether to enter Skill Architect mode to turn the workflow into a skill structure and SKILL.md draft. Offer exactly these choices: yes; no, needs adjustment.
````

## Skill Architecture Document

````markdown
# Skill Architecture

## 1. Skill Name
-

## 2. Trigger Conditions
- Use when:
- Do not use when:

## 3. Operating Modes
- Default mode:
- Optional modes:

## 4. Required Inputs
-

## 5. Conversation Rules
- Question limit:
- Confirmation gates:
- Stop conditions:

## 6. Output Templates
-

## 7. File Structure
```text
skills/
  skill-name/
    SKILL.md
    references/
      output-templates.md
```

## 8. Content Placement
- Put in `SKILL.md`:
- Put in `references/`:
- Do not include:

## 9. SKILL.md Draft

```markdown
---
name:
description:
---

# Skill Title

## Purpose

## Workflow

## Question Rules

## Output Rules
```
````

## Minimum Demo Summary

````markdown
# Minimum Demo Summary

## 1. Current First Slice

## 2. Core Problem This Slice Solves

## 3. Required Capabilities

## 4. Inputs

## 5. Outputs

## 6. First Landing Location

## 7. Explicitly Out Of Scope For Now
````
