#!/bin/bash

EVENT="/dev/input/event4"
PATTERN="evtest --grab $EVENT"

if pgrep -f "$PATTERN" > /dev/null; then
    sudo pkill -f "$PATTERN"
    echo "Keyboard ENABLED."
else
    sudo evtest --grab "$EVENT" > /dev/null 2>&1 &
    echo "Keyboard DISABLED."
fi
