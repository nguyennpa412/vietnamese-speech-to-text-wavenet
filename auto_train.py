import os
#import time

count=0

while (True):
	count+=1
	os.system('python train.py')
#	time.sleep(60)
	print('COMPLETE %s' % count)
