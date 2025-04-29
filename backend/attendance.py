import os
import cv2
import pandas as pd
from datetime import datetime
from deepface import DeepFace
import time

LOG_DIR = "logs"
KNOWN_FACES_DIR = "known_faces"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_known_faces():
    known_faces = []
    for student in os.listdir(KNOWN_FACES_DIR):
        student_folder = os.path.join(KNOWN_FACES_DIR, student)
        if os.path.isdir(student_folder):
            for img in os.listdir(student_folder):
                img_path = os.path.join(student_folder, img)
                known_faces.append((student, img_path))
    return known_faces


def get_current_hour_slot():
    now = datetime.now()
    hour = now.hour
    if 9 <= hour <= 18:
        return f"{hour}AM" if hour < 12 else f"{hour-12 if hour > 12 else 12}PM"
    return None


def is_within_first_30_minutes():
    return datetime.now().minute < 30


def load_attendance_csv():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(LOG_DIR, f"attendance_{date_str}.csv")
    hours = [f"{h}AM" if h < 12 else f"{h-12 if h > 12 else 12}PM" for h in range(9, 19)]

    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        known_faces = get_known_faces()
        student_names = list(set([name for name, _ in known_faces]))
        
        data = []
        for student in student_names:
            row = {"Name": student, "Date": date_str}
            for hour in hours:
                row[hour] = ""
            data.append(row)

        df = pd.DataFrame(data, columns=["Name", "Date"] + hours)
        df.to_csv(path, index=False)

    return df, path


def save_attendance(name):
    now = datetime.now()
    hour_col = get_current_hour_slot()
    if not hour_col:
        return "Outside class hours (9AM–6PM)."

    if not is_within_first_30_minutes():
        return f"{name} was late for the {hour_col} class. Attendance not logged."

    df, path = load_attendance_csv()
    today = now.strftime("%Y-%m-%d")

    if name not in df["Name"].values:
        hours = [f"{h}AM" if h < 12 else f"{h-12 if h > 12 else 12}PM" for h in range(9, 19)]
        new_row = {"Name": name, "Date": today}
        for h in hours:
            new_row[h] = ""
        new_row[hour_col] = "Present"
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        idx = df.index[df["Name"] == name][0]
        current_status = df.at[idx, hour_col]
        if current_status != "Present":
            df.at[idx, hour_col] = "Present"

    df.to_csv(path, index=False)
    return f"Attendance recorded for {name} at {now.strftime('%H:%M:%S')}."


def recognize_face(image_path):
    known_faces = get_known_faces()
    for name, known_image_path in known_faces:
        try:
            result = DeepFace.verify(image_path, known_image_path, enforce_detection=False)
            if result["verified"]:
                return name
        except:
            continue
    return None


def save_new_face(full_frame, student_name):
    student_folder = os.path.join(KNOWN_FACES_DIR, student_name)
    os.makedirs(student_folder, exist_ok=True)

    gray = cv2.cvtColor(full_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        print("No face detected. Saving full image as fallback.")
        face_crop = full_frame
    else:
        (x, y, w, h) = faces[0]
        face_crop = full_frame[y:y+h, x:x+w]

    # Save cropped face
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    new_image_path = os.path.join(student_folder, f"{student_name}_{timestamp}.jpg")
    cv2.imwrite(new_image_path, face_crop)
    print(f"Saved cropped face for {student_name} at {new_image_path}.")

    # (Optional) Backup full frame
    # backup_folder = os.path.join("full_frames_backup", student_name)
    # os.makedirs(backup_folder, exist_ok=True)
    # full_frame_path = os.path.join(backup_folder, f"{student_name}_{timestamp}.jpg")
    # cv2.imwrite(full_frame_path, full_frame)
    # print(f"Backup full frame saved at {full_frame_path}.")

def auto_mark_absentees():
    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(LOG_DIR, f"attendance_{today}.csv")

    if os.path.exists(path):
        return  # Already created

    os.makedirs(LOG_DIR, exist_ok=True)
    students = [name for name in os.listdir(KNOWN_FACES_DIR) if os.path.isdir(os.path.join(KNOWN_FACES_DIR, name))]

    hours = [f"{h}AM" if h < 12 else f"{h-12 if h > 12 else 12}PM" for h in range(9, 19)]
    data = []

    for student in students:
        row = {"Name": student, "Date": today}
        for hour in hours:
            row[hour] = "Absent"
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv(path, index=False)

