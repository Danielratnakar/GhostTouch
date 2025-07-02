# 🧠 GhostTouch – Gesture-Based Smart Home Control

GhostTouch is a futuristic, touchless smart home simulation powered by **computer vision**. Using just a webcam, you can control lights, AC, TV, and door locks with **real-time hand gestures** — no physical switches or remotes needed.

---

## 📽️ Demo Preview

> 🔜 *(Add your GIF or YouTube demo link here)*  
> Example: [Watch Demo on YouTube](https://youtu.be/your-demo-link)

---

## ✋ GESTURE CONTROLS

| Gesture         | Hand Pose (Pattern)     | Action                                      |
|----------------|--------------------------|---------------------------------------------|
| 🤘 Rock Sign    | `[0,1,0,0,1]`            | Toggle System ON/OFF                        |
| ✌️ V Sign       | `[0,1,1,0,0]`            | Toggle Light ON/OFF + enter Brightness Mode |
| 👍 Thumbs Up    | `[1,0,0,0,0]`            | Toggle AC ON/OFF + enter Temp Mode          |
| 🖐️ Open Palm    | `[1,1,1,1,1]`            | Toggle TV ON/OFF                            |
| 👊 + Pinky      | `[0,0,0,0,1]`            | Toggle Door Lock                            |
| 🔁 Circle Draw  | Clockwise Index Finger   | Increase Brightness (Light) / Temp (AC)     |
| 🔁 Circle Draw  | Counter-Clockwise Index | Decrease Brightness (Light) / Temp (AC)     |
| 🚫 Other Gesture| Any non-mapped gesture   | Exit Light/AC adjustment mode               |

---

## 🧠 Gesture Patterns

Each gesture is based on **this finger pattern**:  
`[Thumb, Index, Middle, Ring, Pinky]` → `1 = up`, `0 = down`

---

## 📸 Example

| Feature         | Gesture           | Result                  |
|-----------------|-------------------|--------------------------|
| System Control  | 🤘                | Master switch ON/OFF    |
| Light Control   | ✌️                | Toggle & adjust light   |
| AC Control      | 👍                | Toggle & adjust temp    |
| TV Control      | 🖐️                | Turn TV ON/OFF          |
| Door Lock       | 👊 + Pinky        | Lock/Unlock door        |
| Adjustments     | 🔁 Circle         | Clockwise = ↑ / CCW = ↓ |

---

## 📦 Tech Stack

- Python
- OpenCV
- MediaPipe
- Real-time gesture recognition

---

## 🧪 Run the Project

```bash
pip install opencv-python mediapipe
python main.py
