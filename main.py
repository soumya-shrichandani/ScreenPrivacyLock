# ==============================================================================
# PROJECT SMART SENTINEL — AI ANTI-SHOULDER SURFER & PRIVACY SHIELD
# AUTHOR / CREATOR: Soumya Shrichandani
# COPYRIGHT (C) 2026 SOUMYA SHRICHANDANI. ALL RIGHTS RESERVED.
# ==============================================================================

"""
Project Smart Sentinel — Main Workstation Security Controller.
Orchestrates: Camera -> Face Calibration -> Multi-Face Engine -> Privacy Blur -> Thumbs-Up Trust
"""

import cv2
import time
import os
import datetime
from sentinel import config
from sentinel.detector import FacePerceptionEngine
from sentinel.privacy_shield import PrivacyShieldCloak, execute_defense_action, lock_workstation
from sentinel.audio_alert import SoundSynthesizer
from sentinel.telemetry import SentinelHUD
from sentinel.gesture import HandGestureEngine


class SentinelController:
    """
    Main Autonomous Security Pipeline Controller (V2.0 High-FPS & Gesture Trust Edition).
    """
    def __init__(self):
        print(f"\n==================================================================")
        print(f"[{config.APP_NAME} v{config.VERSION}] AI Security Workstation Initializing")
        print(f"Developed by: {config.AUTHOR}")
        print(f"==================================================================")
        print(f"  • Anti-Shoulder Surfer: ACTIVE (Mode: Frosted Privacy Blur)")
        print(f"  • Operator Calibration: ACTIVE ({config.CALIBRATION_SECONDS}s Face Registration)")
        print(f"  • Gesture Trust:        ACTIVE (Show Thumbs-Up to authorize companion)")
        print(f"  • Walk-Away Auto-Lock:  ACTIVE ({config.ABSENCE_TIMEOUT_SECONDS}s Timeout)")
        print(f"  • Controls: [Q] Quit  |  [C] Test Blur  |  [T] Trust  |  [R] Reset  |  [S] Stealth\n")

        # Camera capture pipeline (Hardware MJPG decompression for zero lag)
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(1)

        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Core Engines
        self.detector = FacePerceptionEngine()
        self.cloak = PrivacyShieldCloak()
        self.sound = SoundSynthesizer()
        self.hud = SentinelHUD()
        self.gesture = HandGestureEngine()

        # Calibration State
        self.is_calibrating = True
        self.calibration_start = time.time()

        # Threat Confirmation Filters (Anti-Flicker)
        self.intruder_frame_count = 0
        self.recovery_frame_count = 0
        self.absence_start_time = None
        self.absence_warned = False
        self.last_snapshot_time = 0.0

        # Trust State
        self.companion_trusted = False
        self.defense_engaged = False
        self.stealth_mode = False
        self.running = True

        # FPS Smoother
        self.fps = 30.0
        self.last_frame_time = time.time()

        # Ensure evidence directory exists
        self.intruders_dir = os.path.abspath(config.INTRUDERS_DIR)
        os.makedirs(self.intruders_dir, exist_ok=True)

    def capture_evidence(self, frame_bgr):
        """Save a timestamped photographic snapshot of the shoulder-surfer."""
        now = time.time()
        if now - self.last_snapshot_time < config.SNAPSHOT_COOLDOWN:
            return

        self.last_snapshot_time = now
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"intruder_{timestamp}.jpg"
        filepath = os.path.join(self.intruders_dir, filename)
        try:
            cv2.imwrite(filepath, frame_bgr)
            print(f"[Sentinel ALERT] Intruder snapshot secured: {filepath}")
        except Exception as e:
            print(f"[Sentinel] Error saving snapshot: {e}")

    def run(self):
        """Main real-time detection & defense loop."""
        while self.running:
            # 1. Update Tkinter privacy overlay events (non-blocking)
            self.cloak.update_loop()

            success, img = self.cap.read()
            if not success:
                time.sleep(0.01)
                continue

            img = cv2.flip(img, 1)
            raw_frame = img.copy()
            curr_time = time.time()

            # Smooth FPS calculation
            dt = curr_time - self.last_frame_time
            self.last_frame_time = curr_time
            if dt > 0:
                self.fps = 0.90 * self.fps + 0.10 * (1.0 / dt)

            # ------------------------------------------------------------ #
            # Phase 1: Initial Face Calibration (First 3 seconds)
            # ------------------------------------------------------------ #
            if self.is_calibrating:
                elapsed_cal = curr_time - self.calibration_start
                prog_ratio = min(1.0, elapsed_cal / config.CALIBRATION_SECONDS)
                done, face_rect = self.detector.calibrate_step(img, prog_ratio)

                self.hud.render_calibration(img, prog_ratio, face_rect)
                cv2.imshow(config.APP_NAME, img)

                if done or elapsed_cal >= config.CALIBRATION_SECONDS:
                    self.is_calibrating = False
                    self.sound.chime_secured()
                    print("[Sentinel] Face calibration complete. Security Sentinel fully ACTIVE!")

                key = cv2.waitKey(1) & 0xFF
                if key in (ord('q'), ord('Q'), 27):
                    break
                continue

            # ------------------------------------------------------------ #
            # Phase 2: Active Multi-Person Security Monitoring
            # ------------------------------------------------------------ #
            status, primary_rect, intruder_rects, threat_level = self.detector.detect(img)

            # If user has marked current companion as trusted, bypass threat level
            if self.companion_trusted and len(intruder_rects) > 0:
                threat_level = 0

            # ------------------------------------------------------------ #
            # Thumbs-Up Gesture Trust Detection (When Screen is Blurred)
            # ------------------------------------------------------------ #
            if self.defense_engaged and config.GESTURE_TRUST_ENABLED:
                # Check if primary operator shows a Thumbs-Up to trust the friend
                if self.gesture.is_thumbs_up(raw_frame):
                    print("[Sentinel Gesture] Thumbs-Up detected! Companion marked as TRUSTED.")
                    self.cloak.flash_trusted_feedback()
                    self.sound.chime_secured()
                    time.sleep(0.6)  # Show brief visual confirmation
                    self.companion_trusted = True
                    self.defense_engaged = False
                    self.cloak.hide()
                    self.intruder_frame_count = 0

            # ------------------------------------------------------------ #
            # Defense State Machine: Shoulder-Surfers
            # ------------------------------------------------------------ #
            if status == "INTRUDER_DETECTED":
                self.recovery_frame_count = 0
                self.absence_start_time = None
                self.absence_warned = False

                if not self.companion_trusted:
                    self.intruder_frame_count += 1
                    # Confirm intruder across consecutive frames to avoid false triggers
                    if self.intruder_frame_count >= config.INTRUDER_CONFIRM_FRAMES:
                        if not self.defense_engaged:
                            print(f"[ALERT] Shoulder-surfer detected! Engaging Privacy Blur...")
                            self.defense_engaged = True
                            self.sound.alert_intruder()
                            execute_defense_action(config.SHIELD_ACTION, self.cloak, len(intruder_rects))
                            if config.CAPTURE_INTRUDER_EVIDENCE:
                                self.capture_evidence(raw_frame)

            # ------------------------------------------------------------ #
            # Defense State Machine: Primary Operator Secure (1 Face)
            # ------------------------------------------------------------ #
            elif status == "SECURE":
                self.intruder_frame_count = 0
                self.absence_start_time = None
                self.absence_warned = False

                # If companion left, reset trust so next stranger is screened
                if self.companion_trusted and len(intruder_rects) == 0:
                    self.companion_trusted = False

                if self.defense_engaged:
                    self.recovery_frame_count += 1
                    # Confirm area is truly clear before lifting blur
                    if self.recovery_frame_count >= config.RECOVERY_CONFIRM_FRAMES:
                        print("[SECURE] Area clear. Disengaging Privacy Shield.")
                        self.defense_engaged = False
                        self.cloak.hide()
                        self.sound.chime_secured()

            # ------------------------------------------------------------ #
            # Defense State Machine: Operator Absent (Walk-Away Auto-Lock)
            # ------------------------------------------------------------ #
            elif status == "USER_ABSENT":
                self.intruder_frame_count = 0
                self.companion_trusted = False
                if self.absence_start_time is None:
                    self.absence_start_time = curr_time

                elapsed_absence = curr_time - self.absence_start_time

                # Warning beep before locking
                if (elapsed_absence >= config.ABSENCE_WARNING_SECONDS
                        and not self.absence_warned
                        and config.AUTO_LOCK_ENABLED):
                    self.absence_warned = True
                    self.sound.alert_absence_warning()

                # Lock workstation
                if elapsed_absence >= config.ABSENCE_TIMEOUT_SECONDS and config.AUTO_LOCK_ENABLED:
                    print(f"[AUTO-LOCK] Operator absent for > {config.ABSENCE_TIMEOUT_SECONDS:.0f}s. Locking Windows Workstation!")
                    self.absence_start_time = None
                    self.absence_warned = False
                    self.cloak.hide()
                    lock_workstation()

            # ------------------------------------------------------------ #
            # Visual HUD Rendering
            # ------------------------------------------------------------ #
            absence_elapsed = (curr_time - self.absence_start_time) if self.absence_start_time else 0.0

            if not self.stealth_mode:
                self.hud.render(img, status, primary_rect, intruder_rects, threat_level,
                                absence_elapsed, self.fps, trusted=self.companion_trusted)
                cv2.imshow(config.APP_NAME, img)

            # ------------------------------------------------------------ #
            # Keyboard Controls
            # ------------------------------------------------------------ #
            key = cv2.waitKey(1) & 0xFF
            if key in (ord('q'), ord('Q'), 27):  # 'Q' or ESC to Quit
                self.running = False
                break
            elif key in (ord('c'), ord('C')):    # 'C' to manually test blur
                if self.cloak.is_active:
                    self.cloak.hide()
                    self.defense_engaged = False
                else:
                    self.cloak.show(intruder_count=1)
                    self.defense_engaged = True
            elif key in (ord('t'), ord('T')):    # 'T' to manually toggle trust companion
                self.companion_trusted = not self.companion_trusted
                print(f"[Sentinel] Companion Trust: {'ACTIVE (Allowed)' if self.companion_trusted else 'REVOKED (Shielded)'}")
                if self.companion_trusted and self.defense_engaged:
                    self.defense_engaged = False
                    self.cloak.hide()
                    self.sound.chime_secured()
            elif key in (ord('r'), ord('R')):    # 'R' to reset trust
                self.companion_trusted = False
                print("[Sentinel] Companion Trust reset.")
            elif key in (ord('l'), ord('L')):    # 'L' to manually lock PC
                lock_workstation()
            elif key in (ord('s'), ord('S')):    # 'S' to toggle stealth mode
                self.stealth_mode = not self.stealth_mode
                if self.stealth_mode:
                    cv2.destroyAllWindows()
                    print("[Sentinel] Stealth Mode: ACTIVE (Running silently in background)")
                else:
                    print("[Sentinel] Stealth Mode: DISABLED (Camera preview restored)")

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        self.cloak.hide()
        print(f"[{config.APP_NAME}] Shutdown complete.")


if __name__ == "__main__":
    sentinel = SentinelController()
    sentinel.run()
