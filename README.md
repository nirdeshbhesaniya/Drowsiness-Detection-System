# 🚗 Drowsiness Detection System (AI + Arduino)

A real-time **Drowsiness Detection System** using **Computer Vision + IoT**.
This system detects eye closure using a laptop camera and triggers **LED + Buzzer alerts via Arduino**.

---

## 🧠 Project Overview

This project uses **MediaPipe Face Landmarker** to track facial landmarks and calculate the **Eye Aspect Ratio (EAR)**.

If the eyes remain closed for a certain duration:

* 🔴 LED turns ON
* 🔊 Buzzer turns ON

---

## 🛠️ Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy
* PySerial
* Arduino

---

## 📦 Components Required

### 💻 Software:

* Python (3.9 / 3.10 recommended)
* Arduino IDE

### 🔌 Hardware:

* Arduino Uno
* LED (Red)
* Buzzer
* 220Ω Resistor
* Breadboard
* Jumper wires

---

## ⚡ Circuit Diagram

### 🔴 LED Connection:

* Arduino Pin 13 → LED (+)
* LED (–) → Resistor → GND

### 🔊 Buzzer Connection:

* Arduino Pin 12 → Buzzer (+)
* Buzzer (–) → GND

---

## 🚀 Setup Guide (Step-by-Step)

### 🔹 Step 1: Clone Repository

```bash
git clone https://github.com/nirdeshbhesaniya/Drowsiness-Detection-System.git
cd drowsiness-detection
```

---

### 🔹 Step 2: Install Dependencies

```bash
pip install opencv-python mediapipe numpy pyserial
```

---

### 🔹 Step 3: Download Model File

Download the MediaPipe model:

https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task

Place it in the project folder:

```
project/
 ├── drowsiness_detection_system.py
 ├── face_landmarker.task
```

---

### 🔹 Step 4: Upload Arduino Code

Open Arduino IDE and upload the following code:

```cpp
int led = 13;
int buzzer = 12;

char data;
unsigned long lastSignalTime = 0;
const int TIMEOUT = 2000;

void setup() {
  pinMode(led, OUTPUT);
  pinMode(buzzer, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  if (Serial.available() > 0) {
    data = Serial.read();
    lastSignalTime = millis();

    if (data == '1') {
      digitalWrite(led, HIGH);
      digitalWrite(buzzer, HIGH);
    }
    else if (data == '0') {
      digitalWrite(led, LOW);
      digitalWrite(buzzer, LOW);
    }
  }

  if (millis() - lastSignalTime > TIMEOUT) {
    digitalWrite(led, LOW);
    digitalWrite(buzzer, LOW);
  }
}
```

---

### 🔹 Step 5: Update COM Port

In `main.py`, update:

```python
COM_PORT = 'COM3'  # Change to your Arduino port
```

---

### 🔹 Step 6: Run the Project

```bash
python main.py
```

---

## 🎯 How It Works

1. Camera captures real-time video
2. MediaPipe detects face landmarks
3. Eye Aspect Ratio (EAR) is calculated
4. If EAR < threshold → Drowsiness detected
5. Signal sent to Arduino via Serial
6. LED + Buzzer activated

---

## 🧪 Testing

| Condition             | Output          |
| --------------------- | --------------- |
| Eyes open             | System idle     |
| Blink                 | No alert        |
| Eyes closed (2–3 sec) | Alert triggered |

---

## ⚠️ Important Notes

* Ensure proper lighting for accurate detection
* Close Arduino Serial Monitor before running Python
* Use correct COM port
* Model file must be in the same directory

---

## 🔥 Features

* Real-time detection
* Lightweight AI model (MediaPipe)
* Arduino integration
* Fail-safe auto OFF system
* Cross-platform compatible

---

## 🚀 Future Improvements

* Mobile alert system (SMS/Email)
* Dashboard UI (React)
* Driver identity verification
* Cloud logging

---

## 👨‍💻 Author

**Nirdesh Bhesaniya**
GitHub: https://github.com/nirdeshbhesaniya

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
