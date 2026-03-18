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
    triggered_by_file = False
    if os.path.exists(start_file):
        try:
            with open(start_file, "r") as f: start_time = float(f.read())
            duration = time.time() - start_time
            triggered_by_file = True
            os.remove(start_file)
        except: pass
    if duration > 3600: duration = 0; triggered_by_file = False
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
        if os.system(f"/usr/bin/afplay '{skill_dir}/assets/LandingInterrupted.mp3' > /dev/null 2>&1") != 0: os.system("say 'Loop Detected' &")
        sys.stderr.write('
[1;31m[TASK-MONITOR][0m [1;31m❯ Response Loop Detected[0m
')
        if os.path.exists(loop_file): os.remove(loop_file)
        print(json.dumps({"continue": False, "stopReason": "Response loop detected."}))
        return
    if triggered_by_file and duration >= 120:
        if os.system(f"/usr/bin/afplay '{skill_dir}/assets/work-complete.mp3' > /dev/null 2>&1") != 0: os.system("say 'Task Complete' &")
        sys.stderr.write(f'
[1;34m[TASK-MONITOR][0m [1m❯ Task Complete ({int(duration)}s)[0m
')
    if current_response:
        history.append(current_response)
        with open(loop_file, "w") as f: json.dump(history[-10:], f)
    print(json.dumps({"continue": True}))
if __name__ == "__main__": main()
