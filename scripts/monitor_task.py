#!/usr/bin/env python3
import sys, json, os, time
from utils import is_terminal_focused, play_alert, notify, get_start_time, clear_start_time, get_state_dir

def main():
    try:
        data = sys.stdin.read()
        if not data.strip():
            print(json.dumps({"continue": True}))
            return
        payload = json.loads(data)
    except Exception:
        print(json.dumps({"continue": True}))
        return

    session_id = payload.get("session_id", "default")
    current_response = payload.get("prompt_response", "").strip()
    
    # Check Duration
    start_time = get_start_time(session_id)
    # Flexible threshold from settings (default: 120s)
    settings = payload.get("settings", {})
    threshold = settings.get("general", {}).get("longTaskThreshold", 120)
    
    if start_time:
        duration = time.time() - start_time
        if duration >= threshold:
            if not is_terminal_focused():
                play_alert("work-complete")
                notify(f"Task Complete ({int(duration)}s)", msg_type="info")
            else:
                notify(f"Task Complete ({int(duration)}s)", msg_type="success")
            clear_start_time(session_id)

    # Response Loop Prevention (3x repetition)
    loop_dir = get_state_dir(session_id)
    loop_file = os.path.join(loop_dir, "response_history.json")
    
    history = []
    if os.path.exists(loop_file):
        try:
            with open(loop_file, "r") as f:
                history = json.load(f)
        except Exception:
            pass
            
    occurrence_count = history.count(current_response) if current_response else 0
    
    if current_response and occurrence_count >= 2:
        play_alert("LandingInterrupted")
        notify("Response Loop Detected", msg_type="alert")
        if os.path.exists(loop_file):
            os.remove(loop_file)
        # Halt the agent
        print(json.dumps({"continue": False, "stopReason": "Response loop detected."}))
        return

    if current_response:
        history.append(current_response)
        with open(loop_file, "w") as f:
            json.dump(history[-10:], f)

    print(json.dumps({"continue": True}))

if __name__ == "__main__":
    main()
