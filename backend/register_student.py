import os
import shutil
import cv2
from tkinter import filedialog, Tk

KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

def save_uploaded_images(student_name, uploaded_files):
    student_dir = os.path.join(KNOWN_FACES_DIR, student_name)
    os.makedirs(student_dir, exist_ok=True)

    for idx, file in enumerate(uploaded_files):
        filename = f"{student_name}_{idx}.jpg"
        file_path = os.path.join(student_dir, filename)
        file.save(file_path)
    return f"{len(uploaded_files)} images uploaded for {student_name}."

def capture_from_webcam(student_name):
    student_dir = os.path.join(KNOWN_FACES_DIR, student_name)
    os.makedirs(student_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow("Register Face - Press Space to Save, Esc to Exit", frame)
        key = cv2.waitKey(1)

        if key == 27:
            break
        elif key == 32:
            img_path = os.path.join(student_dir, f"{student_name}_{count}.jpg")
            cv2.imwrite(img_path, frame)
            count += 1

    cap.release()
    cv2.destroyAllWindows()
    return f"{count} images captured for {student_name}."
