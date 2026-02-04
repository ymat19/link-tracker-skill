---
name: link-tracker
description: Track link clicks via redirect server for preference learning. Generate tracking URLs for reports, analyze click logs to learn user interests.
metadata:
  openclaw:
    emoji: "🔗"
    requires: { bins: ["docker", "curl"] }
---

# Link Tracker

Generate tracking URLs and analyze click logs for preference learning.

## Start Server

```bash
cd ~/repos/link-tracker-skill/skill && docker compose up -d
```

Check status:

```bash
curl -s http://192.168.0.29:59934/health
```

## Generate Tracking URL

```python
from urllib.parse import quote
tracking_url = f"http://192.168.0.29:59934/r?url={quote(original_url, safe='')}&tags={tags}"
```

Tags are comma-separated (e.g., `github,typescript,trending`).

## Read Click Logs

```bash
curl -s http://192.168.0.29:59934/logs?limit=100
```

Or read directly:

```bash
cat ~/repos/link-tracker-skill/skill/data/clicks.jsonl
```

Log format (JSON Lines):

```json
{"ts":"2026-02-03T11:00:00Z","url":"https://github.com/user/repo","tags":["github","typescript"]}
```

## API

- `GET /r?url=<encoded_url>&tags=<tags>` — Log click and redirect
- `GET /stats` — Total click count
- `GET /logs?limit=N` — Recent log entries
- `GET /health` — Health check
