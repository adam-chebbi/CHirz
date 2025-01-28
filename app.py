from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import sqlite3
from file_manager import FileManager
from similarity import calculate_similarity
from text_processing import process_text
from config import BASE_DIR, UPLOAD_FOLDER_CVS, UPLOAD_FOLDER_JDS, DATABASE_URI, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH, SECRET_KEY

app = Flask(__name__)
app.config['UPLOAD_FOLDER_CVS'] = UPLOAD_FOLDER_CVS
app.config['UPLOAD_FOLDER_JDS'] = UPLOAD_FOLDER_JDS
app.config['DATABASE_URI'] = DATABASE_URI
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = SECRET_KEY

file_manager = FileManager()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_file(file, folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(folder, filename)
        file.save(file_path)
        return file_path
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    jd_file = request.files.get('jd-file')
    jd_text = request.form.get('jd-text')
    cv_files = request.files.getlist('cv-files')

    if jd_file:
        jd_file_path = save_file(jd_file, app.config['UPLOAD_FOLDER_JDS'])
    elif jd_text:
        jd_file_path = None
    else:
        flash('Please upload or input a Job Description.', 'danger')
        return redirect(url_for('home'))

    if not cv_files:
        flash('Please upload at least one CV.', 'danger')
        return redirect(url_for('home'))

    jd_content = None
    if jd_file_path:
        jd_content = file_manager.read_file(jd_file_path)
    else:
        jd_content = jd_text

    # Process uploaded CVs and calculate matching scores
    cv_file_paths = []
    matching_scores = []
    for cv_file in cv_files:
        cv_file_path = save_file(cv_file, app.config['UPLOAD_FOLDER_CVS'])
        if cv_file_path:
            cv_file_paths.append(cv_file_path)
            cv_content = file_manager.read_file(cv_file_path)
            score = calculate_similarity(jd_content, cv_content)
            matching_scores.append((cv_file.filename, score))

    # Store results in database or JSON (you can implement this part using your storage choice)
    # Store the CV and JD file information along with matching scores in the database
    conn = sqlite3.connect(app.config['DATABASE_URI'])
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jds (filename, content) VALUES (?, ?)", (jd_file.filename if jd_file else 'JD from text', jd_content))
    jd_id = cursor.lastrowid
    for cv_file, score in zip(cv_file_paths, matching_scores):
        cursor.execute("INSERT INTO cvs (jd_id, filename, filepath, matching_score) VALUES (?, ?, ?, ?)",
                       (jd_id, score[0], cv_file, score[1]))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(app.config['DATABASE_URI'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jds ORDER BY id DESC")
    jds = cursor.fetchall()
    cursor.execute("SELECT * FROM cvs ORDER BY id DESC")
    cvs = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', jds=jds, cvs=cvs)

@app.route('/manage')
def manage():
    conn = sqlite3.connect(app.config['DATABASE_URI'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cvs")
    cvs = cursor.fetchall()
    cursor.execute("SELECT * FROM jds")
    jds = cursor.fetchall()
    conn.close()
    return render_template('manage.html', cvs=cvs, jds=jds)

@app.route('/delete_file/<file_type>/<int:file_id>', methods=['POST'])
def delete_file(file_type, file_id):
    conn = sqlite3.connect(app.config['DATABASE_URI'])
    cursor = conn.cursor()

    if file_type == 'cv':
        cursor.execute("SELECT filepath FROM cvs WHERE id=?", (file_id,))
        file = cursor.fetchone()
        if file:
            os.remove(file[0])
        cursor.execute("DELETE FROM cvs WHERE id=?", (file_id,))
    elif file_type == 'jd':
        cursor.execute("SELECT filename FROM jds WHERE id=?", (file_id,))
        file = cursor.fetchone()
        cursor.execute("DELETE FROM jds WHERE id=?", (file_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('manage'))

if __name__ == '__main__':
    app.run(debug=True)
