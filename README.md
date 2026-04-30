# BuildEye Skills

Claude Code skills for the BuildEye workflow — meeting transcription, summarization, PDF export, and more.

## Skills

| Skill | What it does |
|-------|-------------|
| [meeting-transcriber](./meeting-transcriber/) | Full pipeline: transcribe Hebrew audio → detailed summary → 1-page executive summary → RTL Hebrew PDF |

## How to install a skill

1. Copy the skill folder (e.g. `meeting-transcriber/`) into your Claude Code skills directory
2. Claude will automatically pick it up on the next session

## Structure

Each skill lives in its own subfolder:

```
skill-name/
├── SKILL.md          ← instructions + trigger description (required)
├── scripts/          ← bundled Python scripts
└── references/       ← reference docs loaded into context as needed
```
