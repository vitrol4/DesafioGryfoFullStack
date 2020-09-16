from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os, cv2, numpy

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
options = ['Vertical', 'Horizontal', 'Negative', 'Blur', 'Gradient', 'Canny', 'Contours']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
''' 
Optei por abrir o arquivo de imagem uma vez e fechá-lo uma vez. 
Isso evita operações no disco, logo, melhora o desempenho.
'''
def improcessing(request, uploadFolder, downloadFolder, filename):
    image = cv2.imread(os.path.join(uploadFolder, filename))
    if request.form.get('Contours'):
        im_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        (thresh, im_bw) = cv2.threshold(im_bw, 128, 255, 0)
        contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (0,255,0), 3)
    if request.form.get('Canny'):
        image = cv2.Canny(image,128,255)
    if request.form.get('Vertical'):
        image = cv2.flip(image, 0)
    if request.form.get('Horizontal'):
        image = cv2.flip(image, 1)
    if request.form.get('Negative'):
        image = cv2.bitwise_not(image)
    if request.form.get('Blur'):
        image = numpy.uint8(image)
        image = cv2.blur(image,(50,50))
    if request.form.get('Gradient'):
        image = cv2.Laplacian(image,cv2.CV_64F)
    
    return cv2.imwrite(os.path.join(downloadFolder, filename), image)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))+'/Upload/'
    app.config['DOWNLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))+'/Processed_Images/'
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            if 'file' not in request.files:
                print('No file attached in request')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                print('No file selected')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                improcessing(request, app.config['UPLOAD_FOLDER'], app.config['DOWNLOAD_FOLDER'], filename)
                return redirect(url_for('uploaded_file', filename=filename))
        return render_template('index.html', options=options)
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

    return app 
