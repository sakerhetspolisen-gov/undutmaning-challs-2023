import base64
import flask
import numpy as np
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image
from app import app, model
import imghdr
import json
import os
import tempfile
import io
import base64
import cv2
from torchvision import transforms


#------------------ Utils ---------------------

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None,header)
    if not format:
        return None
    elif format == "jpeg":
        return ".jpeg"
    elif format == "png":
        return ".png"
    elif format == "jpg":
        return ".jpg"
    else:
        return None


def decode_image(image_data):
    image = cv2.imread(image_data)
    return image


def create_response(similarity):
    if similarity > 80.0:
        return flask.redirect(flask.url_for('top_secret_html'))
    else: 
        similarity = round(similarity,3)
        jsondata ={'Permission': 'Access denied!','sim': similarity, 'text': 'Al: Similarity is ' + str(similarity) + ", to class 100, not enough to access a top secret system","info":""}

    return flask.render_template('lab.html',jsondata=jsondata)


#------------------ Routes ---------------------

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/model_top_secret')
def secret_model():
    return flask.redirect("https://download.pytorch.org/models/efficientnet_v2_s-dd5fe13b.pth")

@app.route('/about')
def about():
    return flask.render_template('about.html')

@app.route('/lab', methods = ['GET', 'POST'])
def lab():
    if flask.request.method == "POST":
        imageupload = flask.request.files['image']
        filename = secure_filename(imageupload.filename)
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(imageupload.stream):
                flask.abort(400)
            temp = tempfile.TemporaryFile()
            imageupload.save(str(temp.name))

            tensor = decode_image(str(temp.name))
            similarity = model.check_similarity(tensor)
            response = create_response(similarity)
            temp.close()
            return response
        else:
            flask.abort(400)
    else:
        jsondata = {'Permission': 'Access','sim': '', 'text': '','info': "To gain access to the research and development receipe lab, provide Al with your Security ID below."}
        return flask.render_template('lab.html',jsondata = jsondata)

@app.route('/robots.txt')
def static_from_root():
    print(flask.request.path[1:])
    return flask.send_from_directory(app.static_folder, flask.request.path[1:])

alphabet = ["w","W","o","T","t","€","x","h","J", "1", "3","g","Z","i","r","k","q","Q","m","-","!","?","£","$","3","9"]
hash = ''.join([alphabet[value] for value in np.random.randint(len(alphabet), size=30)])
@app.route('/'+hash+'_top_secret')
def top_secret_html():
    return flask.render_template('top_secret.html')
