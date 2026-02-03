---
name: link-tracker
description: Track link clicks via a local redirect server. Use when generating reports with trackable links, analyzing user interests, or building preference learning systems. Convert URLs to tracking URLs and read click logs for feedback.
---

# Link Tracker

A lightweight redirect server that logs link clicks for preference learning and analytics.

## Quick Start

### 1. Start the server

```bash
cd {baseDir}
docker compose up -d
```

### 2. Generate tracking URLs

Convert a regular URL to a tracking URL:

```
Original:  https://github.com/user/repo
Tracking:  http://localhost:59934/r?url=https%3A%2F%2Fgithub.com%2Fuser%2Frepo&tags=github,trending
```

URL encoding is required for the `url` parameter. Tags are optional, comma-separated.

### 3. Read click logs

Logs are stored at `{baseDir}/data/clicks.jsonl` (JSON Lines format):

```json
{"ts":"2026-02-03T11:00:00.000Z","url":"https://github.com/user/repo","tags":["github","trending"]}
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /r?url=<url>&tags=<tags>` | Log click and redirect to URL |
| `GET /health` | Health check |
| `GET /stats` | Total click count |
| `GET /logs?limit=100` | Recent log entries |

## Configuration

Environment variables (set in docker-compose.yml):

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 59934 | Listen port |
| LOG_PATH | /data/clicks.jsonl | Log file path |
| LOG_UA | false | Log User-Agent |
| LOG_IP | false | Log client IP |
| ALLOWED_DOMAINS | (empty) | Domain whitelist (empty = all) |

## Use Cases

### Daily GitHub Trend Reports

Generate tracking URLs for each repository link, then analyze clicks to learn user preferences.

### Link Interest Analysis

Tag links by category (e.g., `typescript`, `ai`, `devops`) and analyze which tags get clicked most.

## Helper: URL Encoding

Python:
```python
from urllib.parse import quote
tracking_url = f"http://localhost:59934/r?url={quote(original_url, safe='')}&tags={tags}"
```

Bash:
```bash
python3 -c "from urllib.parse import quote; print(quote('$URL', safe=''))"
```
