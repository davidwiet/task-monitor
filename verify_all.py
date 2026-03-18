#!/usr/bin/env python3
import os, sys, json, subprocess, time, shutil

# Base directory for the extension
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

# Add scripts dir to path for imports
sys.path.append(SCRIPTS_DIR)

def run_script(script_name, payload):
    """Simulates a hook call to a script with a JSON payload."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    process = subprocess.Popen(
        [sys.executable, script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=json.dumps(payload))
    return stdout, stderr

def test_response_loop():
    print("Testing Response Loop Detection...")
    session_id = "test_session_resp_loop"
    payload = {
        "session_id": session_id,
        "prompt_response": "Repetitive AI response."
    }
    
    # 1st time
    run_script("monitor_task.py", payload)
    # 2nd time
    run_script("monitor_task.py", payload)
    # 3rd time (Should halt)
    stdout, stderr = run_script("monitor_task.py", payload)
    
    try:
        result = json.loads(stdout)
        if result.get("continue") is False and "Loop Detected" in stderr:
            print("✅ Response Loop Test Passed")
        else:
            print(f"❌ Response Loop Test Failed: {stdout} | {stderr}")
    except Exception as e:
        print(f"❌ Response Loop Test Error: {e}")

def test_tool_loop():
    print("Testing Tool Loop Detection...")
    session_id = "test_session_tool_loop"
    payload = {
        "session_id": session_id,
        "tool_name": "ls",
        "tool_input": {"path": "."}
    }
    
    # 1st time
    run_script("monitor_tool.py", payload)
    # 2nd time
    run_script("monitor_tool.py", payload)
    # 3rd time (Should deny)
    stdout, stderr = run_script("monitor_tool.py", payload)
    
    try:
        result = json.loads(stdout)
        if result.get("decision") == "deny" and "Tool Repetition" in stderr:
            print("✅ Tool Loop Test Passed")
        else:
            print(f"❌ Tool Loop Test Failed: {stdout} | {stderr}")
    except Exception as e:
        print(f"❌ Tool Loop Test Error: {e}")

def test_duration_alert():
    print("Testing Duration Alert (Focus-Aware)...")
    session_id = "test_session_duration"
    
    # Manually create a start time from 130s ago
    from utils import get_state_dir
    session_dir = get_state_dir(session_id)
    with open(os.path.join(session_dir, "start_time"), "w") as f:
        f.write(str(time.time() - 130))
        
    # Set fake TERM_PROGRAM to simulate away-focus
    os.environ["TERM_PROGRAM"] = "None"
    
    payload = {
        "session_id": session_id,
        "prompt_response": "Finished task after long wait."
    }
    
    stdout, stderr = run_script("monitor_task.py", payload)
    
    if "Task Complete (130s)" in stderr:
        print("✅ Duration Alert Test Passed")
    else:
        print(f"❌ Duration Alert Test Failed: {stderr}")

def main():
    print("Starting Task Monitor Verification Suite...\n")
    test_response_loop()
    test_tool_loop()
    test_duration_alert()
    print("\nVerification Complete.")

if __name__ == "__main__":
    main()
