# ==============================================================================
# PROJECT SMART SENTINEL — AI ANTI-SHOULDER SURFER & PRIVACY SHIELD
# AUTHOR / CREATOR: Soumya Shrichandani
# COPYRIGHT (C) 2026 SOUMYA SHRICHANDANI. ALL RIGHTS RESERVED.
# ==============================================================================

import os
import cv2
import time
import math
import numpy as np
from sentinel import config


class TrackedFace:
    """Smoothed bounding box with EMA to eliminate frame jitter."""
    def __init__(self, bbox):
        self.x, self.y, self.w, self.h = [float(v) for v in bbox]
        self.lost_frames = 0

    def update(self, bbox, alpha=0.60):
        bx, by, bw, bh = bbox
        self.x = alpha * bx + (1.0 - alpha) * self.x
        self.y = alpha * by + (1.0 - alpha) * self.y
        self.w = alpha * bw + (1.0 - alpha) * self.w
        self.h = alpha * bh + (1.0 - alpha) * self.h
        self.lost_frames = 0

    @property
    def rect(self):
        return (int(round(self.x)), int(round(self.y)),
                int(round(self.w)), int(round(self.h)))

    @property
    def area(self):
        return self.w * self.h

    @property
    def center(self):
        return (self.x + self.w / 2.0, self.y + self.h / 2.0)


class FacePerceptionEngine:
    """
    High-Speed, High-Accuracy Multi-Angle Face Perception Engine.
    Operates via downscaled pyramid inference (~12ms / 50+ FPS).
    Features:
      - CLAHE adaptive contrast (handles backlighting & dark rooms)
      - Dual-cascade fusion (frontal + profile for turned/tilted heads)
      - 100% full-camera field of view (allows wide movement across the desk)
      - Inertial tracking memory (prevents flickering 'USER_ABSENT' when moving)
      - Calibration-locked primary operator profile
    """
    def __init__(self):
        # 1. Frontal face cascade
        frontal_path = cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        if not os.path.exists(frontal_path):
            frontal_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.frontal_cascade = cv2.CascadeClassifier(frontal_path)

        # 2. Profile face cascade (catches head turned left or right)
        profile_path = cv2.data.haarcascades + 'haarcascade_profileface.xml'
        self.profile_cascade = cv2.CascadeClassifier(profile_path) if os.path.exists(profile_path) else None

        # 3. CLAHE for adaptive illumination balancing
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

        self.tracked_primary = None
        self.calibration_done = False
        self.calibration_samples = []
        self.calibrated_center = None
        self.calibrated_size = None

    def calibrate_step(self, img_bgr, progress_ratio=0.0):
        """
        Scan and register primary operator's face profile during initial startup.
        :param img_bgr: Camera frame
        :param progress_ratio: 0.0 to 1.0
        :return: (is_calibrated, detected_face_rect)
        """
        raw_faces = self._detect_raw(img_bgr)
        if len(raw_faces) > 0:
            # Largest face is primary operator
            raw_faces.sort(key=lambda r: r[2] * r[3], reverse=True)
            chosen = raw_faces[0]
            self.calibration_samples.append(chosen)

            if self.tracked_primary is None:
                self.tracked_primary = TrackedFace(chosen)
            else:
                self.tracked_primary.update(chosen)

        if progress_ratio >= 1.0 and len(self.calibration_samples) >= 3:
            # Calculate mean position and size
            avg_x = np.mean([f[0] + f[2] / 2.0 for f in self.calibration_samples])
            avg_y = np.mean([f[1] + f[3] / 2.0 for f in self.calibration_samples])
            avg_w = np.mean([f[2] for f in self.calibration_samples])
            avg_h = np.mean([f[3] for f in self.calibration_samples])
            self.calibrated_center = (avg_x, avg_y)
            self.calibrated_size = (avg_w, avg_h)
            self.calibration_done = True
            print(f"[Sentinel] Primary Operator Calibrated: center=({int(avg_x)}, {int(avg_y)}), size=({int(avg_w)}x{int(avg_h)})")
            return True, (self.tracked_primary.rect if self.tracked_primary else None)

        return False, (self.tracked_primary.rect if self.tracked_primary else None)

    def _detect_raw(self, img_bgr):
        """
        Downscale frame and run multi-angle cascade with CLAHE adaptive illumination.
        Covers 100% of the camera viewing area so user can move freely.
        """
        h_img, w_img = img_bgr.shape[:2]
        total_area = float(w_img * h_img)

        # 1. Downscale frame for fast, smooth inference
        scale = config.DETECTION_DOWNSCALE
        small_w = max(160, int(w_img * scale))
        small_h = max(90, int(h_img * scale))
        small = cv2.resize(img_bgr, (small_w, small_h), interpolation=cv2.INTER_LINEAR)

        # 2. CLAHE contrast equalization for varying lighting
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        gray = self.clahe.apply(gray)

        # 3. Detect frontal faces
        faces = list(self.frontal_cascade.detectMultiScale(
            gray,
            scaleFactor=1.08,
            minNeighbors=config.CASCADE_MIN_NEIGHBORS,
            minSize=(18, 18),
            flags=cv2.CASCADE_SCALE_IMAGE
        ))

        # 4. If frontal cascade misses, run profile cascade (user looking away / tilted head)
        if len(faces) == 0 and self.profile_cascade is not None:
            # Right profile
            prof_right = self.profile_cascade.detectMultiScale(
                gray,
                scaleFactor=1.09,
                minNeighbors=config.CASCADE_MIN_NEIGHBORS,
                minSize=(18, 18)
            )
            if len(prof_right) > 0:
                faces.extend(prof_right)
            else:
                # Left profile (flipped horizontally)
                flipped = cv2.flip(gray, 1)
                prof_left = self.profile_cascade.detectMultiScale(
                    flipped,
                    scaleFactor=1.09,
                    minNeighbors=config.CASCADE_MIN_NEIGHBORS,
                    minSize=(18, 18)
                )
                for fx, fy, fw, fh in prof_left:
                    orig_x = small_w - fx - fw
                    faces.append((orig_x, fy, fw, fh))

        valid_rects = []
        inv_scale = 1.0 / scale

        # Active boundary limits in full-frame pixels (100% full view)
        zone_x1 = int(w_img * config.ACTIVE_ZONE_LEFT)
        zone_x2 = int(w_img * config.ACTIVE_ZONE_RIGHT)
        zone_y1 = int(h_img * config.ACTIVE_ZONE_TOP)
        zone_y2 = int(h_img * config.ACTIVE_ZONE_BOTTOM)

        for fx, fy, fw, fh in faces:
            # Scale coordinates back to original camera resolution
            rx = int(fx * inv_scale)
            ry = int(fy * inv_scale)
            rw = int(fw * inv_scale)
            rh = int(fh * inv_scale)

            # Check aspect ratio (accommodates profile, tilted, and frontal views)
            aspect = float(rw) / max(1.0, float(rh))
            if aspect < config.FACE_MIN_ASPECT_RATIO or aspect > config.FACE_MAX_ASPECT_RATIO:
                continue

            # Check minimum face area ratio (allows user to sit back comfortably)
            area_ratio = (rw * rh) / total_area
            if area_ratio < config.MIN_FACE_AREA_RATIO:
                continue

            # Check active scan zone boundaries (entire frame)
            cx = rx + rw // 2
            cy = ry + rh // 2
            if not (zone_x1 <= cx <= zone_x2 and zone_y1 <= cy <= zone_y2):
                continue

            valid_rects.append((rx, ry, rw, rh))

        return valid_rects

    def detect(self, img_bgr):
        """
        Scan camera frame and classify faces into Primary User vs Lurkers.
        Employs inertial tracking to smoothly follow user movement and prevent
        momentary head tilts/glances from triggering 'USER_ABSENT'.
        :param img_bgr: OpenCV BGR frame
        :return: (status, primary_rect, intruder_rects, threat_level)
        """
        detected_rects = self._detect_raw(img_bgr)

        # Case 1: Zero faces detected on this frame
        if len(detected_rects) == 0:
            if self.tracked_primary is not None:
                self.tracked_primary.lost_frames += 1
                # Smooth inertial grace window: Operator is still at desk!
                if self.tracked_primary.lost_frames <= config.FACE_PERSISTENCE_FRAMES:
                    return "SECURE", self.tracked_primary.rect, [], 0
                else:
                    self.tracked_primary = None
            return "USER_ABSENT", None, [], 1

        # Case 2: One or more faces detected!
        if self.tracked_primary is not None:
            # Match candidate face closest to tracked primary's moving position
            tx, ty = self.tracked_primary.center
            best_idx = 0
            best_dist = float('inf')
            for idx, r in enumerate(detected_rects):
                cx = r[0] + r[2] / 2.0
                cy = r[1] + r[3] / 2.0
                dist = math.hypot(cx - tx, cy - ty)
                if dist < best_dist:
                    best_dist = dist
                    best_idx = idx

            primary_rect = detected_rects[best_idx]
            intruder_rects = [r for i, r in enumerate(detected_rects) if i != best_idx]
            self.tracked_primary.update(primary_rect)
        else:
            # Initial acquire or return after long absence (largest face is primary)
            detected_rects.sort(key=lambda r: r[2] * r[3], reverse=True)
            primary_rect = detected_rects[0]
            intruder_rects = detected_rects[1:]
            self.tracked_primary = TrackedFace(primary_rect)

        # Case 3: Threat classification
        if len(intruder_rects) > 0:
            status = "INTRUDER_DETECTED"
            threat_level = 2
        else:
            status = "SECURE"
            threat_level = 0

        return status, self.tracked_primary.rect, intruder_rects, threat_level
