#!/usr/bin/env python3
import sys
import json
import os

def main():
    try:
        payload_data = sys.stdin.read()
        if not payload_data.strip():
            print(json.dumps({"continue": True}))
            return
        payload = json.loads(payload_data)
    except Exception:
        print(json.dumps({"continue": True}))
        return

    current_response = payload.get("prompt_response", "").strip()
    session_id = payload.get("session_id", "default")
    turn_id = payload.get("turn_id", 0)
    
    if not current_response:
        print(json.dumps({"continue": True}))
        return

    state_dir = os.path.expanduser("~/.gemini/tmp/loop_detection")
    os.makedirs(state_dir, exist_ok=True)
    state_file = os.path.join(state_dir, f"{session_id}_turn_{turn_id}.json")

    history = []
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                history = json.load(f)
        except:
            history = []

    occurrence_count = history.count(current_response)
    
    if occurrence_count >= 2:
        skill_dir = "/Users/david/.gemini/skills/task-monitor"
        asset_path = os.path.join(skill_dir, "assets", "LandingInterrupted.mp3")
        os.system(f"/usr/bin/afplay '{asset_path}' > /dev/null 2>&1 &")
        
        if os.path.exists(state_file):
            os.remove(state_file)
            
        sys.stderr.write(f"\n\033[1;31m[TASK-MONITOR]\033[0m \033[1;31m❯ Loop Detected (Turn {turn_id})\033[0m\n")
        
        print(json.dumps({
            "continue": False,
            "stopReason": f"Turn loop detected: This message has appeared {occurrence_count + 1} times in turn {turn_id}.",
            "systemMessage": f"⚠️ Agent turn halted: Repeated response detected ({occurrence_count + 1} times)."
        }))
        return

    history.append(current_response)
    
    try:
        with open(state_file, "w") as f:
            json.dump(history, f)
    except:
        pass

    print(json.dumps({"continue": True}))

if __name__ == "__main__":
    main()
