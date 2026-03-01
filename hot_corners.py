"""
Hot Corners for Windows  v4.0
Requirements : Python 3.8+, standard library only.
Run          : python hot_corners.py
"""

import ctypes
import ctypes.wintypes
import json
import os
import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

# ── Embedded icon (base64 PNG) — no external file needed at runtime ───────────
import base64 as _b64

_ICON_B64_32 = "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"
_ICON_B64_24 = "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"

# --- Win32 constants ---
NIM_ADD = 0x00000000
NIM_MODIFY = 0x00000001
NIM_DELETE = 0x00000002

NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004

WM_USER = 0x0400
WM_TRAYICON = WM_USER + 1

WM_LBUTTONUP = 0x0202
WM_RBUTTONUP = 0x0205

GWL_WNDPROC = -4
WM_DESTROY = 0x0002

MF_STRING = 0x00000000
MF_SEPARATOR = 0x00000800
MF_CHECKED = 0x00000008
MF_UNCHECKED = 0x00000000

# Proper LRESULT (32/64-bit safe)
if ctypes.sizeof(ctypes.c_void_p) == 8:
    LRESULT = ctypes.c_longlong
else:
    LRESULT = ctypes.c_long

if ctypes.sizeof(ctypes.c_void_p) == 8:
    UINT_PTR = ctypes.c_ulonglong
else:
    UINT_PTR = ctypes.c_uint

user32 = ctypes.windll.user32
shell32 = ctypes.windll.shell32

user32.SetWindowLongPtrW.restype = ctypes.c_void_p
user32.SetWindowLongPtrW.argtypes = [
    ctypes.wintypes.HWND,
    ctypes.c_int,
    ctypes.c_void_p,
]

user32.CallWindowProcW.restype = LRESULT
user32.CallWindowProcW.argtypes = [
    ctypes.c_void_p,
    ctypes.wintypes.HWND,
    ctypes.wintypes.UINT,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM,
]

user32.AppendMenuW.restype = ctypes.wintypes.BOOL
user32.AppendMenuW.argtypes = [
    ctypes.wintypes.HMENU,
    ctypes.wintypes.UINT,
    UINT_PTR,
    ctypes.wintypes.LPCWSTR,
]

user32.CreatePopupMenu.restype = ctypes.wintypes.HMENU
user32.CreatePopupMenu.argtypes = []

user32.TrackPopupMenu.restype = ctypes.wintypes.UINT
user32.TrackPopupMenu.argtypes = [
    ctypes.wintypes.HMENU,
    ctypes.wintypes.UINT,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.wintypes.HWND,
    ctypes.c_void_p,
]


class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.wintypes.DWORD),
        ("hWnd", ctypes.wintypes.HWND),
        ("uID", ctypes.wintypes.UINT),
        ("uFlags", ctypes.wintypes.UINT),
        ("uCallbackMessage", ctypes.wintypes.UINT),
        ("hIcon", ctypes.wintypes.HICON),
        ("szTip", ctypes.wintypes.WCHAR * 128),
    ]


def hicon_from_base64_png(b64_data):
    import base64

    icon_bytes = base64.b64decode(b64_data)
    size = len(icon_bytes)

    buffer = ctypes.create_string_buffer(icon_bytes)

    CreateIconFromResourceEx = ctypes.windll.user32.CreateIconFromResourceEx
    CreateIconFromResourceEx.restype = ctypes.wintypes.HICON
    CreateIconFromResourceEx.argtypes = [
        ctypes.c_void_p,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.BOOL,
        ctypes.wintypes.DWORD,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.wintypes.UINT,
    ]

    LR_DEFAULTCOLOR = 0x0000
    ICON_VERSION = 0x00030000

    return CreateIconFromResourceEx(
        buffer,
        size,
        True,
        ICON_VERSION,
        32,
        32,
        LR_DEFAULTCOLOR,
    )


# ── DPI awareness ─────────────────────────────────────────────────────────────
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# =============================================================================
#  Helpers
# =============================================================================


def _screen_size():
    return (
        ctypes.windll.user32.GetSystemMetrics(0),
        ctypes.windll.user32.GetSystemMetrics(1),
    )


def _dpi_scale():
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
        ctypes.windll.user32.ReleaseDC(0, hdc)
        return dpi / 96.0
    except Exception:
        return 1.0


# =============================================================================
#  Config
# =============================================================================

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".hot_corners_config.json")

ACTIONS = {
    "Nothing": None,
    "Show Desktop": "show_desktop",
    "Lock Screen": "lock_screen",
    "Task View / All Windows": "task_view",
    "Open Task Manager": "task_manager",
    "Open Start Menu": "start_menu",
    "Open Action Center": "action_center",
    "Open File Explorer": "file_explorer",
    "Sleep": "sleep",
    "Screen Saver": "screen_saver",
    "Custom Command": "custom",
    "Launch App": "launch_app",
}

CORNERS = ["top_left", "top_right", "bottom_left", "bottom_right"]
CORNER_LABEL = {
    "top_left": "Top-Left",
    "top_right": "Top-Right",
    "bottom_left": "Bottom-Left",
    "bottom_right": "Bottom-Right",
}
CORNER_ICON = {  # unicode glyphs shown on the preview canvas
    "top_left": "↖",
    "top_right": "↗",
    "bottom_left": "↙",
    "bottom_right": "↘",
}

_DEFAULT = {
    "top_left": {"action": "Nothing", "custom_cmd": ""},
    "top_right": {"action": "Nothing", "custom_cmd": ""},
    "bottom_left": {"action": "Show Desktop", "custom_cmd": ""},
    "bottom_right": {"action": "Nothing", "custom_cmd": ""},
    "dwell_ms": 400,
    "corner_px": 8,
    "enabled": True,
}


def _fresh():
    return {k: (dict(v) if isinstance(v, dict) else v) for k, v in _DEFAULT.items()}


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                saved = json.load(f)
            cfg = _fresh()
            for k, v in saved.items():
                if k in CORNERS and isinstance(v, dict):
                    cfg[k].update(v)
                else:
                    cfg[k] = v
            return cfg
        except Exception:
            pass
    return _fresh()


def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"[HotCorners] save error: {e}")


# =============================================================================
#  Actions
# =============================================================================

_ke = ctypes.windll.user32.keybd_event
_ke.argtypes = [ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ulong, ctypes.c_ulong]
KEYEVENTF_KEYUP = 0x0002


def _press(*vks):
    for vk in vks:
        _ke(vk, 0, 0, 0)
    for vk in reversed(vks):
        _ke(vk, 0, KEYEVENTF_KEYUP, 0)


VK_LWIN, VK_D, VK_TAB, VK_A = 0x5B, 0x44, 0x09, 0x41


def execute_action(key, custom_cmd=""):
    try:
        if key == "show_desktop":
            _press(VK_LWIN, VK_D)
        elif key == "lock_screen":
            ctypes.windll.user32.LockWorkStation()
        elif key == "task_view":
            _press(VK_LWIN, VK_TAB)
        elif key == "task_manager":
            subprocess.Popen(["taskmgr.exe"], creationflags=subprocess.CREATE_NO_WINDOW)
        elif key == "start_menu":
            _press(VK_LWIN)
        elif key == "action_center":
            _press(VK_LWIN, VK_A)
        elif key == "file_explorer":
            subprocess.Popen(
                ["explorer.exe"], creationflags=subprocess.CREATE_NO_WINDOW
            )
        elif key == "sleep":
            subprocess.Popen(
                [
                    "powershell",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    "Add-Type -Assembly System.Windows.Forms;"
                    "[System.Windows.Forms.Application]::SetSuspendState('Suspend',$false,$false)",
                ],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        elif key == "screen_saver":
            ctypes.windll.user32.PostMessageW(0xFFFF, 0x0112, 0xF140, 0)
        elif key == "custom":
            cmd = (custom_cmd or "").strip()
            if cmd:
                subprocess.Popen(cmd, shell=True)
        elif key == "launch_app":
            path = (custom_cmd or "").strip()
            if path and os.path.exists(path):
                subprocess.Popen(f'start "" "{path}"', shell=True)
    except Exception as e:
        print(f"[HotCorners] '{key}' failed: {e}")


# =============================================================================
#  Daemon
# =============================================================================


class HotCornerDaemon(threading.Thread):
    def __init__(self, cfg):
        super().__init__(daemon=True, name="HotCornerDaemon")
        self._cfg = cfg
        self._active = None
        self._since = None
        self._fired = False

    def _cursor(self):
        pt = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y


    def run(self):

        MONITOR_DEFAULTTONEAREST = 2

        class MONITORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.wintypes.DWORD),
                ("rcMonitor", ctypes.wintypes.RECT),
                ("rcWork", ctypes.wintypes.RECT),
                ("dwFlags", ctypes.wintypes.DWORD),
            ]

        while True:
            now = time.monotonic()

            if not self._cfg.get("enabled", True):
                self._active = None
                self._fired = False
                time.sleep(0.1)
                continue

            px = max(1, int(self._cfg.get("corner_px", 8)))
            dwell = max(0.05, self._cfg.get("dwell_ms", 400) / 1000.0)

            cx, cy = self._cursor()

            # ---- Get monitor under cursor ----
            pt = ctypes.wintypes.POINT(cx, cy)
            hmon = ctypes.windll.user32.MonitorFromPoint(
                pt,
                MONITOR_DEFAULTTONEAREST
            )

            mi = MONITORINFO()
            mi.cbSize = ctypes.sizeof(MONITORINFO)

            ctypes.windll.user32.GetMonitorInfoW(
                hmon,
                ctypes.byref(mi)
            )

            left = mi.rcMonitor.left
            top = mi.rcMonitor.top
            right = mi.rcMonitor.right
            bottom = mi.rcMonitor.bottom

            # ---- Per-monitor corner detection ----
            corner = None

            if cx <= left + px and cy <= top + px:
                corner = "top_left"
            elif cx >= right - px and cy <= top + px:
                corner = "top_right"
            elif cx <= left + px and cy >= bottom - px:
                corner = "bottom_left"
            elif cx >= right - px and cy >= bottom - px:
                corner = "bottom_right"

            # ---- Dwell logic (unchanged behavior) ----
            if corner != self._active:
                self._active = corner
                self._since = now if corner else None
                self._fired = False

            elif corner and not self._fired and now - self._since >= dwell:
                self._fired = True
                c = self._cfg.get(corner, {})
                k = ACTIONS.get(c.get("action", "Nothing"))
                if k:
                    execute_action(k, c.get("custom_cmd", ""))

            time.sleep(0.02)


# =============================================================================
#  GUI
# =============================================================================

PLACEHOLDER = "command or path…"

# =============================================================================
#  App Picker Dialog
# =============================================================================


class AppPickerDialog(tk.Toplevel):
    """
    Popup window that lets the user pick an installed application.
    Scans common Windows install locations for .exe files, shows them
    with name + path, supports search filtering, and has a Browse button
    for anything not in the list.
    """

    # Common locations to scan (fast — only top-level or one level deep)
    _SCAN_DIRS = [
        os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files")),
        os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs"),
        os.path.join(
            os.environ.get("APPDATA", ""), "Microsoft\\Windows\\Start Menu\\Programs"
        ),
        os.path.join(
            os.environ.get("ProgramData", ""),
            "Microsoft\\Windows\\Start Menu\\Programs",
        ),
        "C:\\Windows\\System32",
    ]

    def __init__(self, parent, initial_path="", callback=None):
        super().__init__(parent)
        self.title("Choose an Application")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(520, 480)
        self.grab_set()  # modal
        self.focus_set()

        self._callback = callback
        self._result = initial_path
        self._all_apps = []  # list of (display_name, exe_path)
        self._filtered = []

        # Scale from parent
        self._sc = parent._sc if hasattr(parent, "_sc") else 1.0

        self._build_ui()
        self._center(parent)

        # Scan in background so dialog appears immediately
        t = threading.Thread(target=self._scan_apps, daemon=True)
        t.start()

    def _p(self, v):
        return max(1, round(v * self._sc))

    def _f(self, v):
        return max(7, round(v * self._sc))

    def _center(self, parent):
        self.update_idletasks()

        # parent is already a Tk window
        pw = parent.winfo_x() + parent.winfo_width() // 2
        ph = parent.winfo_y() + parent.winfo_height() // 2

        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()

        self.geometry(f"{w}x{h}+{pw - w // 2}+{ph - h // 2}")

    def _build_ui(self):
        pad = self._p(16)

        # ── Header ────────────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=SURF, highlightbackground=BORDER, highlightthickness=1)
        hdr.pack(fill="x")
        tk.Label(
            hdr,
            text="Choose Application",
            font=("Segoe UI", self._f(12), "bold"),
            bg=SURF,
            fg=TEXT,
        ).pack(side="left", padx=pad, pady=self._p(12))

        # ── Search bar ────────────────────────────────────────────────────────
        sf = tk.Frame(self, bg=BG)
        sf.pack(fill="x", padx=pad, pady=(self._p(12), self._p(6)))

        tk.Label(sf, text="🔍", font=("Segoe UI", self._f(10)), bg=BG, fg=SUBTLE).pack(
            side="left", padx=(0, self._p(6))
        )

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._filter())

        search = tk.Entry(
            sf,
            textvariable=self._search_var,
            font=("Segoe UI", self._f(10)),
            bg=SURF2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            bd=self._p(6),
        )
        search.pack(fill="x", expand=True)
        search.focus_set()

        # ── Status label (shows scanning / count) ─────────────────────────────
        self._status_var = tk.StringVar(value="Scanning installed apps…")
        tk.Label(
            self,
            textvariable=self._status_var,
            font=("Segoe UI", self._f(8)),
            bg=BG,
            fg=SUBTLE,
        ).pack(anchor="w", padx=pad)

        # ── App list ──────────────────────────────────────────────────────────
        list_frame = tk.Frame(self, bg=BG)
        list_frame.pack(fill="both", expand=True, padx=pad, pady=self._p(6))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        self._listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", self._f(9)),
            bg=SURF2,
            fg=TEXT,
            selectbackground=ACCENT,
            selectforeground="#fff",
            activestyle="none",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self._listbox.grid(row=0, column=0, sticky="nsew")
        self._listbox.bind("<Double-Button-1>", lambda e: self._confirm())
        self._listbox.bind("<<ListboxSelect>>", self._on_select)

        # Styled scrollbar for the listbox
        sb_canvas = tk.Canvas(
            list_frame, width=self._p(8), bg=SURF2, highlightthickness=0
        )
        sb_canvas.grid(row=0, column=1, sticky="ns")

        def _sb_scroll(first, last):
            first, last = float(first), float(last)
            sb_canvas.delete("all")
            if last - first >= 1.0:
                return
            h = sb_canvas.winfo_height() or self._p(400)
            w = sb_canvas.winfo_width() or self._p(8)
            y0 = round(first * h) + self._p(2)
            y1 = round(last * h) - self._p(2)
            r = w // 2
            sb_canvas.create_rectangle(0, y0, w, y1, fill=BORDER, outline="")
            sb_canvas.create_oval(0, y0, w, y0 + w, fill=ACCENTL, outline="")
            sb_canvas.create_oval(0, y1 - w, w, y1, fill=ACCENTL, outline="")
            sb_canvas.create_rectangle(0, y0 + r, w, y1 - r, fill=ACCENTL, outline="")

        def _sb_drag(e):
            h = sb_canvas.winfo_height()
            if h:
                self._listbox.yview_moveto(max(0, min(1, e.y / h)))

        sb_canvas.bind("<B1-Motion>", _sb_drag)
        sb_canvas.bind("<Button-1>", _sb_drag)
        self._listbox.configure(yscrollcommand=_sb_scroll)

        # Mousewheel on listbox stays local
        def _wheel(e):
            self._listbox.yview_scroll(int(-1 * e.delta / 120), "units")

        self._listbox.bind("<MouseWheel>", _wheel)

        # ── Selected path display ──────────────────────────────────────────────
        path_frame = tk.Frame(
            self, bg=SURF2, highlightbackground=BORDER, highlightthickness=1
        )
        path_frame.pack(fill="x", padx=pad, pady=(0, self._p(8)))

        tk.Label(
            path_frame, text="Path:", font=("Segoe UI", self._f(8)), bg=SURF2, fg=SUBTLE
        ).pack(side="left", padx=(self._p(8), self._p(4)), pady=self._p(6))

        self._path_var = tk.StringVar(value=self._result)
        tk.Label(
            path_frame,
            textvariable=self._path_var,
            font=("Segoe UI", self._f(8)),
            bg=SURF2,
            fg=ACCENTL,
            anchor="w",
            wraplength=self._p(380),
            justify="left",
        ).pack(
            side="left", fill="x", expand=True, padx=(0, self._p(8)), pady=self._p(6)
        )

        # ── Footer buttons ────────────────────────────────────────────────────
        foot = tk.Frame(self, bg=SURF, highlightbackground=BORDER, highlightthickness=1)
        foot.pack(fill="x", side="bottom")

        tk.Button(
            foot,
            text="Browse…",
            font=("Segoe UI", self._f(9)),
            bg=SURF2,
            fg=TEXT,
            activebackground=BORDER,
            activeforeground=TEXT,
            relief="flat",
            cursor="hand2",
            padx=self._p(14),
            pady=self._p(7),
            command=self._browse,
        ).pack(side="left", padx=self._p(12), pady=self._p(10))

        tk.Button(
            foot,
            text="Cancel",
            font=("Segoe UI", self._f(9)),
            bg=SURF2,
            fg=TEXT,
            activebackground=BORDER,
            activeforeground=TEXT,
            relief="flat",
            cursor="hand2",
            padx=self._p(14),
            pady=self._p(7),
            command=self.destroy,
        ).pack(side="right", padx=(0, self._p(8)), pady=self._p(10))

        tk.Button(
            foot,
            text="Select",
            font=("Segoe UI", self._f(9), "bold"),
            bg=ACCENT,
            fg="#fff",
            activebackground=ACCENTL,
            activeforeground="#fff",
            relief="flat",
            cursor="hand2",
            padx=self._p(14),
            pady=self._p(7),
            command=self._confirm,
        ).pack(side="right", padx=self._p(4), pady=self._p(10))

    # ── App scanning ──────────────────────────────────────────────────────────

    def _scan_apps(self):
        """Scan install dirs for .exe files. Runs on a background thread."""
        found = {}  # name → path (deduplicate by name)

        # 1. Read Start Menu .lnk shortcuts — most reliable source of app names
        import glob

        for base in self._SCAN_DIRS[-2:]:  # just the Start Menu dirs first
            for lnk in glob.glob(os.path.join(base, "**", "*.lnk"), recursive=True):
                try:
                    name = os.path.splitext(os.path.basename(lnk))[0]
                    if name.lower() in ("uninstall", "setup", "update", "help"):
                        continue
                    found[name] = lnk  # keep .lnk — shell can resolve it
                except Exception:
                    pass

        # 2. Scan Program Files for direct .exe files (1 level deep only)
        for base in self._SCAN_DIRS[:4]:
            if not os.path.isdir(base):
                continue
            try:
                for entry in os.scandir(base):
                    if not entry.is_dir():
                        continue
                    try:
                        for sub in os.scandir(entry.path):
                            if sub.name.lower().endswith(".exe") and sub.is_file():
                                name = os.path.splitext(sub.name)[0]
                                skip_keywords = [
                                    "unins",
                                    "uninst",
                                    "update",
                                    "setup",
                                    "crash",
                                    "helper",
                                    "agent",
                                    "service",
                                ]
                                if any(kw in name.lower() for kw in skip_keywords):
                                    continue
                                if name not in found:
                                    found[name] = sub.path
                    except PermissionError:
                        pass
            except PermissionError:
                pass

        # 3. Notable System32 exes
        sys32 = "C:\\Windows\\System32"
        notable = [
            "mspaint.exe",
            "calc.exe",
            "notepad.exe",
            "cmd.exe",
            "powershell.exe",
            "regedit.exe",
            "taskmgr.exe",
            "control.exe",
            "mstsc.exe",
            "wt.exe",
        ]
        for exe in notable:
            path = os.path.join(sys32, exe)
            if os.path.exists(path):
                name = os.path.splitext(exe)[0].replace("exe", "")
                display = {
                    "mspaint": "Paint",
                    "calc": "Calculator",
                    "notepad": "Notepad",
                    "cmd": "Command Prompt",
                    "powershell": "PowerShell",
                    "regedit": "Registry Editor",
                    "taskmgr": "Task Manager",
                    "control": "Control Panel",
                    "mstsc": "Remote Desktop",
                    "wt": "Windows Terminal",
                }.get(name.lower(), name)
                found.setdefault(display, path)

        # Sort by name
        self._all_apps = sorted(found.items(), key=lambda x: x[0].lower())

        # Update UI on main thread
        self.after(0, self._populate_list)

    def _populate_list(self, apps=None):
        if apps is None:
            apps = self._all_apps
        self._listbox.delete(0, "end")
        self._filtered = apps
        for name, path in apps:
            self._listbox.insert("end", f"  {name}")
        count = len(apps)
        total = len(self._all_apps)
        self._status_var.set(
            f"{count} app{'s' if count != 1 else ''} found"
            + (f"  (showing {count} of {total})" if count < total else "")
        )

        # Pre-select if there's a current value
        if self._result:
            for i, (_, path) in enumerate(apps):
                if path.lower() == self._result.lower():
                    self._listbox.selection_set(i)
                    self._listbox.see(i)
                    break

    def _filter(self, *_):
        q = self._search_var.get().strip().lower()
        if not q:
            self._populate_list(self._all_apps)
        else:
            filtered = [
                (n, p) for n, p in self._all_apps if q in n.lower() or q in p.lower()
            ]
            self._populate_list(filtered)

    def _on_select(self, _=None):
        sel = self._listbox.curselection()
        if sel:
            _, path = self._filtered[sel[0]]
            self._result = path
            self._path_var.set(path)

    def _browse(self):
        from tkinter import filedialog

        path = filedialog.askopenfilename(
            parent=self,
            title="Select an Application",
            filetypes=[
                ("Executables", "*.exe *.bat *.cmd *.ps1"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self._result = path
            self._path_var.set(path)
            # Add to list as custom entry and select it
            name = os.path.splitext(os.path.basename(path))[0]
            self._all_apps.insert(0, (f"★ {name}", path))
            self._filter()
            self._listbox.selection_set(0)
            self._listbox.see(0)

    def _confirm(self):
        if self._result:
            if self._callback:
                self._callback(self._result)
            self.destroy()
        else:
            self._status_var.set("⚠  Please select an application first.")


# Colour tokens
BG = "#0e0e16"
SURF = "#16162a"
SURF2 = "#1e1e35"
BORDER = "#2a2a45"
ACCENT = "#6c63ff"
ACCENTL = "#9d98ff"
TEXT = "#ededf5"
SUBTLE = "#70709a"
GREEN = "#3ddc97"
RED = "#ff6b6b"
YELLOW = "#ffd166"

# Corner colours (one per corner so they're visually distinct on the preview)
CORNER_COLOR = {
    "top_left": "#6c63ff",
    "top_right": "#ff6b6b",
    "bottom_left": "#3ddc97",
    "bottom_right": "#ffd166",
}


def png_base64_to_ico_bytes(b64_png):
    import base64
    import struct

    png_data = base64.b64decode(b64_png)
    size = len(png_data)

    width = int.from_bytes(png_data[16:20], "big")
    height = int.from_bytes(png_data[20:24], "big")

    icon_dir = struct.pack("<HHH", 0, 1, 1)

    icon_entry = struct.pack(
        "<BBBBHHII",
        width if width < 256 else 0,
        height if height < 256 else 0,
        0,
        0,
        1,
        32,
        size,
        6 + 16,
    )

    return icon_dir + icon_entry + png_data


class HotCornersApp:
    def __init__(self):
        self.config = load_config()
        self._sc = _dpi_scale()
        self._selected = "top_left"  # which corner is being edited

        self._daemon = HotCornerDaemon(self.config)
        self._daemon.start()

        self.root = tk.Tk()
        # self.root.withdraw()
        # self._create_tray_icon()
        self._setup_tray()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.title("Hot Corners")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        # Set window icon — embedded base64 PNG works with or without icon.ico
        try:
            self._icon_photo = tk.PhotoImage(data=_b64.b64decode(_ICON_B64_32))
            self.root.iconphoto(True, self._icon_photo)
        except Exception:
            pass
        # Prefer iconbitmap (native .ico) when the file is present alongside exe
        try:
            _here = os.path.dirname(os.path.abspath(__file__))
            _ico = os.path.join(_here, "icon.ico")
            if os.path.exists(_ico):
                self.root.iconbitmap(_ico)
        except Exception:
            pass
        self.root.minsize(self._p(520), self._p(400))

        self._apply_theme()

        # Pre-create StringVars for ALL corners so they're always accessible.
        # Must happen after tk.Tk() exists but before _build_ui().
        self._corner_vars = {
            c: tk.StringVar(value=self.config[c]["action"]) for c in CORNERS
        }
        self._custom_vars = {
            c: tk.StringVar(value=self.config[c].get("custom_cmd", "") or PLACEHOLDER)
            for c in CORNERS
        }
        self._custom_entries = {}  # populated by _build_editor

        self._build_ui()

        self.root.update_idletasks()
        rw = self.root.winfo_reqwidth()
        rh = self.root.winfo_reqheight()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{rw}x{rh}+{(sw - rw) // 2}+{(sh - rh) // 2}")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _create_tray_icon(self):
        pass

    def _setup_tray(self):
        hwnd = self.root.winfo_id()

        self._tray_icon_handle = hicon_from_base64_png(_ICON_B64_32)

        self.nid = NOTIFYICONDATA()
        self.nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        self.nid.hWnd = hwnd
        self.nid.uID = 1
        self.nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP
        self.nid.uCallbackMessage = WM_TRAYICON
        self.nid.hIcon = self._tray_icon_handle
        self.nid.szTip = "HotCorners"

        ctypes.windll.shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(self.nid))

        # Subclass window procedure safely
        self.WNDPROC = ctypes.WINFUNCTYPE(
            LRESULT,
            ctypes.wintypes.HWND,
            ctypes.wintypes.UINT,
            ctypes.wintypes.WPARAM,
            ctypes.wintypes.LPARAM,
        )

        self._wnd_proc_ptr = self.WNDPROC(self._wnd_proc)

        self.old_wndproc = ctypes.windll.user32.SetWindowLongPtrW(
            hwnd,
            GWL_WNDPROC,
            self._wnd_proc_ptr,
        )

    def _show_tray_menu(self):
        menu = user32.CreatePopupMenu()

        # ---- Toggle Item ----
        is_enabled = self.config.get("enabled", True)

        toggle_flags = MF_STRING | (MF_CHECKED if is_enabled else MF_UNCHECKED)
        user32.AppendMenuW(menu, toggle_flags, 1, "Enabled")

        # Separator
        user32.AppendMenuW(menu, MF_SEPARATOR, 0, None)

        # Open
        user32.AppendMenuW(menu, MF_STRING, 2, "Open")

        # Exit
        user32.AppendMenuW(menu, MF_STRING, 3, "Exit")

        # Fix menu disappearing instantly
        user32.SetForegroundWindow(self.root.winfo_id())

        pt = ctypes.wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(pt))

        cmd = user32.TrackPopupMenu(
            menu,
            0x00000100,
            pt.x,
            pt.y,
            0,
            self.root.winfo_id(),
            None,
        )

        if cmd == 1:
            self._toggle_enabled()

        elif cmd == 2:
            self._restore_window()

        elif cmd == 3:
            self._exit_app()

    def _toggle_enabled(self):
        current = self.config.get("enabled", True)
        self._set_enabled(not current)

    def _set_enabled(self, state: bool):
        self.config["enabled"] = state

        # Update UI toggle variable
        if hasattr(self, "_enabled_var"):
            self._enabled_var.set(state)

        # Update status label
        self._update_status_label()

        # Update tray tooltip
        self._update_tray_tooltip()

        # Save config
        save_config(self.config)

    def _update_tray_tooltip(self):
        state = "Enabled" if self.config.get("enabled", True) else "Disabled"
        self.nid.szTip = f"HotCorners ({state})"

        shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(self.nid))

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_TRAYICON:
            if lparam == WM_LBUTTONUP:
                self._restore_window()
            elif lparam == WM_RBUTTONUP:
                self._show_tray_menu()
            return 0

        if msg == WM_DESTROY:
            self._remove_tray()

        return ctypes.windll.user32.CallWindowProcW(
            self.old_wndproc,
            hwnd,
            msg,
            wparam,
            lparam,
        )

    def _show_window(self, icon=None, item=None):
        self.root.after(0, self._restore_window)

    def _restore_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def _get_monitor_rect(self, x, y):

        MONITOR_DEFAULTTONEAREST = 2

        class MONITORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.wintypes.DWORD),
                ("rcMonitor", ctypes.wintypes.RECT),
                ("rcWork", ctypes.wintypes.RECT),
                ("dwFlags", ctypes.wintypes.DWORD),
            ]

        pt = ctypes.wintypes.POINT(x, y)

        hmon = ctypes.windll.user32.MonitorFromPoint(
            pt,
            MONITOR_DEFAULTTONEAREST
        )

        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)

        ctypes.windll.user32.GetMonitorInfoW(
            hmon,
            ctypes.byref(mi)
        )

        r = mi.rcMonitor
        return r.left, r.top, r.right, r.bottom

    # def _exit_app(self, icon=None, item=None):
    #     self.tray_icon.stop()
    #     self.root.quit()
    #     self.root.destroy()

    def _remove_tray(self):
        ctypes.windll.shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(self.nid))

    def _exit_app(self):
        self._remove_tray()
        ctypes.windll.user32.DestroyIcon(self._tray_icon_handle)
        self.root.destroy()

    # ── scaling ───────────────────────────────────────────────────────────────
    def _p(self, v):
        return max(1, round(v * self._sc))

    def _f(self, v):
        return max(7, round(v * self._sc))

    # ── theme ─────────────────────────────────────────────────────────────────
    def _apply_theme(self):
        s = ttk.Style(self.root)
        s.theme_use("clam")
        s.configure(
            "TCombobox",
            fieldbackground=SURF2,
            background=SURF2,
            foreground=TEXT,
            selectbackground=ACCENT,
            selectforeground="#fff",
            arrowcolor=ACCENTL,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            borderwidth=1,
            padding=self._p(4),
        )
        s.map(
            "TCombobox",
            fieldbackground=[("readonly", SURF2)],
            foreground=[("readonly", TEXT)],
            background=[("readonly", SURF2), ("active", SURF2)],
        )
        s.configure(
            "TScale",
            background=SURF,
            troughcolor=BORDER,
            sliderlength=self._p(16),
            sliderrelief="flat",
            borderwidth=0,
        )
        s.map("TScale", background=[("active", ACCENT)])
        self.root.option_add("*TCombobox*Listbox.background", SURF2)
        self.root.option_add("*TCombobox*Listbox.foreground", TEXT)
        self.root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#fff")

    # ── top-level layout ──────────────────────────────────────────────────────
    def _build_ui(self):
        # ── header bar ────────────────────────────────────────────────────────
        hbar = tk.Frame(
            self.root, bg=SURF, highlightbackground=BORDER, highlightthickness=1
        )
        hbar.pack(fill="x", side="top")

        # Header icon from embedded base64
        try:
            _hdr_photo = tk.PhotoImage(data=_b64.b64decode(_ICON_B64_24))
            self._hdr_photo = _hdr_photo  # keep reference
            tk.Label(hbar, image=_hdr_photo, bg=SURF).pack(
                side="left", padx=(self._p(18), self._p(6)), pady=self._p(10)
            )
        except Exception:
            pass
        tk.Label(
            hbar,
            text="Hot Corners",
            font=("Segoe UI", self._f(13), "bold"),
            bg=SURF,
            fg=TEXT,
        ).pack(side="left", padx=(0, self._p(18)), pady=self._p(12))

        # Enable toggle on right of header
        tog_wrap = tk.Frame(hbar, bg=SURF)
        tog_wrap.pack(side="right", padx=self._p(18), pady=self._p(10))
        self._enabled_var = tk.BooleanVar(value=self.config.get("enabled", True))
        self._status_lbl = tk.Label(
            tog_wrap, text="", font=("Segoe UI", self._f(8)), bg=SURF, fg=SUBTLE
        )
        self._status_lbl.pack(side="left", padx=(0, self._p(8)))
        self._toggle_canvas = self._make_toggle(
            tog_wrap, self._enabled_var, self._on_toggle
        )
        self._update_status_label()

        # ── body: left preview | right panel ──────────────────────────────────
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3)  # preview gets 3 parts
        body.columnconfigure(1, weight=0)  # divider
        body.columnconfigure(2, weight=2)  # panel gets 2 parts
        body.rowconfigure(0, weight=1)

        # ── left: interactive screen preview ──────────────────────────────────
        left = tk.Frame(body, bg=BG)
        left.grid(
            row=0, column=0, sticky="nsew", padx=(self._p(20), 0), pady=self._p(20)
        )
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        tk.Label(
            left,
            text="Click a corner to configure it",
            font=("Segoe UI", self._f(9)),
            bg=BG,
            fg=SUBTLE,
        ).grid(row=0, column=0, sticky="w", pady=(0, self._p(8)))

        self._canvas = tk.Canvas(
            left,
            bg=SURF2,
            highlightthickness=1,
            highlightbackground=BORDER,
            cursor="hand2",
        )
        self._canvas.grid(row=1, column=0, sticky="nsew")
        self._canvas.bind("<Configure>", self._redraw_preview)
        self._canvas.bind("<Button-1>", self._on_canvas_click)

        # ── divider ───────────────────────────────────────────────────────────
        tk.Frame(body, bg=BORDER, width=1).grid(
            row=0, column=1, sticky="ns", pady=self._p(20)
        )

        # ── right: scrollable settings panel ─────────────────────────────────
        right_outer = tk.Frame(body, bg=BG)
        right_outer.grid(
            row=0, column=2, sticky="nsew", padx=self._p(20), pady=self._p(20)
        )
        right_outer.rowconfigure(0, weight=1)
        right_outer.columnconfigure(0, weight=1)

        # Canvas for the scrollable panel
        self._panel_canvas = tk.Canvas(right_outer, bg=BG, highlightthickness=0)
        self._panel_canvas.grid(row=0, column=0, sticky="nsew")

        # Styled scrollbar — drawn on a Canvas so we control every pixel
        self._sb_canvas = tk.Canvas(
            right_outer,
            width=self._p(8),
            bg=SURF2,
            highlightthickness=0,
            cursor="arrow",
        )
        self._sb_canvas.grid(row=0, column=1, sticky="ns")
        self._sb_thumb = None  # canvas item id

        def _styled_yscroll(first, last):
            """Called by the panel canvas whenever scroll position changes."""
            first, last = float(first), float(last)
            self._sb_canvas.delete("all")
            h = self._sb_canvas.winfo_height()
            w = self._sb_canvas.winfo_width()
            if last - first >= 1.0:
                # Content fits — hide thumb
                return
            y0 = round(first * h) + self._p(2)
            y1 = round(last * h) - self._p(2)
            r = w // 2
            # Rounded-rect thumb using two ovals + rectangle
            self._sb_canvas.create_rectangle(0, y0, w, y1, fill=BORDER, outline="")
            self._sb_canvas.create_oval(0, y0, w, y0 + w, fill=ACCENTL, outline="")
            self._sb_canvas.create_oval(0, y1 - w, w, y1, fill=ACCENTL, outline="")
            self._sb_canvas.create_rectangle(
                0, y0 + r, w, y1 - r, fill=ACCENTL, outline=""
            )

        def _sb_drag(event):
            h = self._sb_canvas.winfo_height()
            frac = max(0.0, min(1.0, event.y / h))
            self._panel_canvas.yview_moveto(frac)

        self._sb_canvas.bind("<B1-Motion>", _sb_drag)
        self._sb_canvas.bind("<Button-1>", _sb_drag)

        self._panel_canvas.configure(yscrollcommand=_styled_yscroll)

        self._panel = tk.Frame(self._panel_canvas, bg=BG)
        self._panel_window = self._panel_canvas.create_window(
            (0, 0), window=self._panel, anchor="nw"
        )

        self._panel.bind("<Configure>", self._on_panel_configure)
        self._panel_canvas.bind("<Configure>", self._on_panelcanvas_configure)

        # Mouse-wheel: scroll the panel only when cursor is over it.
        # Explicitly skip Combobox dropdown listboxes so they can scroll independently.
        def _wheel(e):
            # If the event came from a Combobox popup listbox, do nothing
            widget_class = e.widget.winfo_class()
            if widget_class in ("Listbox", "TCombobox", "ComboboxPopdown"):
                return
            # Walk up to check if we're inside the panel
            w = e.widget
            try:
                while w:
                    if w is self._panel_canvas or w is self._panel:
                        self._panel_canvas.yview_scroll(
                            int(-1 * (e.delta / 120)), "units"
                        )
                        return
                    w = w.master
            except Exception:
                pass

        self._panel_canvas.bind_all("<MouseWheel>", _wheel)

        self._build_panel()

        # ── footer ────────────────────────────────────────────────────────────
        fbar = tk.Frame(
            self.root, bg=SURF, highlightbackground=BORDER, highlightthickness=1
        )
        fbar.pack(fill="x", side="bottom")

        tk.Label(
            fbar,
            text=f"Config: {CONFIG_FILE}",
            font=("Segoe UI", self._f(8)),
            bg=SURF,
            fg=SUBTLE,
        ).pack(side="left", padx=self._p(16), pady=self._p(8))

        tk.Button(
            fbar,
            text="Save & Apply",
            font=("Segoe UI", self._f(9), "bold"),
            bg=ACCENT,
            fg="#fff",
            activebackground=ACCENTL,
            activeforeground="#fff",
            relief="flat",
            cursor="hand2",
            padx=self._p(16),
            pady=self._p(6),
            command=self._save,
        ).pack(side="right", padx=self._p(12), pady=self._p(8))

    # ── panel scroll helpers ──────────────────────────────────────────────────
    def _on_panel_configure(self, _=None):
        self._panel_canvas.configure(scrollregion=self._panel_canvas.bbox("all"))

    def _on_panelcanvas_configure(self, e):
        self._panel_canvas.itemconfig(self._panel_window, width=e.width)

    # ── right panel contents ──────────────────────────────────────────────────
    def _build_panel(self):
        p = self._panel
        pad = self._p(4)

        # ── corner selector tabs ───────────────────────────────────────────────
        tk.Label(
            p, text="CORNERS", font=("Segoe UI", self._f(7), "bold"), bg=BG, fg=SUBTLE
        ).pack(anchor="w", padx=pad, pady=(0, self._p(6)))

        self._tab_btns = {}
        tab_row = tk.Frame(p, bg=BG)
        tab_row.pack(fill="x", padx=pad, pady=(0, self._p(12)))
        tab_row.columnconfigure((0, 1, 2, 3), weight=1)

        for i, corner in enumerate(CORNERS):
            clr = CORNER_COLOR[corner]
            btn = tk.Button(
                tab_row,
                text=CORNER_LABEL[corner].replace("-", "\n"),
                font=("Segoe UI", self._f(7), "bold"),
                bg=SURF2,
                fg=SUBTLE,
                activebackground=SURF,
                activeforeground=TEXT,
                relief="flat",
                cursor="hand2",
                padx=self._p(4),
                pady=self._p(6),
                command=lambda c=corner: self._select_corner(c),
            )
            btn.grid(row=0, column=i, padx=self._p(2), sticky="ew")
            self._tab_btns[corner] = btn

        tk.Frame(p, bg=BORDER, height=1).pack(fill="x", padx=pad, pady=(0, self._p(14)))

        # ── per-corner editor (rebuilt on selection change) ────────────────────
        self._editor_frame = tk.Frame(p, bg=BG)
        self._editor_frame.pack(fill="x", padx=pad)
        self._build_editor()

        tk.Frame(p, bg=BORDER, height=1).pack(
            fill="x", padx=pad, pady=(self._p(16), self._p(14))
        )

        # ── global settings ────────────────────────────────────────────────────
        tk.Label(
            p,
            text="GLOBAL SETTINGS",
            font=("Segoe UI", self._f(7), "bold"),
            bg=BG,
            fg=SUBTLE,
        ).pack(anchor="w", padx=pad, pady=(0, self._p(10)))

        self._dwell_var = tk.IntVar(value=self.config.get("dwell_ms", 400))
        self._corner_px_var = tk.IntVar(value=self.config.get("corner_px", 8))

        self._slider_row(
            p,
            "Dwell Time",
            "How long cursor must stay in corner before triggering",
            self._dwell_var,
            50,
            2000,
            " ms",
        )
        self._slider_row(
            p,
            "Corner Size",
            "Pixel radius from screen edge that counts as a corner",
            self._corner_px_var,
            1,
            60,
            " px",
        )

        # bottom padding
        tk.Frame(p, bg=BG, height=self._p(16)).pack()

    # ── corner editor ─────────────────────────────────────────────────────────
    def _build_editor(self):
        for w in self._editor_frame.winfo_children():
            w.destroy()

        corner = self._selected
        clr = CORNER_COLOR[corner]
        ef = self._editor_frame

        # Title with colour swatch
        title_row = tk.Frame(ef, bg=BG)
        title_row.pack(fill="x", pady=(0, self._p(10)))
        tk.Frame(title_row, bg=clr, width=self._p(4), height=self._p(22)).pack(
            side="left", padx=(0, self._p(8))
        )
        tk.Label(
            title_row,
            text=f"{CORNER_LABEL[corner]}  Corner",
            font=("Segoe UI", self._f(12), "bold"),
            bg=BG,
            fg=TEXT,
        ).pack(side="left")

        # Action label
        tk.Label(
            ef, text="Action", font=("Segoe UI", self._f(9)), bg=BG, fg=SUBTLE
        ).pack(anchor="w", pady=(0, self._p(4)))

        # Dropdown — always use the pre-created StringVar for this corner
        var = self._corner_vars[corner]

        combo = ttk.Combobox(
            ef,
            textvariable=var,
            values=list(ACTIONS.keys()),
            state="readonly",
            font=("Segoe UI", self._f(10)),
        )
        combo.pack(fill="x", pady=(0, self._p(10)))
        combo.bind(
            "<<ComboboxSelected>>", lambda e, c=corner: self._on_action_change(c)
        )

        # Custom command (shown only when Custom Command selected)
        self._custom_frame = tk.Frame(ef, bg=BG)

        tk.Label(
            self._custom_frame,
            text="Command / Path",
            font=("Segoe UI", self._f(9)),
            bg=BG,
            fg=SUBTLE,
        ).pack(anchor="w", pady=(0, self._p(4)))

        # Always use the pre-created custom StringVar for this corner
        cvar = self._custom_vars[corner]
        has_real_cmd = cvar.get() not in ("", PLACEHOLDER)

        entry = tk.Entry(
            self._custom_frame,
            textvariable=cvar,
            font=("Segoe UI", self._f(10)),
            bg=SURF2,
            fg=TEXT if has_real_cmd else SUBTLE,
            insertbackground=TEXT,
            relief="flat",
            bd=self._p(6),
        )
        entry.pack(fill="x")
        self._custom_entries[corner] = entry

        def _fi(_, ent=entry, sv=cvar):
            if sv.get() == PLACEHOLDER:
                sv.set("")
                ent.config(fg=TEXT)

        def _fo(_, ent=entry, sv=cvar):
            if not sv.get().strip():
                sv.set(PLACEHOLDER)
                ent.config(fg=SUBTLE)

        entry.bind("<FocusIn>", _fi)
        entry.bind("<FocusOut>", _fo)

        if var.get() == "Custom Command":
            self._custom_frame.pack(fill="x", pady=(0, self._p(10)))

        # ── Launch App frame (shown only when Launch App selected) ────────────
        self._launch_frame = tk.Frame(ef, bg=BG)

        tk.Label(
            self._launch_frame,
            text="Application",
            font=("Segoe UI", self._f(9)),
            bg=BG,
            fg=SUBTLE,
        ).pack(anchor="w", pady=(0, self._p(4)))

        launch_row = tk.Frame(self._launch_frame, bg=BG)
        launch_row.pack(fill="x")
        launch_row.columnconfigure(0, weight=1)

        # Reuse the same custom_var to store the exe path
        launch_disp = tk.Label(
            launch_row,
            textvariable=cvar,
            font=("Segoe UI", self._f(8)),
            bg=SURF2,
            fg=TEXT if has_real_cmd else SUBTLE,
            anchor="w",
            relief="flat",
            padx=self._p(6),
            pady=self._p(5),
            wraplength=self._p(180),
            justify="left",
        )
        launch_disp.grid(row=0, column=0, sticky="ew", padx=(0, self._p(6)))

        def _open_picker(c=corner, lbl=launch_disp):
            def _on_picked(path):
                self._custom_vars[c].set(path)
                lbl.config(fg=TEXT)

            AppPickerDialog(
                self.root, initial_path=self._custom_vars[c].get(), callback=_on_picked
            )

        tk.Button(
            launch_row,
            text="Browse Apps",
            font=("Segoe UI", self._f(8), "bold"),
            bg=ACCENT,
            fg="#fff",
            activebackground=ACCENTL,
            activeforeground="#fff",
            relief="flat",
            cursor="hand2",
            padx=self._p(10),
            pady=self._p(5),
            command=_open_picker,
        ).grid(row=0, column=1)

        if var.get() == "Launch App":
            self._launch_frame.pack(fill="x", pady=(0, self._p(10)))

        # Quick-action hint
        self._hint_label = tk.Label(
            ef,
            text="",
            font=("Segoe UI", self._f(8)),
            bg=BG,
            fg=clr,
            wraplength=self._p(220),
            justify="left",
        )
        self._hint_label.pack(anchor="w")
        self._update_hint(corner)

    def _on_action_change(self, corner):
        action = self._corner_vars[corner].get()
        if action == "Custom Command":
            self._custom_frame.pack(fill="x", pady=(0, self._p(10)))
        else:
            self._custom_frame.pack_forget()
        if action == "Launch App":
            self._launch_frame.pack(fill="x", pady=(0, self._p(10)))
        else:
            self._launch_frame.pack_forget()
        self._update_hint(corner)
        self._redraw_preview()

    ACTION_HINTS = {
        "Nothing": "",
        "Show Desktop": "Win + D — minimises all windows.",
        "Lock Screen": "Immediately locks your session.",
        "Task View / All Windows": "Win + Tab — shows all open windows.",
        "Open Task Manager": "Launches Task Manager.",
        "Open Start Menu": "Presses the Windows key.",
        "Open Action Center": "Win + A — opens the notification panel.",
        "Open File Explorer": "Opens a new File Explorer window.",
        "Sleep": "Puts the PC to sleep (no admin needed).",
        "Screen Saver": "Activates the screen saver immediately.",
        "Custom Command": "Run any executable, script, or shell command.",
        "Launch App": "Browse and pick any installed application to launch.",
    }

    def _update_hint(self, corner):
        action = self._corner_vars[corner].get()
        self._hint_label.config(text=self.ACTION_HINTS.get(action, ""))

    # ── corner tab selection ──────────────────────────────────────────────────
    def _select_corner(self, corner):
        self._selected = corner
        self._highlight_tabs()
        self._build_editor()
        self._redraw_preview()

    def _highlight_tabs(self):
        for c, btn in self._tab_btns.items():
            if c == self._selected:
                clr = CORNER_COLOR[c]
                btn.config(bg=clr, fg="#fff")
            else:
                btn.config(bg=SURF2, fg=SUBTLE)

    # ── interactive canvas preview ────────────────────────────────────────────
    def _redraw_preview(self, _=None):
        cv = self._canvas
        cv.delete("all")
        W = cv.winfo_width() or self._p(300)
        H = cv.winfo_height() or self._p(220)

        # Screen body
        pad = self._p(10)
        sx0, sy0, sx1, sy1 = pad, pad, W - pad, H - pad

        # Monitor bezel
        cv.create_rectangle(
            sx0 - self._p(6),
            sy0 - self._p(6),
            sx1 + self._p(6),
            sy1 + self._p(6),
            fill=SURF,
            outline=BORDER,
            width=self._p(2),
        )
        # Screen background
        cv.create_rectangle(sx0, sy0, sx1, sy1, fill=BG, outline="")

        # Fake desktop wallpaper gradient (two rectangles)
        cv.create_rectangle(
            sx0, sy0, sx1, sy0 + (sy1 - sy0) // 2, fill="#0f1020", outline=""
        )
        cv.create_rectangle(
            sx0, sy0 + (sy1 - sy0) // 2, sx1, sy1, fill="#0a0a18", outline=""
        )

        # Fake taskbar
        tb = max(12, round((sy1 - sy0) * 0.1))
        cv.create_rectangle(sx0, sy1 - tb, sx1, sy1, fill=SURF2, outline="")

        # Fake windows on desktop
        wins = [
            (0.15, 0.12, 0.40, 0.50),
            (0.50, 0.08, 0.38, 0.45),
            (0.18, 0.55, 0.35, 0.28),
        ]
        for fx, fy, fw, fh in wins:
            x0 = sx0 + round(fx * (sx1 - sx0))
            y0 = sy0 + round(fy * (sy1 - sy0 - tb))
            x1 = x0 + round(fw * (sx1 - sx0))
            y1 = y0 + round(fh * (sy1 - sy0 - tb))
            th = max(5, round((y1 - y0) * 0.14))
            cv.create_rectangle(x0, y0, x1, y1, fill="#1a1a2e", outline=BORDER)
            cv.create_rectangle(x0, y0, x1, y0 + th, fill=SURF2, outline="")

        # Corner hot-zones — size proportional to corner_px setting
        px = (
            self._corner_px_var.get()
            if hasattr(self, "_corner_px_var")
            else self.config.get("corner_px", 8)
        )
        # scale visual zone so it's always visible regardless of px value
        zone = max(self._p(32), min(self._p(80), round((sx1 - sx0) * px / 200)))

        zone_coords = {
            "top_left": (sx0, sy0, sx0 + zone, sy0 + zone),
            "top_right": (sx1 - zone, sy0, sx1, sy0 + zone),
            "bottom_left": (sx0, sy1 - tb - zone, sx0 + zone, sy1 - tb),
            "bottom_right": (sx1 - zone, sy1 - tb - zone, sx1, sy1 - tb),
        }
        self._zone_coords = zone_coords  # save for click detection

        for corner, (x0, y0, x1, y1) in zone_coords.items():
            clr = CORNER_COLOR[corner]
            action = self._corner_vars[corner].get()
            is_sel = corner == self._selected
            active = action != "Nothing"

            # Zone fill
            alpha_fill = clr if is_sel else (SURF2 if not active else SURF)
            cv.create_rectangle(
                x0,
                y0,
                x1,
                y1,
                fill=alpha_fill,
                outline=clr,
                width=self._p(2) if is_sel else self._p(1),
            )

            # Arrow icon centred in zone
            cx_ = (x0 + x1) // 2
            cy_ = (y0 + y1) // 2
            icon_clr = "#fff" if is_sel else (clr if active else SUBTLE)
            cv.create_text(
                cx_,
                cy_,
                text=CORNER_ICON[corner],
                fill=icon_clr,
                font=("Segoe UI", self._f(11), "bold"),
            )

            # Action label below/beside icon
            short = action if action != "Nothing" else "—"
            # truncate long names
            if len(short) > 12:
                short = short[:11] + "…"
            lbl_clr = "#fff" if is_sel else (clr if active else SUBTLE)

            # Position label outside the zone toward screen centre
            offx = self._p(4) if "right" in corner else -self._p(4)
            offy = self._p(4) if "bottom" in corner else -self._p(4)
            anchor_map = {
                "top_left": ("nw", x1 + self._p(4), y1 + self._p(2)),
                "top_right": ("ne", x0 - self._p(4), y1 + self._p(2)),
                "bottom_left": ("sw", x1 + self._p(4), y0 - self._p(2)),
                "bottom_right": ("se", x0 - self._p(4), y0 - self._p(2)),
            }
            anc, lx, ly = anchor_map[corner]
            cv.create_text(
                lx,
                ly,
                text=short,
                fill=lbl_clr,
                anchor=anc,
                font=("Segoe UI", self._f(7)),
            )

        # Selected corner status label at bottom of canvas
        sel_action = self._corner_vars[self._selected].get()
        clr = CORNER_COLOR[self._selected]
        cv.create_text(
            W // 2,
            H - self._p(6),
            text=f"{CORNER_LABEL[self._selected]}: {sel_action}",
            fill=clr,
            font=("Segoe UI", self._f(8), "bold"),
            anchor="s",
        )

    def _on_canvas_click(self, event):
        """Select whichever corner was clicked."""
        if not hasattr(self, "_zone_coords"):
            return
        for corner, (x0, y0, x1, y1) in self._zone_coords.items():
            if x0 <= event.x <= x1 and y0 <= event.y <= y1:
                self._select_corner(corner)
                return

    # ── toggle ────────────────────────────────────────────────────────────────
    def _make_toggle(self, parent, var, callback):
        W = self._p(44)
        H = self._p(22)

        c = tk.Canvas(
            parent,
            width=W,
            height=H,
            bg=SURF,
            highlightthickness=0,
            cursor="hand2",
        )
        c.pack(side="left")

        def draw():
            c.delete("all")
            on = var.get()

            fill = GREEN if on else BORDER
            r = H // 2

            # Track background
            c.create_oval(0, 0, H, H, fill=fill, outline="")
            c.create_oval(W - H, 0, W, H, fill=fill, outline="")
            c.create_rectangle(r, 0, W - r, H, fill=fill, outline="")

            # Knob
            margin = self._p(3)
            kx = W - H + margin if on else margin

            c.create_oval(
                kx,
                margin,
                kx + H - 2 * margin,
                H - margin,
                fill="white",
                outline="",
            )

        def click(_=None):
            var.set(not var.get())
            callback()

        c.bind("<Button-1>", click)

        # 🔥 THIS IS THE IMPORTANT PART
        var.trace_add("write", lambda *args: draw())

        draw()
        return c

    def _update_status_label(self):
        on = self.config.get("enabled", True)
        self._status_lbl.config(
            text="● ACTIVE" if on else "○ PAUSED", fg=GREEN if on else RED
        )

    # ── slider ────────────────────────────────────────────────────────────────
    def _slider_row(self, parent, label, hint, var, lo, hi, unit=""):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(0, self._p(14)))

        top = tk.Frame(row, bg=BG)
        top.pack(fill="x")
        tk.Label(
            top, text=label, font=("Segoe UI", self._f(9), "bold"), bg=BG, fg=TEXT
        ).pack(side="left")

        disp_var = tk.StringVar()

        def _upd(*_):
            disp_var.set(f"{var.get()}{unit}")

        var.trace_add("write", _upd)
        _upd()

        tk.Label(
            top,
            textvariable=disp_var,
            width=7,
            font=("Segoe UI Mono", self._f(9)),
            bg=SURF2,
            fg=ACCENTL,
        ).pack(side="right")

        tk.Label(
            row,
            text=hint,
            font=("Segoe UI", self._f(7)),
            bg=BG,
            fg=SUBTLE,
            wraplength=self._p(220),
            justify="left",
        ).pack(anchor="w", pady=(self._p(2), self._p(4)))

        def _snap(v, iv=var):
            iv.set(int(float(v)))

        scale = ttk.Scale(
            row, from_=lo, to=hi, variable=var, orient="horizontal", command=_snap
        )
        scale.pack(fill="x")

    # ── callbacks ─────────────────────────────────────────────────────────────
    def _on_toggle(self):
        state = self._enabled_var.get()
        self._set_enabled(state)

    def _save(self):
        for corner in CORNERS:
            action = self._corner_vars[corner].get()
            cmd = self._custom_vars[corner].get().strip()
            if cmd == PLACEHOLDER:
                cmd = ""
            self.config[corner]["action"] = action
            self.config[corner]["custom_cmd"] = cmd

        self.config["dwell_ms"] = int(self._dwell_var.get())
        self.config["corner_px"] = int(self._corner_px_var.get())
        self.config["enabled"] = self._enabled_var.get()
        save_config(self.config)
        self._redraw_preview()

        state = "ACTIVE" if self.config["enabled"] else "PAUSED"
        messagebox.showinfo(
            "Hot Corners",
            f"Saved!  Status: {state}\n"
            f"Dwell: {self.config['dwell_ms']} ms  ·  "
            f"Corner zone: {self.config['corner_px']} px\n\n"
            "Changes take effect immediately.",
        )

    def _on_close(self):
        self._save()
        self.root.withdraw()


if __name__ == "__main__":
    HotCornersApp()
