# -*- coding: utf-8 -*-
# import os
import subprocess
import timeit
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
# from correct_spell import get_best_sentence
app = Flask(__name__, template_folder='./')

def transform(filename, filetype):
    # os.system('ffmpeg -i %s -ar 16000 -ac 1 -ab 256000 upload/upload.wav -y' % filename)
    subprocess.call(['ffmpeg', '-i', filename, '-ar', '16000', '-ac', '1', '-ab', '256000', 'upload/uploaded_%s.wav' % filetype, '-y'])

def getOutput(filetype, part):
    start_time = timeit.default_timer()
    if (part == 'wavenet'):
        subprocess.call(['python', 'recognize.py', '--file', 'upload/uploaded_%s.wav' % filetype, filetype])
    elif (part == 'lm'):
        subprocess.call(['python', 'call_lm.py', filetype])
    else:
        subprocess.call(['python', 'google_transcript.py', filetype])
    elapsed = timeit.default_timer() - start_time

    res = open('res_%s_%s.txt' % (part, filetype), 'r')
    output = res.readline()
    res.close()
    
    return [output, str(elapsed)]

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/uploadfile',methods=['POST'])
def uploadFile():
    start_time = timeit.default_timer()
    file = request.files['file']
    if len(file.filename.split('.')) < 2:
        filename = 'upload/uploaded_file.wav'
    else:
        filename = 'upload/uploaded_file.%s' % file.filename.split('.')[len(file.filename.split('.'))-1]
    file.save(filename)
    transform(filename, 'file')
    elapsed = timeit.default_timer() - start_time

    return(str(elapsed))

@app.route('/wavenetfile',methods=['POST'])
def getResWavenetFile():
    return(jsonify(result=getOutput('file', 'wavenet')))

@app.route('/lmfile',methods=['POST'])
def getResLmFile():
    return(jsonify(result=getOutput('file', 'lm')))

@app.route('/googlefile',methods=['POST'])
def getResGoogleFile(): 
    return(jsonify(result=getOutput('file', 'google')))

@app.route('/uploadrecord',methods=['POST'])
def uploadRecord():
    start_time = timeit.default_timer()
    file = request.files['file']
    if len(file.filename.split('.')) < 2:
        filename = 'upload/uploaded_record.wav'
    else:
        filename = 'upload/uploaded_record.%s' % file.filename.split('.')[len(file.filename.split('.'))-1]
    file.save(filename)
    transform(filename, 'record')
    elapsed = timeit.default_timer() - start_time

    return(str(elapsed))

@app.route('/wavenetrecord',methods=['POST'])
def getResWavenetRecord():
    return(jsonify(result=getOutput('record', 'wavenet')))

@app.route('/lmrecord',methods=['POST'])
def getResLmRecord():
    return(jsonify(result=getOutput('record', 'lm')))

@app.route('/googlerecord',methods=['POST'])
def getResGoogleRecord(): 
    return(jsonify(result=getOutput('record', 'google')))

if __name__ == '__main__':
    app.run()