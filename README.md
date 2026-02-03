# Link Tracker Skill 🔗

An [OpenClaw](https://github.com/openclaw/openclaw) skill that provides a lightweight redirect server for tracking link clicks. Perfect for preference learning, analytics, and understanding user interests.

## Use Cases

### 📊 Daily Report Preference Learning
Generate daily GitHub trending reports with tracking URLs. Analyze which repositories users click to learn their interests and refine future recommendations.

### 🎯 Newsletter Engagement
Track which links in automated notifications get clicked. Understand what content resonates with users.

### 🔬 A/B Content Testing
Compare click-through rates on different content types by tagging links with categories (e.g., `typescript`, `ai`, `devops`).

### 📈 Interest Analytics
Build a preference profile over time by analyzing click patterns across tags and domains.

## Features

- **Simple**: Single Python file, zero dependencies (stdlib only)
- **Trackable URLs**: Redirect via `/r?url=<url>&tags=<tags>`
- **JSON Logs**: Append-only JSON Lines format for easy parsing
- **Containerized**: Docker-ready for always-on deployment
- **Configurable**: Environment variables for all settings

## Quick Start

### Docker (Recommended)

```bash
docker compose up -d
```

### Direct

```bash
python3 tracker.py
```

## Usage

### Generate Tracking URL

```
Original:  https://github.com/user/repo
Tracking:  http://<host>:59934/r?url=https%3A%2F%2Fgithub.com%2Fuser%2Frepo&tags=github,typescript
```

### Check Logs

```bash
cat data/clicks.jsonl
```

```json
{"ts":"2026-02-03T11:00:00.000Z","url":"https://github.com/user/repo","tags":["github","typescript"]}
```

## API

| Endpoint | Description |
|----------|-------------|
| `GET /r?url=<url>&tags=<tags>` | Log click and redirect |
| `GET /health` | Health check |
| `GET /stats` | Total click count |
| `GET /logs?limit=N` | Recent log entries |

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `PORT` | 59934 | Server port |
| `LOG_PATH` | /data/clicks.jsonl | Log file path |
| `LOG_UA` | false | Log User-Agent |
| `LOG_IP` | false | Log IP address |
| `ALLOWED_DOMAINS` | (empty) | Domain whitelist (empty = all) |

## OpenClaw Integration

This repository is an OpenClaw skill. Install by symlinking:

```bash
git clone https://github.com/<user>/openclaw-skill-link-tracker.git
ln -s /path/to/openclaw-skill-link-tracker ~/.openclaw/skills/link-tracker
```

Or add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/openclaw-skill-link-tracker"]
    }
  }
}
```

## License

MIT
