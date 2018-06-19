import speech_recognition as sr
from os import path
import glob
import sys

filetype = sys.argv[1]

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), 'upload/uploaded_%s.wav' % filetype)

r = sr.Recognizer()

outputfile = open('res_google_%s.txt' % filetype, 'w')

with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

try:
    res = r.recognize_google(audio, language='vi-VN').encode('utf-8').lower()
    print('\n Google transcript: \n' + res + '\n')
    outputfile.write(res)

except Exception as ex:
    print('\n Google transcript Exception: \n' + str(ex) + '\n')
    outputfile.write(str(ex))
    pass

outputfile.close()