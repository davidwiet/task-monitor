#!/usr/bin/env python3
import os, sys, json, subprocess, time, shutil

# Set up paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
sys.path.append(SCRIPTS_DIR)

def run_script(script_name, input_data):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    process = subprocess.Popen(
        [sys.executable, script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=json.dumps(input_data))
    return stdout, stderr

def test_monitor_task_loop():
    print("Testing monitor_task.py loop detection...")
    session_id = "test_loop_session"
    loop_file = os.path.expanduser(f"~/.gemini/tmp/loop_detection/{session_id}_responses.json")
    if os.path.exists(loop_file): os.remove(loop_file)
    
    payload = {"session_id": session_id, "prompt_response": "Repetitive response content."}
    
    # Run twice
    run_script("monitor_task.py", payload)
    run_script("monitor_task.py", payload)
    
    # Third time should trigger loop
    stdout, stderr = run_script("monitor_task.py", payload)
    result = json.loads(stdout)
    
    assert result["continue"] == False
    assert "Response Loop Detected" in stderr
    print("✅ monitor_task.py loop detection passed.")

def test_monitor_tool_loop():
    print("Testing monitor_tool.py loop detection...")
    session_id = "test_tool_session"
    loop_file = os.path.expanduser(f"~/.gemini/tmp/loop_detection/{session_id}_tools.json")
    if os.path.exists(loop_file): os.remove(loop_file)
    
    payload = {
        "session_id": session_id,
        "tool_name": "test_tool",
        "tool_input": {"arg": 1}
    }
    
    # Run twice
    run_script("monitor_tool.py", payload)
    run_script("monitor_tool.py", payload)
    
    # Third time should trigger loop
    stdout, stderr = run_script("monitor_tool.py", payload)
    result = json.loads(stdout)
    
    assert result["decision"] == "deny"
    assert "Tool Loop Detected" in stderr
    print("✅ monitor_tool.py tool loop detection passed.")

def test_duration_trigger():
    print("Testing monitor_task.py duration trigger...")
    start_file = os.path.expanduser("~/.gemini/tmp/task_start_time")
    # Simulate 130s duration
    with open(start_file, "w") as f:
        f.write(str(time.time() - 130))
    
    payload = {"session_id": "test_duration", "prompt_response": "Some response."}
    
    # Ensure it's not focused to trigger sound
    # (Mocking TERM_PROGRAM to something that won't match)
    env = os.environ.copy()
    env["TERM_PROGRAM"] = "None"
    
    # Run script
    script_path = os.path.join(SCRIPTS_DIR, "monitor_task.py")
    process = subprocess.Popen(
        [sys.executable, script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    stdout, stderr = process.communicate(input=json.dumps(payload))
    
    assert "Task Complete (13" in stderr
    assert not os.path.exists(start_file)
    print("✅ monitor_task.py duration trigger passed.")

def main():
    try:
        test_monitor_task_loop()
        test_monitor_tool_loop()
        test_duration_trigger()
        print("\nAll tests passed successfully! 🎉")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
