import os
 
dataset=[]
 
vais='asset/data/vais/train/'
vivos='asset/data/vivos/train/waves/'

def getDataSet(path):
	for fname in os.listdir(path):
		dataset.append(path+fname)

getDataSet(vais)

for folder in os.listdir(vivos):
	getDataSet(vivos+folder+'/')

def transformAudio(dataset):
	count=0
	for fpath in dataset:
		os.system('ffmpeg -i "%s" -ar 16000 -ac 1 -ab 256000 "/home/fg-412/Desktop/vnmese S2T/speech-to-text-wavenet/asset/data/train_data/%s.wav"' % (fpath,count))
		print('%s.wav OK' % count)
		count+=1

transformAudio(dataset)
