# ==============================================================================
# PROJECT SMART SENTINEL — AI ANTI-SHOULDER SURFER & PRIVACY SHIELD
# AUTHOR / CREATOR: Soumya Shrichandani
# COPYRIGHT (C) 2026 SOUMYA SHRICHANDANI. ALL RIGHTS RESERVED.
# ==============================================================================

"""
Configuration constants for Project Smart Sentinel.
Controls detection sensitivity, auto-lock timeouts, privacy shield modes,
and cyberpunk HUD styling.
"""

import pyautogui

# --- SYSTEM & BRANDING ---
APP_NAME = "SMART SENTINEL"
VERSION = "2.1.0"
AUTHOR = "Soumya Shrichandani"
COPYRIGHT = "Copyright (c) 2026 Soumya Shrichandani. All Rights Reserved."

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
TARGET_FPS = 30
CAMERA_INDEX = 0

# --- INFERENCE SPEED OPTIMIZATION ---
# 0.35x = 448x252 resolution (~12ms per frame, crisp facial detail with 50+ FPS)
DETECTION_DOWNSCALE = 0.35

# --- INITIAL FACE CALIBRATION ---
# 3-second startup scan to register and lock primary operator's face profile
CALIBRATION_SECONDS = 3.0

# --- ACTIVE SCANNING ZONE (FULL 100% FIELD OF VIEW) ---
# Allows operator full freedom of movement across the entire camera view
ACTIVE_ZONE_TOP    = 0.00
ACTIVE_ZONE_BOTTOM = 1.00
ACTIVE_ZONE_LEFT   = 0.00
ACTIVE_ZONE_RIGHT  = 1.00

# --- ACCURACY, SENSITIVITY & HEAD MOTION FREEDOM ---
# 4 neighbors allows natural head movement, speech, and tilts without dropping face
CASCADE_MIN_NEIGHBORS = 4

# Broadened aspect ratio accommodates profile turns, tilted heads, and yaw angles
FACE_MIN_ASPECT_RATIO = 0.50
FACE_MAX_ASPECT_RATIO = 1.60

# Allows user to lean back or sit at normal working distance without dropping face
MIN_FACE_AREA_RATIO = 0.0025

# Inertial tracking persistence: ~0.6s grace period (18 frames at 30fps)
# Prevents false "USER_ABSENT" when user moves, tilts head, blinks, or turns away
FACE_PERSISTENCE_FRAMES = 18

# --- SHOULDER-SURFING (ANTI-LURKER) DEFENSE ---
ANTI_SHOULDER_SURF_ENABLED = True

# Number of consecutive frames with multiple faces required before triggering alert
INTRUDER_CONFIRM_FRAMES = 4

# Recovery frames: consecutive frames of single face required to un-shield
RECOVERY_CONFIRM_FRAMES = 8

# Defense Action: "BLUR" (100% Opaque Frosted Glass Privacy Blur), "MINIMIZE", or "LOCK"
SHIELD_ACTION = "BLUR"

# --- TRUSTED COMPANION GESTURE (THUMBS-UP) ---
# When screen is blurred, primary user can show Thumbs-Up to camera to trust friend
GESTURE_TRUST_ENABLED = True
THUMBS_UP_CONFIRM_FRAMES = 4
HAND_MODEL_PATH = "hand_landmarker.task"

# --- ABSENCE & AUTO-LOCK DEFENSE (20 SECONDS TIMEOUT) ---
AUTO_LOCK_ENABLED = True
ABSENCE_TIMEOUT_SECONDS = 20.0  # Lock workstation after 20s of total user absence
ABSENCE_WARNING_SECONDS = 15.0  # Warning audio beep at 15s

# --- SNAPSHOT EVIDENCE ---
CAPTURE_INTRUDER_EVIDENCE = True
SNAPSHOT_COOLDOWN = 5.0        # minimum seconds between saved intruder snapshots
INTRUDERS_DIR = "intruders"

# --- AUDIO ALERTS ---
AUDIO_ALERTS_ENABLED = True

# --- HUD & VISUAL STYLING (BGR FOR OPENCV) ---
COLOR_SECURE       = (255, 200, 0)    # Electric Cyan
COLOR_INTRUDER     = (40, 40, 255)    # Threat Red
COLOR_WARNING      = (0, 165, 255)    # Defcon Amber / Orange
COLOR_TEXT_PRIMARY = (255, 255, 255)  # Clean White
COLOR_HUD_BG       = (15, 18, 24)     # Deep Titanium Charcoal
