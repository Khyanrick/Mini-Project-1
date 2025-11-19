from flask import Flask, render_template, redirect, request, send_file
from db import fetch_query, execute_query, display_stats
import os

app = Flask(__name__)
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, "uploads")


@app.route('/')
def home():
    files, total_files, total_size = display_stats()
    return render_template('dashboard.html', files=files, total_files=total_files, total_size=total_size)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    execute_query("INSERT INTO files(file_name, file_path, file_size)VALUES(%s,%s,%s)",
                  (file.filename, filepath, os.path.getsize(filepath)))
    return redirect('/')

@app.route('/download/<int:file_id>')
def download_file(file_id):
    file = fetch_query("SELECT file_name, file_path FROM files WHERE file_id=%s", (file_id,))
    if not file:
        files, total_files, total_size = display_stats()
        return render_template('dashboard.html', files=files, total_files=total_files, total_size=total_size)
    file_name, file_path = file[0]

    if not os.path.exists(file_path):
        files, total_files, total_size = display_stats()
        return render_template('dashboard.html', files=files, total_files=total_files, total_size=total_size)
    return send_file(file_path, as_attachment=True)

@app.route('/delete/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    file = fetch_query("SELECT file_name, file_path FROM files WHERE file_id=%s", (file_id,))
    if not file:
        files, total_files, total_size = display_stats()
        return render_template('dashboard.html', files=files, total_files=total_files, total_size=total_size)
    file_name, file_path = file[0]
    if not os.path.exists(file_path):
        files, total_files, total_size = display_stats()
        return render_template('dashboard.html', files=files, total_files=total_files, total_size=total_size)
    os.remove(file_path)
    execute_query("DELETE FROM files WHERE file_id= %s;", (file_id,))
    return redirect('/')

#level 2
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug = True)
