import speech_recognition as sr
import os
import re

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

textdata = []
traindatapath = 'asset/data/train_data/'
r = sr.Recognizer()
file = open('asset/data/train_data/text.txt','w')

for fname in sorted(os.listdir(traindatapath),key=numericalSort):
	AUDIO_FILE = traindatapath+fname
	with sr.AudioFile(AUDIO_FILE) as source:
    		audio = r.record(source)
	try:
		transcript = (r.recognize_google(audio, language='vi-VN')).encode('utf-8').strip()
		file.write('%s|' % fname.split('.')[0] + transcript + '\n')
		print('%s:\n' % fname + transcript)
	except:
		pass
		
file.close()

