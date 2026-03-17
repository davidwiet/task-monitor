#!/usr/bin/env python3
import sys
import json
import os
import glob
from datetime import datetime

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

    session_id = payload.get("session_id", "")
    if not session_id:
        print("{}")
        return

    short_id = session_id.split("-")[0]
    search_pattern = os.path.expanduser(f"~/.gemini/tmp/*/chats/*-{short_id}.json")
    files = glob.glob(search_pattern)
    
    if not files:
        search_pattern = os.path.expanduser(f"~/.gemini/history/*/chats/*-{short_id}.json")
        files = glob.glob(search_pattern)
        if not files:
            print("{}")
            return

    latest_file = sorted(files, key=os.path.getmtime, reverse=True)[0]

    try:
        with open(latest_file, 'r') as f:
            data = json.load(f)
            
        messages = data.get("messages", [])
        if len(messages) >= 2:
            last_gemini = None
            last_user = None
            for msg in reversed(messages):
                if msg.get("type") == "gemini" and last_gemini is None:
                    last_gemini = msg
                elif msg.get("type") == "user" and last_gemini is not None and last_user is None:
                    last_user = msg
                    break
            
            if last_gemini and last_user:
                def parse_time(ts_str):
                    if not ts_str: return None
                    ts_str = ts_str.replace("Z", "+0000")
                    try:
                        return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%f+0000")
                    except ValueError:
                        try:
                            return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S+0000")
                        except ValueError:
                            return None

                t1 = parse_time(last_user.get("timestamp"))
                t2 = parse_time(data.get("lastUpdated")) or parse_time(last_gemini.get("timestamp"))
                
                if t1 and t2:
                    diff = (t2 - t1).total_seconds()
                    if diff >= 120:
                        # Use asset from skill dir
                        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        asset_path = os.path.join(skill_dir, "assets", "work-complete.mp3")
                        os.system(f"afplay '{asset_path}' > /dev/null 2>&1 &")
                        
                        # Visual Theme Output (Blue Header)
                        print(f"\n\033[1;34m[TASK-MONITOR]\033[0m \033[1m❯ Task Complete (Duration: {int(diff)}s)\033[0m")
    except Exception:
        pass

    print("{}")

if __name__ == "__main__":
    main()
