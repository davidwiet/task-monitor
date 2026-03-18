#!/usr/bin/env python3
import sys, json, os, hashlib
from utils import play_alert, notify, get_state_dir

def main():
    try:
        data = sys.stdin.read()
        if not data.strip():
            print(json.dumps({"decision": "allow"}))
            return
        payload = json.loads(data)
    except Exception:
        print(json.dumps({"decision": "allow"}))
        return

    session_id = payload.get("session_id", "default")
    tool_name = payload.get("tool_name", "")
    tool_input = json.dumps(payload.get("tool_input", {}), sort_keys=True)
    
    # Unique signature for tool repetition tracking
    command_sig = f"{tool_name}:{tool_input}"
    
    state_dir = get_state_dir(session_id)
    history_file = os.path.join(state_dir, "tool_history.json")
    
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
        except Exception:
            pass
            
    occurrence_count = history.count(command_sig)
    
    # Deny if tool signature repeated 3 times total
    if occurrence_count >= 2:
        play_alert("LandingInterrupted")
        notify("Tool Repetition Loop Detected", msg_type="alert")
        if os.path.exists(history_file):
            os.remove(history_file)
        # Deny tool execution
        print(json.dumps({"decision": "deny", "reason": "Tool loop detected."}))
        return

    history.append(command_sig)
    with open(history_file, "w") as f:
        json.dump(history[-10:], f)

    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
