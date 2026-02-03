# openclaw-skill-link-tracker

An [OpenClaw](https://github.com/openclaw/openclaw) skill for tracking link clicks.

## Overview

A lightweight redirect server that logs link clicks. Use it for:

- **Preference Learning** — Track which links users click to learn their interests
- **Newsletter Analytics** — Measure engagement with shared content
- **A/B Testing** — Compare click-through rates by tagging links

## Installation

```bash
# Clone
git clone https://github.com/ymat19/openclaw-skill-link-tracker.git

# Symlink to OpenClaw skills
ln -s /path/to/openclaw-skill-link-tracker/skill ~/.openclaw/skills/link-tracker
```

Or add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/openclaw-skill-link-tracker/skill"]
    }
  }
}
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
