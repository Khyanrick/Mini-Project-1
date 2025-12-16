from flask import Flask, render_template, redirect, request, send_file, session
from db import fetch_query, execute_query, display_stats
import os
from login_config import ALLOWED_USERS, SECRET_KEY, SHARED_PASSWORD_HASH
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = SECRET_KEY
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, "uploads")


@app.route('/dashboard')
def home():
    username = session.get('username')
    if username  not in ALLOWED_USERS:
        return redirect('/')
    files, total_files, total_size = display_stats()
    return render_template('dashboard.html', files=files, total_files=total_files, total_size=total_size, username=session.get('username'))

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    execute_query("INSERT INTO files(file_name, file_path, file_size, uploaded_by)VALUES(%s,%s,%s,%s)",
                  (file.filename, filepath, os.path.getsize(filepath),(session.get('username'))))
    return redirect('/dashboard')

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
    return redirect('/dashboard')

#level 2
@app.route('/', methods= ['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        username= request.form.get('username')
        password= request.form.get('password')
        if username not in ALLOWED_USERS:
            return render_template('login.html', error="invalid username!")
        elif check_password_hash(SHARED_PASSWORD_HASH, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="invalid KEY!")
        
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')    


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
