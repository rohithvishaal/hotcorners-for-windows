# Hot Corners for Windows

A lightweight, always-on-top utility that triggers actions when your mouse cursor reaches the corners of your screen. Similar to Mac's Hot Corners feature, this brings that convenience to Windows.

## Screenshots
![Hot Corners for Windows — Main UI screenshot](screenshots\main_ui.png)
![Action Center](screenshots\action_center.png)
- runs in background, no clutter - can be enabled, disabled and terminated all from here itself.
## Features

- **4 Configurable Corners** — Set different actions for each screen corner (top-left, top-right, bottom-left, bottom-right)
- **Multi Monitor Aware** - actions are trigerred only in particular monitor space
- **Rich Action Library** — 12+ built-in actions including:
  - Show Desktop (Win + D)
  - Lock Screen
  - Task View / All Windows (Win + Tab)
  - Open Task Manager
  - Open Start Menu
  - Action Center (Win + A)
  - File Explorer
  - Sleep
  - Screen Saver
  - Custom Commands (run any executable or script)
  - Launch App (browse & pick installed applications)
  - Nothing (disabled)
- **Customizable Triggers** — Adjust dwell time (50–2000 ms) and corner size (1–60 px)
- **System Tray Integration** — Minimize to tray, quick enable/disable toggle
- **Dark Modern UI** — Beautiful, responsive interface with real-time preview
- **Zero Dependencies** — Uses only Python standard library + tkinter
- **DPI-Aware** — Scales correctly on high-DPI displays
- **Standalone executable** - ~9 MB

## System Requirements

- **Windows 7 or later** (tested on Windows 10 & 11)
- **Python 3.8+** (with tkinter — usually included)
- **Admin privileges** (for some actions like Lock Screen & Sleep but for general stuff it is not needed)

## Installation

### Option 1: Run from Source

1. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/)  
   ⚠️ Check "Add Python to PATH" during installation

2. **Clone or download the repository:**
   ```bash
   git clone https://github.com/rohithvishaal/hotcorners-for-windows.git
   cd hotcorners-for-windows
   ```

3. **Run the application:**
   ```bash
   python hot_corners.py
   ```

### Option 2: Build as Standalone Executable

Use **PyInstaller** to create a single `.exe` file that requires no Python installation.

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   pyinstaller ^
    --onefile ^
    --windowed ^
    --name HotCorners ^
    --icon=icon.ico ^
    --distpath dist ^
    --workpath build_tmp ^
    --specpath . ^
    --exclude-module _bootlocale ^
    --exclude-module lib2to3 ^
    --exclude-module email ^
    --exclude-module html ^
    --exclude-module http ^
    --exclude-module unittest ^
    --exclude-module xml ^
    --exclude-module xmlrpc ^
    --exclude-module pydoc ^
    --exclude-module doctest ^
    --exclude-module difflib ^
    --exclude-module optparse ^
    --exclude-module curses ^
    --exclude-module numpy ^
    --exclude-module scipy ^
    --exclude-module pandas ^
    --exclude-module matplotlib ^
    hot_corners.py
   ```

**Optional:** Create a desktop shortcut or add to Windows Startup folder for auto-launch.

### Option 3: Pre-built Release

Download a ready-made `.exe` from the Releases page — no Python needed!

## Usage

### First Launch

1. **Open the application** — The main settings window appears
2. **Select a corner** — Click one of the four corner buttons (Top-Left, Top-Right, Bottom-Left, Bottom-Right) or the interactive preview on the left
3. **Choose an action** — Select from the dropdown menu
4. **Configure if needed** — For "Custom Command" or "Launch App", enter the command/path
5. **Adjust global settings** — Fine-tune dwell time and corner size at the bottom of the panel
6. **Save & Apply** — Click the "Save & Apply" button; changes take effect immediately

### Using Actions

#### Built-in Actions
- **Show Desktop** — Minimizes all windows (Win + D)
- **Lock Screen** — Immediately locks your Windows session
- **Task View** — Shows all open windows (Win + Tab)
- **Task Manager** — Opens Windows Task Manager
- **Start Menu** — Opens the Windows Start Menu
- **Action Center** — Opens the notification panel (Win + A)
- **File Explorer** — Opens a new File Explorer window
- **Sleep** — Puts your PC to sleep (no admin elevation needed)
- **Screen Saver** — Activates the screen saver immediately
- **Nothing** — This corner does nothing

#### Custom Command
Run any executable, batch script, or PowerShell command. Examples:
- `notepad.exe` — Open Notepad
- `C:\Program Files\VLC\vlc.exe` — Open VLC media player
- `powershell -Command "Get-Date"` — Run a PowerShell snippet
- `shutdown -s -t 60` — Shutdown in 60 seconds

#### Launch App
Opens a dialog to browse and pick any installed application. The app picker scans:
- Program Files & Program Files (x86)
- Common Windows system utilities (Paint, Calculator, Notepad, etc.)
- Your local application directory
- Supports search filtering and manual file browse

### Settings

#### Dwell Time (50–2000 ms)
How long your cursor must stay in a corner **before** the action triggers. Default: **400 ms** (0.4 seconds)

#### Corner Size (1–60 px)
The pixel radius from the screen edge that counts as a "corner". Default: **8 px**  
Larger values = easier to hit, smaller values = more precise

#### Enable/Disable
Toggle hot corners on/off without losing your configuration. Use the toggle in the header or right-click the tray icon.

### Tray Icon

In the system tray (bottom-right of taskbar):
- **Left-click** — Show/restore the settings window
- **Right-click** — Quick menu with Enable/Disable, Open, and Exit options
- **Tooltip** — Shows current status (Enabled / Disabled)

### Configuration File

All settings are saved to:
```
C:\Users\[YourUsername]\.hot_corners_config.json
```

You can edit this file directly (with the app closed) or use the UI. Example:
```json
{
  "top_left": {
    "action": "Show Desktop",
    "custom_cmd": ""
  },
  "top_right": {
    "action": "Task View / All Windows",
    "custom_cmd": ""
  },
  "bottom_left": {
    "action": "Launch App",
    "custom_cmd": "C:\\Program Files\\VLC\\vlc.exe"
  },
  "bottom_right": {
    "action": "Nothing",
    "custom_cmd": ""
  },
  "dwell_ms": 400,
  "corner_px": 8,
  "enabled": true
}
```

## Development / Building on Your Machine

### Prerequisites

- Python 3.8+ with pip
- Git (optional, for cloning)
- PyInstaller (if building .exe)

### Setup Development Environment

```shell
# Clone the repository
git clone https://github.com/rohithvishaal/hotcorners-for-windows.git
cd hotcorners-for-windows

# (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate

# Install development dependencies
# Only if you want to build .exe
pip install pyinstaller  
pip install nuikta

# use the build.bat if required, it does everything for you
.\build.bat
# try both pyinstaller and nuikta for build sizes
```

### File Structure

```
.gitignore
build.bat
hot_corners.py
icon.ico
README.md
```

### Building the Executable
```
# after the activating the env
venv\Scripts\activate
.\build.bat
```
### Creating an Icon

To create a proper `.ico` file from a PNG:

1. Use an online converter (e.g., [convertio.co](https://convertio.co/png-ico/)) or
2. Use Python + Pillow:
   ```bash
   pip install pillow
   python -c "from PIL import Image; Image.open('icon.png').save('icon.ico')"
   ```

### Code Structure Overview

- **Win32 API Bindings** — Low-level mouse tracking and system actions via `ctypes`
- **HotCornerDaemon** — Background thread monitoring cursor position
- **AppPickerDialog** — Modal window for browsing installed applications
- **HotCornersApp** — Main GUI built with tkinter
- **Embedded Assets** — Base64-encoded PNG icons (no external files needed at runtime)

### Modifying the Code

Want to add a new action? Edit the `ACTIONS` dictionary and `execute_action()` function:

```python
ACTIONS = {
    # ...existing...
    "My New Action": "my_action",
}

def execute_action(key, custom_cmd=""):
    # ...existing...
    elif key == "my_action":
        # Your code here
        pass
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tkinter'"
**Solution:** Install tkinter separately:
```bash
# Windows
pip install tk

# Or install Python 3.8+ and ensure tcl/tk is included
```

### Issue: Cursor tracking doesn't work / actions don't trigger
- Ensure the app is **enabled** (check the status toggle)
- Try increasing the **dwell time** (some systems need longer)
- Check if the corner zone is visible in the preview
- Make sure the app has **focus** at least once after startup

### Issue: "Access Denied" when trying to lock screen or sleep
- The app may need **admin privileges** if you are locked down for these actions
- Right-click `HotCorners.exe` → "Run as administrator"
- Or create a shortcut with admin mode enabled

### Issue: High CPU usage
- This is usually the cursor tracking loop running at 50 Hz (every 20 ms)
- To reduce load, edit the `time.sleep(0.02)` line in `HotCornerDaemon.run()` to a higher value
- Default (0.02 seconds) is responsive; increasing to 0.1 will reduce CPU at the cost of slight latency

### Issue: Custom command doesn't run / Launch App fails
- Verify the **full path** to the executable is correct
- Use forward slashes `/` or double backslashes `\\` in paths
- For scripts (`.bat`, `.ps1`), ensure they're executable
- Test the command manually in Command Prompt first

### Issue: Settings don't persist on restart
- Check that `C:\Users\[YourUsername]\.hot_corners_config.json` exists and is readable
- Ensure you clicked **"Save & Apply"** before closing the app
- If the file is corrupted, delete it and restart the app (it will regenerate defaults)

## Performance

- **CPU Usage** — ~0.1–0.3% at idle (cursor tracking only)
- **Memory** — ~10-17 MB (tkinter + Python runtime)
- **Startup Time** — <1 second on modern hardware

On older machines, you can reduce the tracking frequency by editing the daemon sleep interval in the source code.

## Known Limitations

- **Single-monitor focus** — Currently designed for primary monitor; multi-monitor support planned
- **Gesture/Swipe detection** — Only cursor position, not velocity
- **Accessibility** — No keyboard-only mode yet
- **Third-party apps** — Some full-screen games may bypass corner detection

## Security & Privacy

- **Fully offline** — No internet connection required
- **No telemetry** — Nothing is sent anywhere
- **Open source** — Inspect the code yourself
- **Config is local** — Stored in `C:\Users\[YourUsername]\.hot_corners_config.json` on your machine

## License

MIT License — See LICENSE file for details

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Submit a Pull Request

## Support & Feedback

- **Issues** — Report bugs on GitHub Issues
- **Feature Requests** — Use GitHub Discussions
- **Questions** — Check existing issues first

## Roadmap

- [ ] Multi-monitor support
- [ ] Custom hotkey triggers (not just corners)
- [ ] Action scheduling / time-based triggers
- [ ] Gesture detection (swipe velocity)
- [ ] More built-in actions (brightness, volume, etc.)
- [ ] Dark/Light theme toggle

## Changelog

### v4.0
- Rewritten UI with modern dark theme
- App picker dialog with app scanning
- System tray integration
- Improved DPI awareness
- Support for custom commands and launch app

### v3.0 & Earlier
- Basic corner detection
- Standard action set

---

**Made with ❤️ for Windows power users who miss their Mac and Linux**