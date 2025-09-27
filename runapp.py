# Credit for this: Ethan
# -*- coding: utf-8 -*-
import os, sys
from flask import Flask, jsonify, session, abort, request, flash
from flask import render_template_string, redirect, url_for, render_template, send_file, send_from_directory
from astar import example
import json
from PIL import Image
import pytz
from werkzeug.utils import secure_filename
import numpy
import datetime


ALLOWED_EXTENSIONS = set(['png','jpg'])
UPLOAD_FOLDER = "D:\\agv\\static"
utc_now = pytz.utc.localize(datetime.datetime.utcnow())
currentDT = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
hr = str(currentDT.time().hour)
mi = str(currentDT.time().minute)
sc = str(currentDT.time().second)
ms = str(currentDT.time().microsecond)
timeString = hr+'_'+mi+'_'+sc+'_'+ms
DATE = currentDT.strftime("%Y-%m-%d")
DATE_UNDERSCORE = currentDT.strftime("%Y_%m_%d")
tagdatetime = DATE_UNDERSCORE + timeString


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret!'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def home():
    #mapped = example()
    #print(mapped)
    col = Image.open("static/floor_plan_factory.png")
    col = col.resize((80,40))
    gray = col.convert('L')
    bw = gray.point(lambda x: 0 if x<210 else x>210, '1')
    np_img = numpy.array(bw)
    #bw.save("imgbw.png")
    #print(bw)
    #numpydata = asarray(col)
    #xx = numpy.resize(gray, (40,80))
    intint = (~np_img.astype(bool)).astype(int).tolist()
    #intint = np_img.astype(int).tolist()
    #print(intint)
    #numpy.savetxt("arraypic.txt", intint)
    return render_template("index.html", intins=intint) #grp=mapped


@app.route('/processfloorplan', methods=['GET', 'POST'])
def processfloorplan():
    if request.method == 'POST':
        fpfile = request.files['floorplanfile']
        if fpfile and allowed_file(fpfile.filename):
            filename = secure_filename(fpfile.filename)
            fpfile.save(os.path.join(app.config['UPLOAD_FOLDER'], tagdatetime+filename))
            filename = os.path.join(app.config['UPLOAD_FOLDER'], tagdatetime+filename)
            col = Image.open(filename)
            col = col.resize((80,40))
            gray = col.convert('L')
            bw = gray.point(lambda x: 0 if x<210 else x>=210, '1')
            np_img = numpy.array(bw)
            intint = (~np_img.astype(bool)).astype(int).tolist()

            return render_template("index.html", intins=intint)
    

@app.route('/uploadfloorplan')
def uploadfloorplan():
    return render_template("upload_floorplan.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

