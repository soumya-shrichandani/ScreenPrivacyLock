# ==============================================================================
# PROJECT SMART SENTINEL — AI ANTI-SHOULDER SURFER & PRIVACY SHIELD
# AUTHOR / CREATOR: Soumya Shrichandani
# COPYRIGHT (C) 2026 SOUMYA SHRICHANDANI. ALL RIGHTS RESERVED.
# ==============================================================================

import tkinter as tk
import ctypes
import math
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageGrab
import pyautogui
from sentinel import config

# Windows Extended Styles for Topmost Window
GWL_EXSTYLE       = -20
WS_EX_TOPMOST     = 0x00000008
WS_EX_TOOLWINDOW  = 0x00000080
HWND_TOPMOST      = -1
SWP_NOSIZE        = 0x0001
SWP_NOMOVE        = 0x0002
SWP_NOACTIVATE    = 0x0010


def _get_toplevel_hwnd(root: tk.Tk) -> int:
    child = root.winfo_id()
    parent = ctypes.windll.user32.GetParent(child)
    return parent if parent else child


def _apply_overlay_styles(hwnd: int) -> None:
    cur = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, cur | WS_EX_TOOLWINDOW)
    ctypes.windll.user32.SetWindowPos(
        hwnd, HWND_TOPMOST, 0, 0, 0, 0,
        SWP_NOSIZE | SWP_NOMOVE | SWP_NOACTIVATE
    )


class PrivacyShieldCloak:
    """
    100% Opaque Frosted Glass Privacy Blur Screen.
    Completely conceals all desktop windows with authentic frosted blur,
    preventing any shoulder-surfers from reading sensitive code or documents.
    Dismissible via primary operator Thumbs-Up gesture or 'T' key.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sentinel_Privacy_Shield")
        self.root.overrideredirect(True)

        self.width = config.SCREEN_WIDTH
        self.height = config.SCREEN_HEIGHT
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        self.bg_color = "#0B0F19"
        self.root.config(bg=self.bg_color)

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=self.bg_color,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.root.update_idletasks()
        try:
            hwnd = _get_toplevel_hwnd(self.root)
            _apply_overlay_styles(hwnd)
        except Exception:
            pass

        # 100% OPAQUE — Zero transparency so work is completely unreadable
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 1.0)

        self.is_active = False
        self.pulse_phase = 0.0
        self.intruder_count = 1
        self.photo_blur = None
        self.trusted_anim_start = None

        self.root.withdraw()

    def _generate_frosted_blur(self):
        """Capture screen and apply heavy Gaussian blur for genuine frosted glass effect."""
        try:
            screen_pil = ImageGrab.grab()
            arr_rgb = np.array(screen_pil)
            h, w = arr_rgb.shape[:2]

            # Fast dual-pass heavy frosted blur: downscale 8x, gaussian blur, upscale
            small = cv2.resize(arr_rgb, (max(10, w // 8), max(10, h // 8)), interpolation=cv2.INTER_LINEAR)
            blurred = cv2.GaussianBlur(small, (31, 31), 0)
            frosted = cv2.resize(blurred, (self.width, self.height), interpolation=cv2.INTER_LINEAR)

            # Dark tint layer for privacy security
            dark_tint = np.full_like(frosted, (12, 16, 26))
            frosted = cv2.addWeighted(frosted, 0.45, dark_tint, 0.55, 0)

            img_out = Image.fromarray(frosted)
            return ImageTk.PhotoImage(img_out)
        except Exception:
            # Fallback: elegant frosted dark obsidian canvas
            return None

    def show(self, intruder_count=1):
        """Engage the 100% opaque privacy blur."""
        self.intruder_count = intruder_count
        if not self.is_active:
            # Generate authentic frosted blur from desktop
            self.photo_blur = self._generate_frosted_blur()

            self.root.deiconify()
            self.root.update_idletasks()
            self.root.update()
            try:
                hwnd = _get_toplevel_hwnd(self.root)
                _apply_overlay_styles(hwnd)
            except Exception:
                pass
            self.root.wm_attributes("-topmost", True)
            self.root.wm_attributes("-alpha", 1.0)
            self.is_active = True

        self._render_hud()
        self.root.update()

    def hide(self):
        """Disengage privacy blur and restore desktop view."""
        if self.is_active:
            self.canvas.delete("all")
            self.photo_blur = None
            self.trusted_anim_start = None
            self.root.withdraw()
            self.is_active = False
            self.root.update()

    def update_loop(self):
        """Non-blocking update tick for Tkinter event queue."""
        if self.is_active:
            self._render_hud()
            self.root.update()
        else:
            self.root.update_idletasks()

    def flash_trusted_feedback(self):
        """Display affirmative friend-trusted feedback before closing blur."""
        self.trusted_anim_start = True
        self._render_hud()
        self.root.update()

    def _render_hud(self):
        self.canvas.delete("all")
        cx = self.width // 2
        cy = self.height // 2

        # 1. Render Frosted Desktop Background
        if self.photo_blur is not None:
            self.canvas.create_image(0, 0, image=self.photo_blur, anchor="nw")
        else:
            # Solid deep obsidian backing with frosted glass tech matrix
            self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#0A0E17", outline="")
            step = 60
            for x in range(0, self.width, step):
                self.canvas.create_line(x, 0, x, self.height, fill="#121824", width=1)
            for y in range(0, self.height, step):
                self.canvas.create_line(0, y, self.width, y, fill="#121824", width=1)

        self.pulse_phase += 0.15
        pulse_r = int(120 + math.sin(self.pulse_phase) * 14)

        if self.trusted_anim_start:
            # Green affirmative trust confirmation
            self.canvas.create_oval(
                cx - pulse_r, cy - pulse_r,
                cx + pulse_r, cy + pulse_r,
                outline="#00FF66", width=4
            )
            self.canvas.create_text(
                cx, cy - 25,
                text="👍",
                font=("Segoe UI", 52),
                fill="#00FF66"
            )
            self.canvas.create_text(
                cx, cy + 45,
                text="COMPANION VERIFIED AS TRUSTED",
                font=("Consolas", 30, "bold"),
                fill="#00FF66"
            )
            self.canvas.create_text(
                cx, cy + 90,
                text="Restoring desktop access...",
                font=("Segoe UI", 16),
                fill="#E0FFE0"
            )
            return

        # 2. Pulsing Hazard Reticle
        self.canvas.create_oval(
            cx - pulse_r, cy - pulse_r,
            cx + pulse_r, cy + pulse_r,
            outline="#FF2A2A", width=3
        )
        self.canvas.create_oval(
            cx - 85, cy - 85,
            cx + 85, cy + 85,
            outline="#FF8800", width=2, dash=(6, 4)
        )

        # Center Alert Icon
        self.canvas.create_text(
            cx, cy - 20,
            text="⚠️",
            font=("Segoe UI", 48),
            fill="#FF2A2A"
        )

        # 3. Main Warning Text
        self.canvas.create_text(
            cx, cy + 45,
            text="DEFCON 3: PRIVACY SHIELD ENGAGED",
            font=("Consolas", 30, "bold"),
            fill="#FF2A2A"
        )
        self.canvas.create_text(
            cx, cy + 90,
            text=f"SHOULDER-SURFER DETECTED ({self.intruder_count} UNAUTHORIZED PERSON BEHIND WORKSTATION)",
            font=("Segoe UI", 16, "bold"),
            fill="#FFD700"
        )

        # 4. Interactive Gesture Instructions
        self.canvas.create_rectangle(
            cx - 360, cy + 125,
            cx + 360, cy + 185,
            fill="#151B28", outline="#00E5FF", width=2
        )
        self.canvas.create_text(
            cx, cy + 145,
            text="👍 IS THIS A TRUSTED FRIEND / COLLEAGUE?",
            font=("Segoe UI", 13, "bold"),
            fill="#00FFFF"
        )
        self.canvas.create_text(
            cx, cy + 168,
            text="Show a THUMBS-UP to the webcam or press 'T' to authorize and dismiss blur",
            font=("Segoe UI", 11),
            fill="#C0D0E0"
        )

        # 5. Corner Security Brackets
        cw, ch = self.width, self.height
        bracket_len = 60
        b_color = "#FF2A2A"
        margin = 35

        self.canvas.create_line(margin, margin, margin + bracket_len, margin, fill=b_color, width=3)
        self.canvas.create_line(margin, margin, margin, margin + bracket_len, fill=b_color, width=3)
        self.canvas.create_line(cw - margin, margin, cw - margin - bracket_len, margin, fill=b_color, width=3)
        self.canvas.create_line(cw - margin, margin, cw - margin, margin + bracket_len, fill=b_color, width=3)
        self.canvas.create_line(margin, ch - margin, margin + bracket_len, ch - margin, fill=b_color, width=3)
        self.canvas.create_line(margin, ch - margin, margin, ch - margin - bracket_len, fill=b_color, width=3)
        self.canvas.create_line(cw - margin, ch - margin, cw - margin - bracket_len, ch - margin, fill=b_color, width=3)
        self.canvas.create_line(cw - margin, ch - margin, cw - margin, ch - margin - bracket_len, fill=b_color, width=3)

        # Bottom Telemetry Watermark
        self.canvas.create_text(
            cx, ch - 50,
            text="PROJECT SMART SENTINEL | DEVELOPED BY SOUMYA SHRICHANDANI",
            font=("Consolas", 11, "bold"),
            fill="#607080"
        )


def execute_defense_action(action_type="BLUR", cloak_instance=None, intruder_count=1):
    """Dispatch designated defense action."""
    if action_type in ("BLUR", "CLOAK") and cloak_instance:
        cloak_instance.show(intruder_count=intruder_count)
    elif action_type == "MINIMIZE":
        pyautogui.hotkey('win', 'd')
    elif action_type == "LOCK":
        lock_workstation()


def lock_workstation():
    """Immediately lock the Windows computer."""
    try:
        ctypes.windll.user32.LockWorkStation()
    except Exception as e:
        print(f"[Sentinel] Error locking workstation: {e}")
