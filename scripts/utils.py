import os, sys, json, time, subprocess, platform

def get_os():
    return platform.system()

def is_terminal_focused():
    """Detects if the current terminal app is frontmost (macOS only)."""
    if get_os() != "Darwin":
        return True # Default to True on Linux/Windows for now
    
    try:
        # Detect active terminal app from environment
        term_app = os.environ.get("TERM_PROGRAM", "Terminal")
        if "vscode" in term_app.lower() or term_app == "Code":
            term_app = "Visual Studio Code"
        elif term_app == "Apple_Terminal":
            term_app = "Terminal"
            
        # AppleScript with a 2-second timeout to prevent blocking
        script = 'tell application "System Events" to get name of first process whose frontmost is true'
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=2.0
        )
        frontmost = result.stdout.strip()
        
        # Match process names (Code and Electron are common for VS Code)
        app_list = [term_app, "Code", "Visual Studio Code", "Electron", "iTerm2", "Terminal"]
        return any(app.lower() in frontmost.lower() for app in app_list)
    except Exception:
        return True # Fail-safe: assume focused

def get_state_dir(session_id="default"):
    """Returns a session-specific directory for state management."""
    base_dir = os.path.expanduser("~/.gemini/tmp/task-monitor")
    session_dir = os.path.join(base_dir, session_id)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir

def get_asset_path(sound_name):
    """Locates audio assets relative to the script location."""
    # Assume we are in task-monitor/scripts/
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    ext_root = os.path.dirname(scripts_dir)
    return os.path.join(ext_root, "assets", f"{sound_name}.mp3")

def notify(message, msg_type="info"):
    """Standardized color-coded notification on stderr."""
    colors = {
        "info": "34",    # Blue
        "alert": "31",   # Red
        "warning": "33", # Yellow
        "success": "32"  # Green
    }
    color = colors.get(msg_type, "34")
    sys.stderr.write(f"\n\033[1;{color}m[TASK-MONITOR]\033[0m \033[1m❯ {message}\033[0m\n")
    sys.stderr.flush()

def play_alert(sound_name):
    """Plays an alert sound with platform-appropriate tools."""
    asset_path = get_asset_path(sound_name)

    if get_os() == "Darwin":
        if os.path.exists(asset_path):
            # afplay in background
            import time; subprocess.Popen(["afplay", asset_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.1)
        else:
            # Fallback to system voice if asset missing
            subprocess.Popen(["say", sound_name.replace("-", " ")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif get_os() == "Windows":
        if os.path.exists(asset_path):
            # Use PowerShell to play the MP3 on Windows
            ps_command = f"(New-Object Media.MediaPlayer).Open('{asset_path}'); (New-Object Media.MediaPlayer).Play(); Start-Sleep -s 2"
            subprocess.Popen(["powershell", "-c", ps_command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # Simple beep if asset is missing
            subprocess.Popen(["powershell", "-c", "[System.Console]::Beep(440, 500)"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif get_os() == "Linux":
        # Attempt paplay (PulseAudio) or aplay (ALSA)
        if os.path.exists(asset_path):
            subprocess.Popen(["paplay", asset_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_start_time(session_id):
    """Retrieves start time from session-isolated file."""
    start_file = os.path.join(get_state_dir(session_id), "start_time")
    if os.path.exists(start_file):
        try:
            with open(start_file, "r") as f:
                return float(f.read())
        except Exception:
            return None
    return None

def clear_start_time(session_id):
    """Clears start time to prevent re-triggering."""
    start_file = os.path.join(get_state_dir(session_id), "start_time")
    if os.path.exists(start_file):
        try:
            os.remove(start_file)
        except Exception:
            pass
