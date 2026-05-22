# Intentions Specification

> Version 0.1.0 — Draft

---

## What is an Intention?

An Intention is a lightweight, portable file that gives an AI agent **purpose context** before a conversation begins.

Humans never talk in a vacuum. Every conversation has an underlying *why* — a purpose that shapes what they need, how they want to be spoken to, and what success looks like. Without declared intention, agents default to a generic helpful mode that often mismatches what the user actually needs.

Intentions solve this by making purpose context a first-class, structured element of every conversation.

---

## Directory Structure

An intention is a folder containing, at minimum, an `INTENTION.md` file:

```
intention-name/
├── INTENTION.md        # Required: metadata + instructions
├── references/         # Optional: supporting documentation
├── examples/           # Optional: example conversations
└── assets/             # Optional: templates, resources
```

---

## `INTENTION.md` Format

The `INTENTION.md` file must contain YAML frontmatter followed by Markdown content.

### Frontmatter

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier. Lowercase, hyphens for spaces. Max 64 chars. |
| `description` | Yes | What this intention does and when to use it. Used by agents to decide when to activate. |
| `type` | Yes | One of: `emotional`, `executional`, `exploratory`, `decisional` |
| `output` | No | Default output preferences: `length`, `format`, `tone` |
| `drift_signals` | No | List of strong signals that indicate the intention may have shifted |
| `version` | No | Semver string e.g. `1.0.0` |
| `author` | No | Author name or handle |
| `license` | No | License identifier e.g. `Apache-2.0` |

### Minimal Example

```yaml
---
name: exploratory
description: Use when the user wants to brainstorm, discover, or think without a fixed destination. No fixed answer expected.
type: exploratory
---
```

### Full Example

```yaml
---
name: exploratory
description: Use when the user wants to brainstorm, discover, or think without a fixed destination. No fixed answer expected.
type: exploratory
version: 1.0.0
author: intentions-project
license: Apache-2.0
output:
  length: short
  format: prose
  tone: casual
drift_signals:
  - explicit redirect from user ("actually...", "wait...", "never mind")
  - emotional language appearing mid-task
  - user expresses frustration or feeling lost
---
```

---

## Markdown Body

The Markdown body after the frontmatter contains the agent instructions. There are no strict format restrictions — write whatever helps the agent serve the user's purpose effectively.

**Recommended sections:**

- **Mode description** — what this intention means and why it exists
- **Behavior rules** — what the agent should do in this mode
- **What to stop** — behaviors the agent should suppress in this mode
- **Output guidance** — how responses should be shaped
- **Drift handling** — how to respond when drift is detected

---

## The Three-Field Template

Every intention conversation is anchored by three fields the user fills in:

| Field | Type | Description |
|-------|------|-------------|
| `intention` | Structured choice | One of the four intention types |
| `output` | Structured choices | Length · Format · Tone |
| `context` | Free text | What this conversation is actually about |

The `output` field accepts:

- **length**: `short` · `medium` · `detailed`
- **format**: `prose` · `bullets` · `table` · `code`
- **tone**: `casual` · `formal` · `direct`

---

## Intention Types

There are four core intention types. Each changes how the agent behaves — not just in tone, but in what it prioritizes and what it suppresses.

| Type | Core Need | Agent Mode |
|------|-----------|------------|
| `emotional` | Feel heard, process, think out loud | Listens deeply, reflects back, no unsolicited advice |
| `executional` | Get something specific done | Direct, efficient, output-focused, no fluff |
| `exploratory` | Brainstorm, discover, no fixed destination | Divergent ideas, open questions, no rushing |
| `decisional` | Weigh options, reach a conclusion | Structured tradeoffs, clear recommendation |

---

## Drift Detection

Intentions shift mid-conversation. Agents should monitor for **strong signals** of drift and surface a light nudge — without interrupting unnecessarily.

### Strong Signals (trigger a nudge)
- Emotional expression mid-task: *"this is frustrating"* / *"actually..."* / *"wait..."*
- An explicit redirect from the user
- A clear tonal shift away from the declared intention

### Weak Signals (adapt quietly, no nudge)
- Slight topic shift
- A tangential question
- Minor change in phrasing

### The Nudge
When a strong signal is detected, the agent surfaces:

> *"Feels like we've shifted a bit — still in [intention] mode or want to switch?"*

**Cooldown rule:** After flagging drift once, the agent does not flag again for a meaningful period — even if weak signals continue. This prevents pestering.

**Confirmation rule:** The user confirms before the agent changes modes. Detection without confirmation is presumptuous.

---

## Intention Memory

Agents may optionally build a personal intention profile over time.

- **Opt-in only** — never built without explicit user consent
- **Reminded at natural moments** — on first use, or when consistent patterns emerge. Never intrusively.
- **Personal profile** — surfaces defaults before the user fills in the template: *"You usually start in Exploratory — want to use that as your default?"*
- **Community contribution** — anonymized pattern data may feed community templates, with user permission

---

## Community Templates

Named intention configurations that combine all three fields into a reusable package. Crowdsourced by the community — the same way skills evolved.

```yaml
---
name: therapy-mode
description: Processing a hard day or difficult personal situation
type: emotional
output:
  length: short
  format: prose
  tone: casual
---
```

Anyone can contribute a community template by opening a pull request.

---

## Compatibility

Intentions follow the same folder-based, markdown-first philosophy as [Agent Skills](https://agentskills.io). They are designed to be:

- **Portable** — work across any agent that supports the format
- **Composable** — can be used alongside skills
- **Forkable** — copy, modify, and share freely
- **Version-controlled** — plain text, git-friendly

---

*Intentions format — open standard — Apache 2.0*
