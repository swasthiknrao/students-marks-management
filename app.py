from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Excel file paths
STUDENTS_FILE = 'students.xlsx'
SETTINGS_FILE = 'settings.xlsx'

def init_excel_files():
    # Create students file if it doesn't exist
    if not os.path.exists(STUDENTS_FILE):
        df = pd.DataFrame(columns=['roll_number', 'name', 'dob', 'score'])
        df.to_excel(STUDENTS_FILE, index=False)
    
    # Create settings file if it doesn't exist
    if not os.path.exists(SETTINGS_FILE):
        df = pd.DataFrame({'max_marks': [100]})
        df.to_excel(SETTINGS_FILE, index=False)

def get_max_marks():
    if os.path.exists(SETTINGS_FILE):
        df = pd.read_excel(SETTINGS_FILE)
        return df['max_marks'].iloc[0]
    return 100

def update_max_marks(max_marks):
    df = pd.DataFrame({'max_marks': [max_marks]})
    df.to_excel(SETTINGS_FILE, index=False)

def get_students(sort_by=None):
    if os.path.exists(STUDENTS_FILE):
        df = pd.read_excel(STUDENTS_FILE)
        if sort_by:
            df = df.sort_values(by=sort_by)
        return df
    return pd.DataFrame(columns=['roll_number', 'name', 'dob', 'score'])

def add_student(roll_number, name, dob):
    df = get_students()
    if roll_number in df['roll_number'].values:
        return False
    new_row = pd.DataFrame({'roll_number': [roll_number], 'name': [name], 'dob': [dob], 'score': [None]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(STUDENTS_FILE, index=False)
    return True

def update_student(old_roll_number, roll_number, name, dob):
    df = get_students()
    if old_roll_number != roll_number and roll_number in df['roll_number'].values:
        return False, "Roll number already exists!"
    
    if old_roll_number in df['roll_number'].values:
        df.loc[df['roll_number'] == old_roll_number, 'roll_number'] = roll_number
        df.loc[df['roll_number'] == roll_number, 'name'] = name
        df.loc[df['roll_number'] == roll_number, 'dob'] = dob
        df.to_excel(STUDENTS_FILE, index=False)
        return True, "Student details updated successfully!"
    return False, "Student not found!"

def delete_student(roll_number):
    df = get_students()
    if roll_number in df['roll_number'].values:
        df = df[df['roll_number'] != roll_number]
        df.to_excel(STUDENTS_FILE, index=False)
        return True
    return False

def update_score(roll_number, score):
    df = get_students()
    max_marks = get_max_marks()
    if roll_number in df['roll_number'].values:
        if float(score) > max_marks:
            return False, "Score cannot be greater than maximum marks!"
        df.loc[df['roll_number'] == roll_number, 'score'] = score
        df.to_excel(STUDENTS_FILE, index=False)
        return True, "Score updated successfully!"
    return False, "Student not found!"

def get_student_info(roll_number):
    df = get_students()
    student = df[df['roll_number'] == roll_number]
    if student.empty:
        return None
    student_dict = student.iloc[0].to_dict()
    # Handle NaN values from pandas
    if pd.isna(student_dict['score']):
        student_dict['score'] = None
    student_dict['max_marks'] = get_max_marks()
    return student_dict

# Initialize Excel files
init_excel_files()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'admin' and password == 'admin':
        session['user'] = 'admin'
        return redirect(url_for('admin_dashboard'))
    else:
        students_df = get_students()
        student = students_df[(students_df['roll_number'] == username) & (students_df['dob'] == password)]
        if not student.empty:
            session['user'] = 'student'
            session['student_id'] = username
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
            return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('user') != 'admin':
        return redirect(url_for('index'))
    
    sort_by = request.args.get('sort')
    students = get_students(sort_by)
    students = students.fillna({'score': 'Not Uploaded'})
    students = students.to_dict('records')
    max_marks = get_max_marks()
    
    return render_template('admin_dashboard.html', students=students, max_marks=max_marks)

@app.route('/admin/update_max_marks', methods=['POST'])
def update_max_marks_route():
    if session.get('user') != 'admin':
        return redirect(url_for('index'))
    
    try:
        max_marks = float(request.form['max_marks'])
        if max_marks <= 0:
            flash('Maximum marks must be positive!', 'error')
        else:
            update_max_marks(max_marks)
            flash('Maximum marks updated successfully!', 'success')
    except ValueError:
        flash('Invalid maximum marks value!', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_student', methods=['POST'])
def add_student_route():
    if session.get('user') != 'admin':
        return redirect(url_for('index'))
    
    roll_number = request.form['roll_number']
    name = request.form['name']
    dob = request.form['dob']
    
    if add_student(roll_number, name, dob):
        flash('Student added successfully!', 'success')
    else:
        flash('Roll number already exists!', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_student', methods=['POST'])
def update_student_route():
    if session.get('user') != 'admin':
        return redirect(url_for('index'))
    
    old_roll_number = request.form['old_roll_number']
    roll_number = request.form['roll_number']
    name = request.form['name']
    dob = request.form['dob']
    
    success, message = update_student(old_roll_number, roll_number, name, dob)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_student/<roll_number>', methods=['POST'])
def delete_student_route(roll_number):
    if session.get('user') != 'admin':
        return redirect(url_for('index'))
    
    if delete_student(roll_number):
        flash('Student deleted successfully!', 'success')
    else:
        flash('Student not found!', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_score', methods=['POST'])
def update_score_route():
    if session.get('user') != 'admin':
        return redirect(url_for('index'))
    
    roll_number = request.form['roll_number']
    score = request.form['score']
    
    try:
        score = float(score)
        if score < 0:
            flash('Score must be positive!', 'error')
        else:
            success, message = update_score(roll_number, score)
            if success:
                flash(message, 'success')
            else:
                flash(message, 'error')
    except ValueError:
        flash('Invalid score value!', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('user') != 'student':
        return redirect(url_for('index'))
    
    student = get_student_info(session.get('student_id'))
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('student_dashboard.html', student=student)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 