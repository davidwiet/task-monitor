#!/usr/bin/env python3
import sys, json, os, time
from utils import get_state_dir

def main():
    try:
        # Standard Hook Input: session_id is provided in the hook payload
        data = sys.stdin.read()
        if not data.strip():
            session_id = "default"
        else:
            payload = json.loads(data)
            session_id = payload.get("session_id", "default")
    except Exception:
        session_id = "default"
        
    # Record current time to session-specific start_time file
    session_dir = get_state_dir(session_id)
    start_file = os.path.join(session_dir, "start_time")
    
    with open(start_file, "w") as f:
        f.write(str(time.time()))
    
    # Standard Hook Output: Silent success
    print("{}")

if __name__ == "__main__":
    main()
