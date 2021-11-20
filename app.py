import os
import sys
import glob
import re
import numpy as np

from keras.applications.imagenet_utils import preprocess_input,decode_predictions
from keras.models import load_model
from keras.preprocessing import image



from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer





app = Flask(__name__)

 #MODEL_PATH='./model.hdf5'

model=load_model(MODEL_PATH)
model._make_predict_function()

def model_predict(img_path,model):
    img=image.load_img(img_path,target_size=(224,224))
    x=image.img_to_array(img)
    x=np.expand_dims(x,axis=0)
    x=preprocess__input(x,mode='caffe')
    preds=model.predict(x)
    return preds
UPLOAD_FOLDER = 'static'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='./' + filename), code=301)

@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=requests.files['file']
        basepath=os.file.dirname(__file__)
        file_path=os.path.join(
            basepath,'uploads',secure_filename(f.filename))
        f.save(file_path)
        preds=model_predict(file_path,model)
        pred_class=decode_predictions(preds,top=1)
        result=str(pred_class[0][[0][1]])
        return result
    return None
        


 
if __name__ == "__main__":
    app.run()
