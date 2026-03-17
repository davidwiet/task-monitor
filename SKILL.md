---
name: task-monitor
description: Monitors Gemini CLI sessions for duration, repetition, and focus. Use when starting autonomous coding, research, or long-running tasks to ensure loops are prevented and user is notified of completion.
---

# Task Monitor

A specialized operational skill designed to maintain system integrity and user focus during autonomous agentic sessions. It provides auditory and visual feedback for task status and safety-critical events.

## Features

### 1. Loop Prevention (`AfterAgent` Hook)
Automatically detects and halts the agent if it repeats the exact same message 3 times within a single turn. 
- **Auditory Alert:** `LandingInterrupted.mp3`
- **Visual Alert:** `[TASK-MONITOR] ❯ Loop Detected`

### 2. Completion Notification (`AfterAgent` Hook)
Plays a success sound if a task takes 120 seconds or longer to complete.
- **Auditory Alert:** `work-complete.mp3`
- **Visual Alert:** `[TASK-MONITOR] ❯ Task Complete (Duration: Xs)`

### 3. Out-of-Focus Alerts (`Notification` Hook)
Triggers a system ping if the agent is blocked by a permission prompt while the terminal window is not in focus.
- **Auditory Alert:** System `Ping.aiff`
- **Visual Alert:** `[TASK-MONITOR] ❯ Attention Required`

## Usage Instructions

This skill is primarily automated via the Gemini CLI hook system. To ensure it is active, verify that your global `~/.gemini/settings.json` points to the scripts within this skill directory.

### Configuration Path Logic
All scripts within this skill use relative path detection to find their bundled assets in the `assets/` folder, ensuring portability.

```bash
# Example AfterAgent registration
"AfterAgent": [
  {
    "name": "task-monitor-loop",
    "type": "command",
    "command": "python3 scripts/detect_loops.py"
  }
]
```

### Visual Theme
The skill employs ANSI escape codes for high-visibility terminal logging:
- `[TASK-MONITOR]` (Blue): Status Info
- `[TASK-MONITOR]` (Red): Safety/Loop Alert
- `[TASK-MONITOR]` (Yellow): User Attention Required

## Testing
To test the loop prevention:
1. Ask the agent to repeat the word "Test" in 3 separate responses within a single turn.
2. The agent should halt, play the interruption sound, and display the red alert header.
