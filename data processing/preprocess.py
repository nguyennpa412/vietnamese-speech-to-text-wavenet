import numpy as np
import pandas as pd
import glob
import csv
import librosa
import scikits.audiolab
import data
import os
import subprocess

# data path
_data_path = "asset/data/"

#
# process new_data
#

def process_new_data(csv_file, category):

	parent_path = _data_path + 'FINAL_DATA/' + category + '/'
	labels, wave_files = [], []

	# create csv writer
	writer = csv.writer(csv_file, delimiter=',')

	# read label text file list
	f = open(parent_path + 'text.txt', 'rt')
	records = f.readlines()
	for record in records:
		# parsing record
		field = record.split('|')  # split by '|'
		
		if (field[0]+'.wav' in os.listdir(parent_path + 'audio/')):
			# wave file name
			wave_file = parent_path + 'audio/' + '%s.wav' % field[0]
			wave_files.append(wave_file)

			# label index
			labels.append(data.str2index(field[1]))  # last column is text label
			
	f.close()

	# save results
	for i, (wave_file, label) in enumerate(zip(wave_files, labels)):
		fn = wave_file.split('/')[-1]
		target_filename = 'asset/data/preprocess/mfcc/' + fn + '.npy'
		if os.path.exists( target_filename ):
			continue
		# print info
		print("new_data corpus preprocessing (%d / %d) - '%s']" % (i, len(wave_files), wave_file))

		# load wave file
		wave, sr = librosa.load(wave_file, mono=True, sr=None)
		
		# re-sample ( 48K -> 16K )
		# wave = wave[::3]

		# get mfcc feature
		mfcc = librosa.feature.mfcc(wave, sr=16000)

		# save result ( exclude small mfcc data to prevent ctc loss )
		if len(label) < mfcc.shape[1]:
			# save meta info
			writer.writerow([fn] + label)
			# save mfcc
			np.save(target_filename, mfcc, allow_pickle=False)

#
# Create directories
#
if not os.path.exists('asset/data/preprocess'):
	os.makedirs('asset/data/preprocess')
if not os.path.exists('asset/data/preprocess/meta'):
	os.makedirs('asset/data/preprocess/meta')
if not os.path.exists('asset/data/preprocess/mfcc'):
	os.makedirs('asset/data/preprocess/mfcc')


#
# Run pre-processing for training
#

# new_data corpus
csv_f = open('asset/data/preprocess/meta/train.csv', 'w')
process_new_data(csv_f, 'train')
print('DONE process new_data train')
csv_f.close()

#
# Run pre-processing for testing
#

# new_data corpus for test
csv_f = open('asset/data/preprocess/meta/test.csv', 'w')
process_new_data(csv_f, 'test')
print('DONE process new_data test')
csv_f.close()

