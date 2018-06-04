import os

new_train_audio = []
new_train_text = []
new_test_audio = []
new_test_text = []
 
vais_train_audio = 'asset/data/vais/train/audio/'
vais_train_text = 'asset/data/vais/train/text.txt'
vais_test_audio = 'asset/data/vais/test/audio/'
vais_test_text = 'asset/data/vais/test/text.txt'

vivos_train_audio = 'asset/data/vivos/train/waves/'
vivos_train_text = 'asset/data/vivos/train/prompts.txt'
vivos_test_audio = 'asset/data/vivos/test/waves/'
vivos_test_text = 'asset/data/vivos/test/prompts.txt'

KTSpeech_train_audio = 'asset/data/KTSpeech/train/audio/'
KTSpeech_train_text = 'asset/data/KTSpeech/train/text.txt'
KTSpeech_test_audio = 'asset/data/KTSpeech/test/audio/'
KTSpeech_test_text = 'asset/data/KTSpeech/test/text.txt'

audiobook_train_audio = 'asset/data/audioBook/TRUNG_SO_DOC_DAC/train/audio/'
audiobook_train_text = 'asset/data/audioBook/TRUNG_SO_DOC_DAC/train/text.txt'
audiobook_test_audio = 'asset/data/audioBook/TRUNG_SO_DOC_DAC/test/audio/'
audiobook_test_text = 'asset/data/audioBook/TRUNG_SO_DOC_DAC/test/text.txt'

Kingline_train_audio = 'asset/data/King-ASR-M-008-Promotion/train/audio/'
Kingline_train_text = 'asset/data/King-ASR-M-008-Promotion/train/text.txt'
Kingline_test_audio = 'asset/data/King-ASR-M-008-Promotion/test/audio/'
Kingline_test_text = 'asset/data/King-ASR-M-008-Promotion/test/text.txt'

new_train_audio_path = '/home/fg-412/Desktop/vnmese S2T/data processing/asset/data/FINAL_DATA/train/audio'
new_train_text_path = 'asset/data/FINAL_DATA/train/text.txt'

new_test_audio_path = '/home/fg-412/Desktop/vnmese S2T/data processing/asset/data/FINAL_DATA/test/audio'
new_test_text_path = 'asset/data/FINAL_DATA/test/text.txt'

def gather(audiopath, textpath, new_audio, new_text):
	text = open(textpath, 'rt')
	records = text.readlines()
	audio_count = 0

	if ('vivos' in audiopath):
		separator = ' '
	else:
		separator = '|'

	set_name = audiopath.split('/')[2]

	print('gathering %s...' % set_name)

	for audio in os.listdir(audiopath):
		audio_name = audio.split('.')[0]

		for record in records:
			text_audio_name = record.split(separator)[0]
			if (audio_name.lower() == text_audio_name):
				new_audio.append(audiopath + audio)

				if (set_name == 'vivos'):
					new_text.append(' '.join(record.split(separator)[1:]).lower())
				else:
					new_text.append(record.split(separator)[1].lower())

				audio_count += 1
	
	text.close()
	
	print('%s %d OK' % (audiopath, audio_count))

def makeNew(new_audio, new_text, new_audio_path, new_text_path, category):
	newtext = open(new_text_path, 'w')
	newtext.write('')

	count=0
	for audio_path in new_audio:
		os.system('ffmpeg -i "%s" -ar 16000 -ac 1 -ab 256000 "%s/%s_%s.wav"' % (audio_path,new_audio_path,category,count))
		newtext.write('%s_%s' % (category,count) + '|' + new_text[count])
		print('%s data %s/%s OK' % (category,count,len(new_audio)))
		count+=1
		
	newtext.close()
	

for folder in os.listdir(vivos_train_audio):
	folder_path = vivos_train_audio + folder + '/'
	gather(folder_path, vivos_train_text, new_train_audio, new_train_text)

for folder in os.listdir(vivos_test_audio):
	folder_path = vivos_test_audio + folder + '/'
	gather(folder_path, vivos_test_text, new_test_audio, new_test_text)

gather(vais_train_audio, vais_train_text, new_train_audio, new_train_text)
gather(vais_test_audio, vais_test_text, new_test_audio, new_test_text)

gather(KTSpeech_train_audio, KTSpeech_train_text, new_train_audio, new_train_text)
gather(KTSpeech_test_audio, KTSpeech_test_text, new_test_audio, new_test_text)

gather(audiobook_train_audio, audiobook_train_text, new_train_audio, new_train_text)
gather(audiobook_test_audio, audiobook_test_text, new_test_audio, new_test_text)

for folder in os.listdir(Kingline_train_audio):
	folder_path = Kingline_train_audio + folder + '/'
	for part in os.listdir(folder_path):
		part_folder_path = folder_path + part + '/'
		gather(part_folder_path, Kingline_train_text, new_train_audio, new_train_text)

for folder in os.listdir(Kingline_test_audio):
	folder_path = Kingline_test_audio + folder + '/'
	for part in os.listdir(folder_path):
		part_folder_path = folder_path + part + '/'
		gather(part_folder_path, Kingline_test_text, new_test_audio, new_test_text)

makeNew(new_train_audio,new_train_text,new_train_audio_path,new_train_text_path,'train')
makeNew(new_test_audio,new_test_text,new_test_audio_path,new_test_text_path,'test')

os.system('python preprocess.py')