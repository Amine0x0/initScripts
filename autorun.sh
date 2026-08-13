#!/bin/bash

SCRIPT_PATH="$HOME/workspace/initScripts/main.py"
LOCK_FILE="/tmp/initScripts.lock"

if [ ! -f "$LOCK_FILE" ]; then
    touch "$LOCK_FILE"
    echo "Running main.py for this session..."
    python3 "$SCRIPT_PATH"
else
    echo "main.py has already run this session. Skipping."
fi