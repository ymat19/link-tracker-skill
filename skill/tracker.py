#!/usr/bin/env python3
"""
Link Tracker - A simple redirect server with click logging.

Usage:
    GET /r?url=<encoded_url>&tags=<comma_separated_tags>
    GET /health

Environment variables:
    PORT        - Listen port (default: 59934)
    LOG_PATH    - Log file path (default: /data/clicks.jsonl)
    LOG_UA      - Log User-Agent (default: false)
    LOG_IP      - Log client IP (default: false)
    ALLOWED_DOMAINS - Comma-separated whitelist (default: empty = allow all)
"""

import json
import os
import sys
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote

# Configuration
PORT = int(os.environ.get("PORT", 59934))
LOG_PATH = os.environ.get("LOG_PATH", "/data/clicks.jsonl")
LOG_UA = os.environ.get("LOG_UA", "false").lower() == "true"
LOG_IP = os.environ.get("LOG_IP", "false").lower() == "true"
ALLOWED_DOMAINS = [d.strip() for d in os.environ.get("ALLOWED_DOMAINS", "").split(",") if d.strip()]


def is_allowed_url(url: str) -> bool:
    """Check if URL is allowed based on domain whitelist."""
    if not ALLOWED_DOMAINS:
        return True
    try:
        parsed = urlparse(url)
        return any(parsed.netloc == d or parsed.netloc.endswith(f".{d}") for d in ALLOWED_DOMAINS)
    except Exception:
        return False


def log_click(url: str, tags: list[str], ua: str | None, ip: str | None) -> None:
    """Append click event to log file."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "url": url,
        "tags": tags,
    }
    if LOG_UA and ua:
        entry["ua"] = ua
    if LOG_IP and ip:
        entry["ip"] = ip

    # Ensure log directory exists
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class TrackerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for link tracking."""

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def send_json(self, status: int, data: dict) -> None:
        """Send JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Health check
        if path == "/health":
            self.send_json(200, {"status": "ok"})
            return

        # Redirect endpoint
        if path == "/r":
            url_list = query.get("url", [])
            if not url_list:
                self.send_json(400, {"error": "Missing 'url' parameter"})
                return

            url = unquote(url_list[0])

            # Validate URL
            if not url.startswith(("http://", "https://")):
                self.send_json(400, {"error": "Invalid URL scheme"})
                return

            if not is_allowed_url(url):
                self.send_json(403, {"error": "Domain not allowed"})
                return

            # Parse tags
            tags_str = query.get("tags", [""])[0]
            tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []

            # Get optional headers
            ua = self.headers.get("User-Agent") if LOG_UA else None
            ip = self.client_address[0] if LOG_IP else None

            # Log the click
            try:
                log_click(url, tags, ua, ip)
            except Exception as e:
                print(f"[ERROR] Failed to log click: {e}", file=sys.stderr)

            # Redirect
            self.send_response(302)
            self.send_header("Location", url)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return

        # Stats endpoint (optional)
        if path == "/stats":
            try:
                if os.path.exists(LOG_PATH):
                    with open(LOG_PATH, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    self.send_json(200, {"total_clicks": len(lines)})
                else:
                    self.send_json(200, {"total_clicks": 0})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        # Logs endpoint (optional)
        if path == "/logs":
            try:
                limit = int(query.get("limit", ["100"])[0])
                if os.path.exists(LOG_PATH):
                    with open(LOG_PATH, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    entries = [json.loads(line) for line in lines[-limit:]]
                    self.send_json(200, {"logs": entries})
                else:
                    self.send_json(200, {"logs": []})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        # 404 for unknown paths
        self.send_json(404, {"error": "Not found"})

    def do_HEAD(self) -> None:
        """Handle HEAD requests (same as GET but no body)."""
        self.do_GET()


def main():
    print(f"[INFO] Link Tracker starting on port {PORT}")
    print(f"[INFO] Log path: {LOG_PATH}")
    if ALLOWED_DOMAINS:
        print(f"[INFO] Allowed domains: {ALLOWED_DOMAINS}")
    else:
        print("[INFO] All domains allowed")

    server = HTTPServer(("", PORT), TrackerHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
