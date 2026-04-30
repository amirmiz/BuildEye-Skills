# BuildEye Skills

Claude Code skills for the BuildEye workflow — meeting transcription, summarization, PDF export, and more.

## Skills

| Skill | What it does | Download |
|-------|-------------|----------|
| [meeting-transcriber](./meeting-transcriber/) | Full pipeline: transcribe Hebrew audio → detailed summary → 1-page executive summary → RTL Hebrew PDF | [⬇ ZIP](https://github.com/amirmiz/BuildEye-Skills/releases/latest/download/meeting-transcriber.zip) |
| [buildeye-quotation](./buildeye-quotation/) | Hebrew quotation generator: guided questions → fills BuildEye DOCX template with auto-incrementing quote number | [⬇ ZIP](https://github.com/amirmiz/BuildEye-Skills/releases/latest/download/buildeye-quotation.zip) |

## How to install a skill

1. Download the skill ZIP from the table above
2. Extract and copy the skill folder into your Claude Code skills directory
3. Claude will automatically pick it up on the next session

## Structure

Each skill lives in its own subfolder:

```
skill-name/
├── SKILL.md          ← instructions + trigger description (required)
├── scripts/          ← bundled Python scripts
└── references/       ← reference docs loaded into context as needed
```

Releases are auto-generated on every push to `main`.
