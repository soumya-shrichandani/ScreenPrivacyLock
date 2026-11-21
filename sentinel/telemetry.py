# ==============================================================================
# PROJECT SMART SENTINEL — AI ANTI-SHOULDER SURFER & PRIVACY SHIELD
# AUTHOR / CREATOR: Soumya Shrichandani
# COPYRIGHT (C) 2026 SOUMYA SHRICHANDANI. ALL RIGHTS RESERVED.
# ==============================================================================

import cv2
import numpy as np
import math
from sentinel import config


class SentinelHUD:
    """
    Cinematic Cyberpunk Telemetry HUD for Camera Video Feed.
    Renders military-grade tactical brackets, radar blips, threat meters,
    initial face calibration UI, and developer credentials.
    """
    def __init__(self):
        self.radar_angle = 0.0
        self.flash_counter = 0

    def draw_corner_brackets(self, img, rect, color, tag=""):
        x, y, w, h = rect
        line_len = max(12, int(min(w, h) * 0.22))
        thickness = 2

        # 4 Corner brackets
        cv2.line(img, (x, y), (x + line_len, y), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x, y), (x, y + line_len), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x + w, y), (x + w - line_len, y), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x + w, y), (x + w, y + line_len), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x, y + h), (x + line_len, y + h), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x, y + h), (x, y + h - line_len), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x + w, y + h), (x + w - line_len, y + h), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x + w, y + h), (x + w, y + h - line_len), color, thickness, cv2.LINE_AA)

        if tag:
            (tw, th), _ = cv2.getTextSize(tag, cv2.FONT_HERSHEY_PLAIN, 0.9, 1)
            cv2.rectangle(img, (x, max(0, y - 20)), (x + tw + 10, y), (15, 18, 24), -1)
            cv2.rectangle(img, (x, max(0, y - 20)), (x + tw + 10, y), color, 1)
            cv2.putText(img, tag, (x + 5, y - 5),
                        cv2.FONT_HERSHEY_PLAIN, 0.85, color, 1, cv2.LINE_AA)

    def draw_radar(self, img, primary_rect, intruder_rects):
        h_img, w_img = img.shape[:2]
        radar_cx = w_img - 70
        radar_cy = 70
        radar_r = 45

        cv2.circle(img, (radar_cx, radar_cy), radar_r, (20, 25, 32), -1)
        cv2.circle(img, (radar_cx, radar_cy), radar_r, (0, 180, 255), 1, cv2.LINE_AA)
        cv2.circle(img, (radar_cx, radar_cy), radar_r // 2, (0, 100, 160), 1, cv2.LINE_AA)

        cv2.line(img, (radar_cx - radar_r, radar_cy), (radar_cx + radar_r, radar_cy), (0, 80, 120), 1)
        cv2.line(img, (radar_cx, radar_cy - radar_r), (radar_cx, radar_cy + radar_r), (0, 80, 120), 1)

        self.radar_angle = (self.radar_angle + 6.0) % 360.0
        rad = math.radians(self.radar_angle)
        scan_x = int(radar_cx + math.cos(rad) * radar_r)
        scan_y = int(radar_cy + math.sin(rad) * radar_r)
        cv2.line(img, (radar_cx, radar_cy), (scan_x, scan_y), (0, 255, 200), 1, cv2.LINE_AA)

        # Primary user blip
        if primary_rect is not None:
            px, py, pw, ph = primary_rect
            norm_x = (px + pw / 2) / w_img
            norm_y = (py + ph / 2) / h_img
            bx = int(radar_cx + (norm_x - 0.5) * 2 * (radar_r - 8))
            by = int(radar_cy + (norm_y - 0.5) * 2 * (radar_r - 8))
            cv2.circle(img, (bx, by), 4, (255, 255, 0), -1, cv2.LINE_AA)

        # Intruder blips
        for ir in intruder_rects:
            ix, iy, iw, ih = ir
            norm_x = (ix + iw / 2) / w_img
            norm_y = (iy + ih / 2) / h_img
            bx = int(radar_cx + (norm_x - 0.5) * 2 * (radar_r - 8))
            by = int(radar_cy + (norm_y - 0.5) * 2 * (radar_r - 8))
            cv2.circle(img, (bx, by), 5, (40, 40, 255), -1, cv2.LINE_AA)

        cv2.putText(img, "RADAR", (radar_cx - 20, radar_cy + radar_r + 14),
                    cv2.FONT_HERSHEY_PLAIN, 0.75, (0, 180, 255), 1, cv2.LINE_AA)

    def render_calibration(self, img, progress_ratio, detected_face):
        """Initial face scanning overlay during startup calibration."""
        h_img, w_img = img.shape[:2]
        cx, cy = w_img // 2, h_img // 2

        # Draw detected face with rotating calibration brackets
        if detected_face is not None:
            self.draw_corner_brackets(img, detected_face, (0, 255, 255), tag="[CALIBRATING OPERATOR]")

        # Progress bar
        bar_w = int(w_img * 0.45)
        bar_x = (w_img - bar_w) // 2
        bar_y = h_img - 110

        pct = int(min(1.0, progress_ratio) * 100)
        cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_w, bar_y + 14), (30, 35, 45), -1)
        fill_w = int(bar_w * min(1.0, progress_ratio))
        cv2.rectangle(img, (bar_x, bar_y), (bar_x + fill_w, bar_y + 14), (0, 255, 255), -1)

        cv2.putText(img, f"SCANNING OPERATOR PROFILE: {pct}%", (bar_x, bar_y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, "Please look directly at camera while registering face",
                    (bar_x, bar_y + 32),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (180, 200, 220), 1, cv2.LINE_AA)

    def render(self, img, status, primary_rect, intruder_rects, threat_level, absence_timer=0.0, fps=30.0, trusted=False):
        h_img, w_img = img.shape[:2]
        self.flash_counter += 1

        # 1. Primary Operator Brackets
        if primary_rect is not None:
            tag = "[TRUSTED OPERATOR]" if not trusted else "[OPERATOR + FRIEND (TRUSTED)]"
            color = (0, 255, 120) if trusted else config.COLOR_SECURE
            self.draw_corner_brackets(img, primary_rect, color, tag=tag)

        # 2. Lurker / Intruder Brackets
        for ir in intruder_rects:
            if trusted:
                # Green brackets for trusted companion
                self.draw_corner_brackets(img, ir, (0, 255, 120), tag="[AUTHORIZED COMPANION]")
            else:
                color = config.COLOR_INTRUDER if (self.flash_counter % 6 < 4) else config.COLOR_WARNING
                self.draw_corner_brackets(img, ir, color, tag="[UNAUTHORIZED LURKER!]")

        # 3. Radar
        self.draw_radar(img, primary_rect, (intruder_rects if not trusted else []))

        # 4. Top Status Banner
        bar_h = 36
        overlay_roi = img[0:bar_h, 0:w_img]
        dark_bar = np.full_like(overlay_roi, (12, 15, 20))
        cv2.addWeighted(dark_bar, 0.80, overlay_roi, 0.20, 0, overlay_roi)

        if threat_level == 2 and not trusted:
            status_text = f"🚨 DEFCON 3: PRIVACY SHIELD ENGAGED ({len(intruder_rects)} LURKER BEHIND YOU)"
            status_color = (40, 40, 255) if (self.flash_counter % 8 < 5) else (0, 165, 255)
        elif trusted:
            status_text = f"🤝 COMPANION TRUSTED (SHOW 👍 OR 'T' TO TOGGLE)"
            status_color = (0, 255, 120)
        elif threat_level == 1:
            time_left = max(0.0, config.ABSENCE_TIMEOUT_SECONDS - absence_timer)
            status_text = f"⚠️ OPERATOR ABSENT — AUTO-LOCK IN {time_left:.1f}s"
            status_color = config.COLOR_WARNING
        else:
            status_text = "🛡️ DEFCON 1: SECURE — 1 OPERATOR VERIFIED"
            status_color = (0, 255, 120)

        cv2.putText(img, status_text, (18, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.56, status_color, 2, cv2.LINE_AA)

        # 5. Bottom Watermark & Hotkeys
        bot_h = 44
        bot_roi = img[h_img - bot_h:h_img, 0:w_img]
        bot_dark = np.full_like(bot_roi, (8, 10, 14))
        cv2.addWeighted(bot_dark, 0.85, bot_roi, 0.15, 0, bot_roi)

        fps_val = int(round(fps))
        watermark = f"{config.APP_NAME} v{config.VERSION} | FPS: {fps_val} | BY {config.AUTHOR.upper()}"
        cv2.putText(img, watermark, (18, h_img - 22),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (180, 200, 220), 1, cv2.LINE_AA)

        cv2.putText(img, "[Q] Quit  [C] Blur Test  [T] Trust  [R] Reset  [S] Stealth",
                    (w_img - 420, h_img - 22),
                    cv2.FONT_HERSHEY_PLAIN, 0.88, (140, 160, 180), 1, cv2.LINE_AA)
