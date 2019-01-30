import os
from flask import Flask, request, redirect, url_for, jsonify, make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
# import image
import imageservice
import json
import sys

UPLOAD_FOLDER = os.path.abspath("uploads")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app, resources={r"/*": {"origins": "*"}})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # Specify image
        category = sys.argv[1]
        imageservice.imagelink = file.filename
        imageservice.subjectlink = category
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',filename=filename))
        
    
    # import main class
    from model import Model
    # Instanciate main class
    p1 = Model()
    # Execute main class
    p1.performImage()
    return jsonify(request.json)

if __name__ == '__main__':
    app.run(debug=True)