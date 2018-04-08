# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__, template_folder='./')

def getLabel(filepath):
    os.system('python recognize.py --file %s' % filepath)
    outputfile = open('output.txt', 'r')
    label = outputfile.readline()
    outputfile.close()
    return label

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def recognizeFile():
    file = request.files['file']
    file.save('upload.wav')

    label = getLabel('upload.wav')
    return label

if __name__ == '__main__':
    app.run()