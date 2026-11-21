# ==============================================================================
# PROJECT SMART SENTINEL — AI ANTI-SHOULDER SURFER & PRIVACY SHIELD
# AUTHOR / CREATOR: Soumya Shrichandani
# COPYRIGHT (C) 2026 SOUMYA SHRICHANDANI. ALL RIGHTS RESERVED.
# ==============================================================================

"""
Real-time Thumbs-Up Gesture Recognizer for Trusting Companions.
When the screen is blurred, the primary operator can simply show a Thumbs-Up
to the webcam to mark the person behind them as 'TRUSTED' and dismiss the blur.
"""

import os
import math
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from sentinel import config


class HandGestureEngine:
    """
    MediaPipe Task-powered Hand Gesture Detector.
    Lightweight: only invoked when Privacy Blur is active or during trust evaluation.
    """
    def __init__(self, model_path=None):
        if model_path is None:
            # Check local directory or default model path
            local_model = os.path.join(os.path.dirname(__file__), "..", config.HAND_MODEL_PATH)
            model_path = os.path.abspath(local_model)

        self.available = False
        self.landmarker = None
        self.hold_counter = 0

        if os.path.exists(model_path):
            try:
                base_options = python.BaseOptions(model_asset_path=model_path)
                options = vision.HandLandmarkerOptions(
                    base_options=base_options,
                    running_mode=vision.RunningMode.IMAGE,
                    num_hands=1
                )
                self.landmarker = vision.HandLandmarker.create_from_options(options)
                self.available = True
                print(f"[Sentinel Gesture] Hand Landmarker loaded successfully from: {model_path}")
            except Exception as e:
                print(f"[Sentinel Gesture] Model load warning: {e}")
        else:
            print(f"[Sentinel Gesture] Hand model not found at: {model_path} (Fallback to keyboard 'T' for trust)")

    def is_thumbs_up(self, frame_bgr):
        """
        Check if primary operator is showing a Thumbs-Up gesture.
        :param frame_bgr: OpenCV BGR frame
        :return: True if confirmed Thumbs-Up held, else False
        """
        if not self.available or self.landmarker is None:
            return False

        # Convert to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        try:
            result = self.landmarker.detect(mp_image)
        except Exception:
            return False

        if not result.hand_landmarks or len(result.hand_landmarks) == 0:
            self.hold_counter = max(0, self.hold_counter - 1)
            return False

        lms = result.hand_landmarks[0]

        wrist     = lms[0]
        thumb_tip = lms[4]
        index_mcp = lms[5]

        # 1. Thumb elevation and extension check
        d_thumb_idx = math.hypot(thumb_tip.x - index_mcp.x, thumb_tip.y - index_mcp.y)
        thumb_up = (thumb_tip.y < wrist.y - 0.05) and (thumb_tip.y < index_mcp.y - 0.01) and (d_thumb_idx > 0.05)

        # 2. Curl checks for four other fingers (index, middle, ring, pinky)
        curled = 0
        for tip_idx, mcp_idx in [(8, 5), (12, 9), (16, 13), (20, 17)]:
            d = math.hypot(lms[tip_idx].x - lms[mcp_idx].x, lms[tip_idx].y - lms[mcp_idx].y)
            if d < 0.14:
                curled += 1

        raw_thumbs_up = thumb_up and (curled >= 3)

        if raw_thumbs_up:
            self.hold_counter += 1
            if self.hold_counter >= config.THUMBS_UP_CONFIRM_FRAMES:
                return True
        else:
            self.hold_counter = max(0, self.hold_counter - 1)

        return False
