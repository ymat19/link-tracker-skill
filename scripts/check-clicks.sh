#!/bin/bash
# Check for new clicks and notify agent

# mise環境のPATH
export PATH="$HOME/.local/share/mise/installs/node/24.13.0/bin:$PATH"

LOG_FILE="$HOME/repos/link-tracker-skill/skill/data/clicks.jsonl"
STATE_FILE="$HOME/repos/link-tracker-skill/scripts/.last_line_count"

# Initialize state file if not exists
if [ ! -f "$STATE_FILE" ]; then
    echo "0" > "$STATE_FILE"
fi

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    exit 0
fi

# Get current and previous line counts
CURRENT_COUNT=$(wc -l < "$LOG_FILE")
LAST_COUNT=$(cat "$STATE_FILE")

# If new lines exist
if [ "$CURRENT_COUNT" -gt "$LAST_COUNT" ]; then
    # Get new entries
    NEW_LINES=$((CURRENT_COUNT - LAST_COUNT))
    NEW_ENTRIES=$(tail -n "$NEW_LINES" "$LOG_FILE")
    
    # Update state
    echo "$CURRENT_COUNT" > "$STATE_FILE"
    
    # Send system event to agent
    openclaw system event --text "【クリック検知】新しいクリックがあったにゃ！このリポジトリを解説して：
$NEW_ENTRIES" --mode now
fi
