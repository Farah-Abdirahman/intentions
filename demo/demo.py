#!/usr/bin/env python3
"""
intentions/demo/demo.py

Demonstrates the power of Intentions by running the same message through
Claude twice — once without any intention, once with an INTENTION.md loaded.

The difference in response quality is the proof.

Usage:
    python demo.py                          # interactive mode, pick intention
    python demo.py --intention emotional    # load a specific intention type
    python demo.py --intention exploratory --message "I want to start a side project"

Requirements:
    pip install boto3 pyyaml rich

Environment variables:
    AWS_ACCESS_KEY_ID       Your AWS access key
    AWS_SECRET_ACCESS_KEY   Your AWS secret key
    AWS_REGION              e.g. us-east-1 (default: us-east-1)
    BEDROCK_MODEL_ID        e.g. anthropic.claude-sonnet-4-5-20251001
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import boto3
    import yaml
    from rich.console import Console
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.prompt import Prompt, IntPrompt
    from rich.table import Table
    from rich import box
except ImportError:
    print("\n[!] Missing dependencies. Run:\n\n    pip install boto3 pyyaml rich\n")
    sys.exit(1)

console = Console()

# ── Config ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
INTENTIONS_DIR = REPO_ROOT / "intentions"

INTENTION_TYPES = ["emotional", "executional", "exploratory", "decisional"]

INTENTION_COLORS = {
    "emotional":   "bright_magenta",
    "executional": "bright_cyan",
    "exploratory": "bright_blue",
    "decisional":  "bright_yellow",
}

INTENTION_ICONS = {
    "emotional":   "◎",
    "executional": "◈",
    "exploratory": "◇",
    "decisional":  "◆",
}

DEFAULT_MODEL = "anthropic.claude-sonnet-4-5-20251001"

# ── Parser ────────────────────────────────────────────────────────────────────

def parse_intention_file(path: Path) -> dict:
    """Parse an INTENTION.md file into frontmatter + body."""
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not match:
        console.print(f"[red]Could not parse frontmatter in {path}[/red]")
        sys.exit(1)
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        console.print(f"[red]YAML error in {path}: {e}[/red]")
        sys.exit(1)

    body = match.group(2).strip()
    return {
        "name":         frontmatter.get("name", "unknown"),
        "description":  frontmatter.get("description", ""),
        "type":         frontmatter.get("type", ""),
        "output":       frontmatter.get("output", {}),
        "drift_signals":frontmatter.get("drift_signals", []),
        "body":         body,
    }


def build_system_prompt(intention: dict, user_context: str = "") -> str:
    """Build a system prompt from a parsed intention."""
    output = intention.get("output", {})
    length = output.get("length", "medium")
    fmt    = output.get("format", "prose")
    tone   = output.get("tone", "casual")

    prompt = f"""You are operating in {intention['name'].upper()} mode.

{intention['body']}

OUTPUT PREFERENCES:
- Length: {length}
- Format: {fmt}
- Tone: {tone}
"""
    if user_context:
        prompt += f"\nCONTEXT: {user_context}"
    return prompt.strip()


# ── Bedrock call ──────────────────────────────────────────────────────────────

def call_claude(bedrock_client, model_id: str, message: str, system_prompt: str = None) -> str:
    """Call Claude via Bedrock with or without a system prompt."""
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": message}],
            }
        ],
    }
    if system_prompt:
        payload["system"] = system_prompt

    response = bedrock_client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


# ── Display ───────────────────────────────────────────────────────────────────

def display_header():
    console.print()
    console.rule("[bold white]INTENTIONS DEMO[/bold white]")
    console.print(
        "[dim]Same message. Same model. Different purpose context.[/dim]",
        justify="center"
    )
    console.print()


def display_intention_menu() -> str:
    descriptions = {
        "emotional":   "Feel heard, process, think out loud",
        "executional": "Get something specific done",
        "exploratory": "Brainstorm, discover, no fixed destination",
        "decisional":  "Weigh options, reach a conclusion",
    }
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("num",  style="dim", width=4)
    table.add_column("icon", width=3)
    table.add_column("name", style="bold")
    table.add_column("description", style="dim")

    for i, t in enumerate(INTENTION_TYPES, 1):
        color = INTENTION_COLORS[t]
        table.add_row(
            str(i),
            f"[{color}]{INTENTION_ICONS[t]}[/{color}]",
            f"[{color}]{t}[/{color}]",
            descriptions[t],
        )

    console.print(table)
    choice = IntPrompt.ask("Pick an intention", choices=["1","2","3","4"])
    return INTENTION_TYPES[choice - 1]


def display_intention_loaded(intention: dict):
    itype  = intention["name"]
    color  = INTENTION_COLORS.get(itype, "white")
    icon   = INTENTION_ICONS.get(itype, "•")
    output = intention.get("output", {})
    output_str = f"{output.get('length','?')} · {output.get('format','?')} · {output.get('tone','?')}"
    console.print(
        f"  [{color}]{icon} Loaded:[/{color}] [bold]{itype}[/bold]  "
        f"[dim]output: {output_str}[/dim]"
    )
    console.print()


def display_comparison(message, without_response, with_response, intention):
    itype = intention["name"]
    color = INTENTION_COLORS.get(itype, "white")
    icon  = INTENTION_ICONS.get(itype, "•")

    console.print()
    console.rule("[dim]message[/dim]")
    console.print(Panel(f'[italic]"{message}"[/italic]', border_style="dim"))
    console.print()
    console.rule("[dim]responses[/dim]")
    console.print()

    without_panel = Panel(
        without_response,
        title="[bold white]Without Intention[/bold white]",
        title_align="left",
        border_style="dim white",
        padding=(1, 2),
    )
    with_panel = Panel(
        with_response,
        title=f"[bold {color}]{icon} With {itype} intention[/bold {color}]",
        title_align="left",
        border_style=color,
        padding=(1, 2),
    )

    console.print(Columns([without_panel, with_panel], equal=True, expand=True))
    console.print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Intentions demo — shows before/after Claude responses"
    )
    parser.add_argument("--intention", "-i", choices=INTENTION_TYPES)
    parser.add_argument("--message",   "-m", type=str)
    parser.add_argument("--context",   "-c", type=str, default="")
    parser.add_argument("--region",    "-r", type=str,
                        default=os.environ.get("AWS_REGION", "us-east-1"))
    parser.add_argument("--model",     type=str,
                        default=os.environ.get("BEDROCK_MODEL_ID", DEFAULT_MODEL))
    args = parser.parse_args()

    # ── AWS credentials check
    if not os.environ.get("AWS_ACCESS_KEY_ID"):
        console.print("\n[red][!] AWS credentials not found.[/red]")
        console.print("Set [bold]AWS_ACCESS_KEY_ID[/bold] and [bold]AWS_SECRET_ACCESS_KEY[/bold] env vars.\n")
        sys.exit(1)

    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=args.region,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    display_header()

    # ── Pick intention
    intention_type = args.intention or display_intention_menu()

    intention_path = INTENTIONS_DIR / intention_type / "INTENTION.md"
    if not intention_path.exists():
        console.print(f"[red]Could not find {intention_path}[/red]")
        sys.exit(1)

    intention = parse_intention_file(intention_path)
    display_intention_loaded(intention)

    # ── Get message
    message = args.message or Prompt.ask("[bold]Your message[/bold]")
    if not message.strip():
        console.print("[red]No message provided.[/red]")
        sys.exit(1)

    # ── Run both calls
    console.print()
    with console.status("[dim]Calling Claude without intention...[/dim]"):
        without_response = call_claude(bedrock, args.model, message)

    with console.status(f"[dim]Calling Claude with {intention_type} intention...[/dim]"):
        system_prompt = build_system_prompt(intention, args.context)
        with_response = call_claude(bedrock, args.model, message, system_prompt)

    # ── Show comparison
    display_comparison(message, without_response, with_response, intention)

    # ── Footer
    console.rule()
    console.print(
        f"  [dim]Intention loaded from:[/dim] [bold]{intention_path.relative_to(REPO_ROOT)}[/bold]"
    )
    console.print(
        "  [dim]Fork and add your own intentions at[/dim] "
        "[bold]github.com/YOUR_USERNAME/intentions[/bold]"
    )
    console.print()


if __name__ == "__main__":
    main()
