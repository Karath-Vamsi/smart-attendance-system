# Smart Attendance System

## 📌 Project Overview

The **Smart Attendance System** is a Python-based facial recognition application designed to automate and streamline classroom attendance. Leveraging the DeepFace library, it captures faces via webcam, recognizes students by matching them against a registered database, and logs their attendance in a structured daily CSV file. The system ensures punctuality by only marking students present if they appear within the first 30 minutes of a session.

---

## 📁 Project Structure

```
attendance_project/
├── known_faces/              # Stores registered face images (e.g., alice_1.jpg, bob_1.jpg)
├── attendance_YYYY-MM-DD.csv# Daily attendance logs
├── deepface_attendance.py    # Handles face detection and attendance logging
├── register_student.py       # Captures face images for registration
└── main.py                   # Entry point and runtime control
```

---

## 🔧 Features

- 📷 **Face Registration**: Capture and store facial images of students for future recognition.
- 🧠 **Face Recognition**: Use DeepFace to compare real-time webcam faces against known faces.
- 📅 **Daily CSV Logging**: Creates an attendance CSV file each day in the format:
  ```
  Name | Date | 9AM | 10AM | ... | 9PM
  ```
- ⏰ **Time-Based Attendance**:
  - Marks students **Present** only if they appear **within the first 30 minutes** of the hour.
  - Displays a **"Late" message** if they appear after 30 minutes; no attendance is marked.
- 🧼 **Cleanup**: Temporary webcam images (e.g., `temp.jpg`) are deleted after use.
- ❌ **No Interference**: Registration images are preserved and not deleted during attendance check.

---

## 🔮 Future Enhancements

- 🛡️ **Liveness Detection**:
  - Use techniques like eye blinking, head movement, or face depth to prevent spoofing.
- 📊 **Attendance Summary View**:
  - Export or display statistics such as total presents, absents, or monthly reports per student.

---

## 🏁 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- OpenCV (`cv2`)
- DeepFace
- Pandas
- NumPy

Install dependencies using pip:

```bash
pip install deepface opencv-python pandas numpy
```

---

## 🚀 How to Use

1. **Register Students**:
   Capture and save face images of students to the `known_faces/` directory.
   ```bash
   python register_student.py
   ```

2. **Take Attendance**:
   Use the webcam to detect and recognize faces.
   ```bash
   python deepface_attendance.py
   ```

3. **Main Menu Control** *(optional)*:
   Run the main interface to choose between registration and attendance.
   ```bash
   python main.py
   ```

---

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it for academic or educational purposes.

---

## 🙌 Acknowledgements

- [DeepFace](https://github.com/serengil/deepface) - for facial recognition.
- OpenCV - for image and video capture.
