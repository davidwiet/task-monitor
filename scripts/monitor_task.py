#!/usr/bin/env python3
import sys, json, os, time
def main():
    try:
        data = sys.stdin.read()
        if not data.strip(): print(json.dumps({"continue": True})); return
        payload = json.loads(data)
    except: print(json.dumps({"continue": True})); return
    session_id = payload.get("session_id", "default")
    current_response = payload.get("prompt_response", "").strip()
    start_file = os.path.expanduser("~/.gemini/tmp/task_start_time")
    duration = 0
    if os.path.exists(start_file):
        try:
            with open(start_file, "r") as f: start_time = float(f.read())
            duration = time.time() - start_time
            os.remove(start_file)
        except: pass
    loop_file = os.path.expanduser(f"~/.gemini/tmp/loop_detection/{session_id}_responses.json")
    os.makedirs(os.path.dirname(loop_file), exist_ok=True)
    history = []
    if os.path.exists(loop_file):
        try:
            with open(loop_file, "r") as f: history = json.load(f)
        except: pass
    occurrence_count = history.count(current_response)
    skill_dir = "/Users/david/.gemini/skills/task-monitor"
    if current_response and occurrence_count >= 2:
        os.system(f"afplay '{skill_dir}/assets/LandingInterrupted.mp3' &")
        os.system("say 'Loop Detected' &")
        sys.stderr.write('\n\033[1;31m[TASK-MONITOR]\033[0m \033[1;31m❯ Response Loop Detected\033[0m\n')
        if os.path.exists(loop_file): os.remove(loop_file)
        print(json.dumps({"continue": False, "stopReason": "Response loop detected."}))
        return
    if duration >= 120:
        os.system(f"afplay '{skill_dir}/assets/work-complete.mp3' &")
        os.system("say 'Task Complete' &")
        sys.stderr.write(f'\n\033[1;34m[TASK-MONITOR]\033[0m \033[1m❯ Task Complete ({int(duration)}s)\033[0m\n')
    if current_response:
        history.append(current_response)
        with open(loop_file, "w") as f: json.dump(history[-10:], f)
    print(json.dumps({"continue": True}))
if __name__ == "__main__": main()
