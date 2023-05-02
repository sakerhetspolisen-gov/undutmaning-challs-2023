from flask import Flask
from app.model import Model



app = Flask(__name__, static_folder='static',template_folder = "template")
app.debug = True   
app.config["MAX_CONTENT_LENGTH"] = 512*512*4
app.config["UPLOAD_EXTENSIONS"] = ['.jpeg','.png','.jpg']

model = Model()

from app import views
