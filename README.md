# 🛡️ Task Monitor (v2.0.0)

Professional, platform-aware guardrails for the [Gemini CLI](https://geminicli.com) providing automated auditory and visual feedback for task status, focus, and safety-critical events.

## 🎧 Features

### 1. **"Work Complete!"** (Long-Task Notifications)
Plays the iconic *Warcraft III* "Work complete!" sound when a task exceeds the threshold.
- **Why?** So you can walk away from your terminal during deep research or complex coding tasks.
- **Configurable:** By default, this triggers after **120 seconds**. You can customize this threshold in your settings (set to `0` to always trigger when away).
- **Focus-Aware:** Only plays sound if the terminal is **not in focus** (macOS).

### 2. **Repetition & Loop Guard**
Detects when the AI gets stuck in "Broken Record" loops (repeating messages or tool calls).
- **Action:** Halts the agent immediately if a loop is detected (3x repetition).
- **Sound:** Plays `LandingInterrupted.mp3`.
- **Theme:** Displays a high-visibility **[TASK-MONITOR] ❯ Loop Detected** red alert.

### 3. **Focus Alerts** (Out-of-Focus Prompting)
Triggers a system "Ping" if the agent is blocked by a permission prompt while your terminal window is **not in focus**.
- **Why?** Prevents the agent from sitting idle because you switched tabs.

## ⚙️ Configuration
You can customize the extension's behavior in `gemini-extension.json` or through your user settings:

```json
"settings": {
  "general": {
    "longTaskThreshold": 120, // Seconds before "Work Complete!" sounds
    "maxTurns": 15
  }
}
```

## 🎨 Visual Theme
The extension provides a color-coded "System Console" experience:
- 🔵 **Blue:** Task completion notifications.
- 🔴 **Red:** Critical safety alerts (loops).
- 🟡 **Yellow:** User attention required.
- 🟢 **Green:** Status updates when in-focus.

## 🚀 Installation & Configuration

1. **Install the extension:**
   ```bash
   gemini extensions link /path/to/task-monitor
   ```

2. **Configure your hooks:**
   The extension uses the following hooks in `gemini-extension.json`:
   - `BeforeAgent`: Records task start time.
   - `AfterAgent`: Monitors for loops and completion.
   - `BeforeTool`: Guards against tool loops.
   - `Notification`: Alerts for attention when away.

## 🌍 Platform Support
- **macOS:** Full support for AppleScript-based terminal focus detection and `afplay` audio.
- **Windows:** High-accuracy loop detection and native PowerShell-based audio.
- **Linux:** Universal loop detection and `paplay`/`aplay` audio fallback.

---
*Created with 💙 for the Gemini CLI community.*
