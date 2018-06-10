# -*- coding: utf-8 -*-
# import os
import subprocess
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
# from correct_spell import get_best_sentence
app = Flask(__name__, template_folder='./')

def getLabel(filepath):
    # os.system('python recognize.py --file %s' % filepath)
    subprocess.call(['python', 'recognize.py', '--file', filepath])
    outputfile = open('output.txt', 'r')
    records = outputfile.readlines()
    res = []
    for record in records:
        # print(record)
        res.append(record)
    outputfile.close()
    # label = get_best_sentence(label).encode('utf-8')
    # print(res)
    return res

def transform(filename):
    # os.system('ffmpeg -i %s -ar 16000 -ac 1 -ab 256000 upload/upload.wav -y' % filename)
    subprocess.call(['ffmpeg', '-i', filename, '-ar', '16000', '-ac', '1', '-ab', '256000', 'upload/upload.wav', '-y'])

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def recognizeFile():
    file = request.files['file']
    if len(file.filename.split('.')) < 2:
        filename = 'upload/upload.wav'
    else:
        filename = 'upload/upload.%s' % file.filename.split('.')[len(file.filename.split('.'))-1]
    file.save(filename)
    transform(filename)

    res = getLabel('upload/upload.wav')
    return jsonify(result=res)

if __name__ == '__main__':
    app.run()