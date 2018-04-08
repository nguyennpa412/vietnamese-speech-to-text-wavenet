# -*- coding: utf-8 -*-
import os
import recognize_module
import data

from flask import Flask, render_template, request
app = Flask(__name__, template_folder='./')

def getLabel(filepath):
    labelArr = recognize_module.recognize(filepath)
    for index_list in labelArr:
        label = data.index2str(index_list)
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