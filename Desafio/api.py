from flask import Flask, flash, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import subprocess, os

UPLOAD_FOLDER = 'Upload/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
options = {
    "vertical":"-v",
    "horizontal":"-h",
    "negative":"-n",
    "blur":"-b",
    "gradient":"-g",
    "canny":"-c",
    "contours":"-C"
}
buttons = ['Upload image', 'Download image']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/download')
def download(filename):
    process = subprocess.run(['python3', 'improcessing.py', 'Upload/'+filename],
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
    path = "Processed_Images/"+filename
    return send_file(path, as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('templates/index.html')