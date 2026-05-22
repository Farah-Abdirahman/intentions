---
name: your-intention-name
description: >
  Describe what this intention does and when an agent should activate it.
  Be specific — agents use this to decide when to load this intention.
type: emotional | executional | exploratory | decisional  # pick one, delete the rest
version: 1.0.0
author: your-name
license: Apache-2.0
output:
  length: short | medium | detailed     # pick one
  format: prose | bullets | table | code  # pick one
  tone: casual | formal | direct          # pick one
drift_signals:
  - signal that suggests the intention has shifted
  - another signal
  - emotional language, explicit redirects, tonal shift
---

# [Intention Name]

> One sentence that captures the essence of this mode.

---

## What This Mode Is For

Explain the human need this intention serves. Why does it exist?
What gap does it close between what users need and what agents default to?

---

## Behavior Rules

What the agent should DO in this mode:

- Rule one
- Rule two
- Rule three

---

## What to Stop

What the agent should SUPPRESS in this mode — behaviors that would be
unhelpful or counterproductive given the declared intention:

- Stop doing X
- Stop doing Y

---

## Output Guidance

How responses should be shaped in this mode:

- **Length**: short / medium / detailed — and why
- **Format**: prose / bullets / table / code — and why
- **Tone**: casual / formal / direct — and why

---

## Drift Handling

What strong signals suggest the intention has shifted away from this mode?
What should the agent do when it detects them?

Strong signals for this intention:
- Signal one
- Signal two

Nudge to surface:
> "Feels like we've shifted — still in [name] mode or want to switch?"

---

## Examples

### Good activation scenario
> User says: "..."
> Why this intention fits: ...

### Poor activation scenario
> User says: "..."
> Why a different intention fits better: ...

---

## Notes

Any additional context, edge cases, or guidance for people using or
extending this intention.
