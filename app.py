from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
from backend.attendance import save_attendance, recognize_face, auto_mark_absentees
from backend.register_student import save_uploaded_images, capture_from_webcam
from backend.utils import get_attendance_summary

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['KNOWN_FACES_DIR'] = 'known_faces'
app.config['LOG_DIR'] = 'logs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['KNOWN_FACES_DIR'], exist_ok=True)
os.makedirs(app.config['LOG_DIR'], exist_ok=True)

@app.route('/')
def home():
    today = datetime.now().strftime("%Y-%m-%d")
    csv_path = os.path.join(app.config['LOG_DIR'], f"attendance_{today}.csv")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        attendance_html = df.to_html(classes='table table-striped', index=False)
    else:
        attendance_html = "<p>No attendance data for today yet.</p>"

    return render_template('index.html', attendance_table=attendance_html)

@app.route('/register', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        student_name = request.form['student_name']
        method = request.form['method']

        student_dir = os.path.join(app.config['KNOWN_FACES_DIR'], student_name)
        os.makedirs(student_dir, exist_ok=True)

        if method == 'webcam':
            capture_from_webcam(student_name)
        elif method == 'upload':
            uploaded_files = request.files.getlist('face_images')
            save_uploaded_images(student_name, uploaded_files)

        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/attendance', methods=['GET', 'POST'])
def take_attendance():
    if request.method == 'POST':
        uploaded_file = request.files.get('photo')
        if not uploaded_file:
            return render_template('attendance_result.html', name=None, status="No image received.")

        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.jpg')
        uploaded_file.save(photo_path)

        name = recognize_face(photo_path)
        if name:
            status = save_attendance(name)  # <- Use the returned message
            return render_template('attendance_result.html', name=name, status=status)
        else:
            return render_template('attendance_result.html', name=None, status="Face not recognized.")

    return render_template('attendance.html')

@app.route('/attendance_summary')
def attendance_summary():
    summary = get_attendance_summary()

    return render_template("attendance_summary.html", summary=summary)

# Serve uploaded images (for testing purposes)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
