# link-tracker-skill

A lightweight redirect server that logs link clicks. Works as an agent skill (OpenClaw, etc.) or standalone.

## Use Cases

- **Preference Learning** — Track which links users click to learn their interests
- **Newsletter Analytics** — Measure engagement with shared content
- **A/B Testing** — Compare click-through rates by tagging links

## Installation

```bash
git clone https://github.com/ymat19/link-tracker-skill.git
```

### As Agent Skill (OpenClaw, etc.)

```bash
ln -s /path/to/link-tracker-skill/skill ~/.openclaw/skills/link-tracker
```

## Usage

See [skill/SKILL.md](skill/SKILL.md) for detailed usage instructions.

### Quick Start

```bash
cd skill
docker compose up -d
```

### API

```
GET /r?url=<encoded_url>&tags=<tags>  →  Log & redirect
GET /health                            →  Health check
```

## License

MIT
