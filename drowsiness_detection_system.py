# Import required libraries

import cv2
import mediapipe as mp
import numpy as np
import time
import os
import serial

from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from absl import logging as absl_logging
from contextlib import contextmanager

# -------------------- SETTINGS --------------------
COM_PORT = 'COM5'   # 🔴 CHANGE THIS
BAUD_RATE = 9600

EAR_THRESHOLD = 0.25
FRAME_CHECK = 15

MODEL_PATH = "face_landmarker.task"

# -------------------- SERIAL SETUP --------------------
try:
    arduino = serial.Serial(COM_PORT, BAUD_RATE)
    time.sleep(2)
    print("✅ Arduino connected")
except:
    print("⚠️ Arduino not connected (running in test mode)")
    arduino = None

# -------------------- LOG CLEAN --------------------
os.environ["GLOG_minloglevel"] = "2"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
absl_logging.set_verbosity(absl_logging.ERROR)

@contextmanager
def suppress_native_stderr():
    stderr_fd = os.dup(2)
    try:
        with open(os.devnull, "w") as devnull:
            os.dup2(devnull.fileno(), 2)
            yield
    finally:
        os.dup2(stderr_fd, 2)
        os.close(stderr_fd)

# -------------------- LOAD MODEL --------------------
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1
)

with suppress_native_stderr():
    detector = vision.FaceLandmarker.create_from_options(options)

# -------------------- EYE INDEX --------------------
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye):
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
    return (A + B) / (2.0 * C)

# -------------------- CAMERA SETUP --------------------
def open_camera():
    for i in range(3):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap
        cap.release()
    return None

cap = open_camera()

if cap is None:
    print("❌ Camera not found")
    exit()

print("✅ Camera started")

# -------------------- MAIN LOOP --------------------
flag = 0
last_timestamp = -1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    timestamp = int(time.monotonic() * 1000)
    if timestamp <= last_timestamp:
        timestamp = last_timestamp + 1
    last_timestamp = timestamp

    result = detector.detect_for_video(mp_image, timestamp)

    status = "Awake"

    if result.face_landmarks:
        for face_landmarks in result.face_landmarks:
            points = [(int(lm.x * w), int(lm.y * h)) for lm in face_landmarks]

            leftEye = [points[i] for i in LEFT_EYE]
            rightEye = [points[i] for i in RIGHT_EYE]

            # Draw eye points
            for (x, y) in leftEye + rightEye:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

            # -------------------- DROWSINESS LOGIC --------------------
            if ear < EAR_THRESHOLD:
                flag += 1
                if flag >= FRAME_CHECK:
                    status = "DROWSY 😴"
                    if arduino:
                        arduino.write(b'1')   # LED + buzzer ON
            else:
                flag = 0
                if arduino:
                    arduino.write(b'0')   # OFF

            # Show EAR
            cv2.putText(frame, f"EAR: {ear:.2f}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Show status
    cv2.putText(frame, status, (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255) if status != "Awake" else (0, 255, 0), 2)

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) == 27:
        break

# -------------------- CLEANUP --------------------
cap.release()
cv2.destroyAllWindows()

if arduino:
    arduino.write(b'0')   # 🔥 Turn OFF before exit
    time.sleep(1)
    arduino.close()