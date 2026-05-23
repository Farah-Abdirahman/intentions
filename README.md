# Intentions

> *Humans never talk in a vacuum. Every conversation has a why.*

**Intentions** is a lightweight, open format for giving AI agents **purpose context** — a declared reason for the conversation that shapes how the agent behaves from the first response.


---

## The Problem

Without declared intention, agents default to a generic helpful mode that often mismatches what users actually need:

- Someone venting about work gets unsolicited advice instead of being heard
- Someone who needs a quick answer gets a long explanation
- Someone brainstorming gets pushed toward a conclusion too early
- Someone who needs a decision gets open-ended exploration instead

This isn't a knowledge gap. It's a **purpose gap**. The agent has the capability — it just lacks the context to deploy it correctly.

---

## The Solution

A simple, structured file — `INTENTION.md` — that declares the purpose of a conversation before it begins.

```yaml
---
name: exploratory
description: Use when the user wants to brainstorm without a fixed destination.
type: exploratory
output:
  length: short
  format: prose
  tone: casual
drift_signals:
  - user commits to a direction
  - concrete deliverable appears
---

# Exploratory Mode

Be a thinking partner, not an answer machine. Offer divergent ideas.
Ask questions that open directions, not close them. Don't rush to conclusions...
```

That's it. A folder with a file. The agent loads it, and the entire conversation is anchored to a declared purpose.

---

## The Three-Field Template

Every intention conversation is anchored by three fields:

| Field | Type | Description |
|-------|------|-------------|
| **Intention** | Structured choice | One of the four intention types |
| **Output** | Structured choices | Length · Format · Tone |
| **Context** | Free text | What this conversation is actually about |

Simple enough to fill in quickly. Powerful enough to change everything about how the agent responds.

---

## The Four Core Intentions

| Type | Core Need | Agent Mode |
|------|-----------|------------|
| [`emotional`](./intentions/emotional/INTENTION.md) | Feel heard, process, think out loud | Listens deeply, reflects back, no unsolicited advice |
| [`executional`](./intentions/executional/INTENTION.md) | Get something specific done | Direct, efficient, output-focused, no fluff |
| [`exploratory`](./intentions/exploratory/INTENTION.md) | Brainstorm, discover, no fixed destination | Divergent ideas, open questions, no rushing |
| [`decisional`](./intentions/decisional/INTENTION.md) | Weigh options, reach a conclusion | Structured tradeoffs, clear recommendation |

---

## Drift Detection

Intentions shift mid-conversation. Agents monitor for **strong signals** and surface a light nudge — without interrupting unnecessarily.

**Strong signals** (trigger a nudge):
- Emotional expression mid-task: *"this is frustrating"* / *"actually..."*
- An explicit redirect from the user
- A clear tonal shift away from the declared intention

**Weak signals** (agent adapts quietly, no nudge):
- Slight topic shift
- A tangential question

**The nudge:**
> *"Feels like we've shifted a bit — still in Exploratory mode or want to switch?"*

A **cooldown** prevents repeat nudges. The user **confirms** before the agent changes modes.

---

## Intention Memory

Agents may optionally build a personal intention profile over time.

- **Opt-in only** — never built without explicit user consent
- **Reminded at natural moments** — on first use or when patterns emerge. Never intrusively.
- **Surfaces defaults** — *"You usually start in Exploratory — want to use that as your default?"*
- **Feeds community templates** — anonymized patterns, with user permission

---

## Community Intentions

Named, reusable configurations that combine intention type + output preferences for a specific use case. Anyone can contribute.

| Name | Type | Best for |
|------|------|----------|
| [therapy-mode](./community/therapy-mode/INTENTION.md) | emotional | Processing a hard day |
| [sprint-mode](./community/sprint-mode/INTENTION.md) | executional | Shipping fast under pressure |

Browse all community intentions in [`/community`](./community/) →

---

## Repository Structure

```
intentions/
├── README.md                        # You are here
├── spec/
│   └── INTENTION_SPEC.md            # Full format specification
├── template/
│   └── INTENTION.md                 # Blank template — copy to get started
├── intentions/
│   ├── emotional/
│   │   └── INTENTION.md
│   ├── executional/
│   │   └── INTENTION.md
│   ├── exploratory/
│   │   └── INTENTION.md
│   └── decisional/
│       └── INTENTION.md
└── community/
    ├── README.md
    ├── therapy-mode/
    │   └── INTENTION.md
    └── sprint-mode/
        └── INTENTION.md
```

---

## Creating Your Own Intention

1. Copy [`/template/INTENTION.md`](./template/INTENTION.md) into a new folder
2. Fill in the frontmatter — `name`, `description`, `type`, `output`, `drift_signals`
3. Write the markdown body — behavior rules, what to stop, output guidance, drift handling
4. Use it locally or open a PR to share it with the community

See the [full specification](./spec/INTENTION_SPEC.md) for all available fields.

---

## Demo — See It In Action

The demo script runs the same message through Claude twice — once without any intention, once with an `INTENTION.md` loaded — and shows the responses side by side in the terminal.

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/intentions.git
cd intentions

# Install dependencies
pip install boto3 pyyaml rich

# Set your API key
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-20251001

# Run interactively — pick an intention, type a message
python demo/demo.py

# Or specify directly
python demo/demo.py --intention emotional --message "I've been really struggling lately and I don't know why"
python demo/demo.py --intention executional --message "Write me a Python function to parse a CSV file"
python demo/demo.py --intention exploratory --message "I want to start something on the side but have no idea what"
python demo/demo.py --intention decisional --message "Should I learn React or Vue for my first frontend project?"
```

The difference in response quality is the proof.

---

## Contributing

Intentions is open to contributions from anyone. The best way to contribute is to share an intention that solves a real, recurring use case.

To contribute a community intention:

1. Fork this repo
2. Add your intention folder under `/community/your-intention-name/`
3. Open a pull request with a brief description of the use case it solves

The format is intentionally simple. If it fits in a `SKILL.md`, it fits here.

---

## Compatibility

Intentions follow the same folder-based, markdown-first philosophy as [Agent Skills](https://agentskills.io). They are:

- **Portable** — work across any agent that supports the format
- **Composable** — can be used alongside skills
- **Forkable** — copy, modify, share freely
- **Version-controlled** — plain text, git-friendly

---

## Origin

This format was developed through a conversation exploring how humans bring purpose to every interaction — and how agents could be given the same grounding.

The feature concept, the four intention types, the three-field template, drift detection, intention memory, and the community crowdsourcing model were all developed collaboratively before a single line was written.

---

*Intentions — open format — Apache 2.0*

---

## Installation

### Claude Code

Register the intentions repo as a plugin:

```bash
/plugin marketplace add YOUR_USERNAME/intentions
```

Then install:

```bash
/plugin install intentions
```

Use in any conversation:

```bash
/load-intention exploratory
/load-intention executional short bullets direct "shipping a feature today"
/load-intention emotional
```

Or just start talking — Claude will auto-detect context and activate the right intention mode.

### Claude.ai (browser)

Copy the contents of any `skills/[type]/SKILL.md` into your **Custom Instructions** under Settings. This anchors every conversation to that intention by default.

To switch intentions, update your custom instructions before starting a new conversation.
