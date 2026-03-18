#!/usr/bin/env python3
import sys, json, os, subprocess
from utils import is_terminal_focused, notify, get_os

def main():
    try:
        data = sys.stdin.read()
        if not data.strip():
            print("{}")
            return
        payload = json.loads(data)
    except Exception:
        print("{}")
        return

    # metadata.is_active_window is provided by the CLI if supported
    metadata = payload.get("metadata", {})
    is_active = metadata.get("is_active_window")
    
    # Fallback to our custom focus detection
    if is_active is None:
        is_active = is_terminal_focused()
        
    if not is_active:
        if get_os() == "Darwin":
            # Standard system ping for macOS
            subprocess.Popen(["afplay", "/System/Library/Sounds/Ping.aiff"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        notify("Attention Required (Gemini is waiting)", msg_type="warning")

    # Hook must return an object (even empty)
    print("{}")

if __name__ == "__main__":
    main()
