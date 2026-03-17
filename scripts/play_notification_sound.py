#!/usr/bin/env python3
import sys
import json
import os

def main():
    try:
        payload_data = sys.stdin.read()
        if not payload_data.strip():
            print("{}")
            return
        payload = json.loads(payload_data)
    except Exception:
        print("{}")
        return

    metadata = payload.get("metadata", {})
    is_active = metadata.get("is_active_window", True)
    
    if not is_active:
        os.system("/usr/bin/afplay /System/Library/Sounds/Ping.aiff > /dev/null 2>&1 &")
        sys.stderr.write(f"\n\033[1;33m[TASK-MONITOR]\033[0m \033[1m❯ Attention Required (Out-of-Focus Prompt)\033[0m\n")

    print("{}")

if __name__ == "__main__":
    main()
