#!/usr/bin/env python3
import sys, json, os
def main():
    try:
        data = sys.stdin.read()
        if not data.strip(): print(json.dumps({"decision": "allow"})); return
        payload = json.loads(data)
    except: print(json.dumps({"decision": "allow"})); return
    session_id = payload.get("session_id", "default")
    tool_name = payload.get("tool_name", "")
    tool_input = json.dumps(payload.get("tool_input", {}), sort_keys=True)
    command_sig = f"{tool_name}:{tool_input}"
    loop_file = os.path.expanduser(f"~/.gemini/tmp/loop_detection/{session_id}_tools.json")
    os.makedirs(os.path.dirname(loop_file), exist_ok=True)
    history = []
    if os.path.exists(loop_file):
        try:
            with open(loop_file, "r") as f: history = json.load(f)
        except: pass
    occurrence_count = history.count(command_sig)
    if occurrence_count >= 2:
        skill_dir = "/Users/david/.gemini/skills/task-monitor"
        if os.system(f"/usr/bin/afplay '{skill_dir}/assets/LandingInterrupted.mp3' > /dev/null 2>&1") != 0:
            os.system("say 'Tool Loop Detected' &")
        sys.stderr.write(f'\n\033[1;31m[TASK-MONITOR]\033[0m \033[1;31m❯ Tool Loop Detected\033[0m\n')
        if os.path.exists(loop_file): os.remove(loop_file)
        print(json.dumps({"decision": "deny", "reason": "Tool loop detected."}))
        return
    history.append(command_sig)
    with open(loop_file, "w") as f: json.dump(history[-10:], f)
    print(json.dumps({"decision": "allow"}))
if __name__ == "__main__": main()
