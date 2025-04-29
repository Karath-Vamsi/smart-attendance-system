import pandas as pd
from datetime import datetime
import os

LOG_DIR = "logs"

def get_attendance_for_student(name):
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(LOG_DIR, f"attendance_{date_str}.csv")

    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)
    student_row = df[df["Name"].str.lower() == name.lower()]
    
    if student_row.empty:
        return None

    attendance = {col: student_row.iloc[0][col] for col in df.columns[2:]}
    return attendance

def get_attendance_summary():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(LOG_DIR, f"attendance_{date_str}.csv")

    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)
    summary = {}

    for index, row in df.iterrows():
        student_name = row["Name"]
        student_attendance = {col: row[col] for col in df.columns[2:]}
        summary[student_name] = student_attendance

    return summary
