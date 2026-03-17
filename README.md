# 🛡️ Task Monitor (for Gemini CLI)

A specialized operational skill for the [Gemini CLI](https://geminicli.com) that provides automated auditory and visual feedback for task status, focus, and safety-critical events.

## 🎧 Features

### 1. **"Work Complete!"** (Long-Task Notifications)
Plays the iconic *Warcraft III* "Work complete!" sound when a task takes **120 seconds or longer** to finish.
- **Why?** So you can walk away from your terminal during deep research or complex coding tasks without "babysitting" the progress bar.

### 2. **Repetition Guard** (Loop Prevention)
Detects when the AI gets stuck in a "Broken Record" loop (repeating the exact same message 3 times in a single turn).
- **Action:** Halts the agent immediately.
- **Sound:** Plays `LandingInterrupted.mp3`.
- **Theme:** Displays a high-visibility **[TASK-MONITOR] ❯ Loop Detected** red alert.

### 3. **Focus Alerts** (Out-of-Focus Prompting)
Triggers a system "Ping" if the agent is blocked by a permission prompt while your terminal window is **not in focus**.
- **Why?** Prevents the agent from sitting idle for hours just because you switched to another tab and didn't see the "Approve? (y/n)" prompt.

## 🎨 Visual Theme
The skill provides a color-coded "System Console" experience:
- 🔵 **Blue:** Successful completion info.
- 🔴 **Red:** Critical safety alerts (loops).
- 🟡 **Yellow:** User attention required.

## 🚀 Installation

1. **Install the skill:**
   ```bash
   gemini skills install https://github.com/dwietchner/task-monitor
   ```

2. **Reload your session:**
   ```bash
   /skills reload
   ```

3. **Configure your hooks:**
   Add the following to your `~/.gemini/settings.json`:

   ```json
   "hooks": {
     "AfterAgent": [
       {
         "name": "long-task-sound",
         "type": "command",
         "command": "python3 ~/.gemini/skills/task-monitor/scripts/play_long_task_sound.py"
       },
       {
         "name": "loop-preventer",
         "type": "command",
         "command": "python3 ~/.gemini/skills/task-monitor/scripts/detect_loops.py"
       }
     ],
     "Notification": [
       {
         "name": "active-window-notify",
         "type": "command",
         "command": "python3 ~/.gemini/skills/task-monitor/scripts/play_notification_sound.py"
       }
     ]
   }
   ```

---
*Created with 💙 for the Gemini CLI community.*
