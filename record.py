from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
import time

THRESHOLD = 500
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
#RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "recorded.wav"

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in xrange(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in xrange(int(seconds*RATE))])
    return r

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("RECORDING...")

silent_time = 0
num_silent = 0
wait_count = 0
snd_started = False

r = array('h')

while 1:
    # little endian, signed short
    snd_data = array('h', stream.read(CHUNK))
    if byteorder == 'big':
        snd_data.byteswap()
    r.extend(snd_data)

    silent = is_silent(snd_data)

    if not snd_started:
		if wait_count == 0:
			start = time.time()
		else:
			end = time.time()
			silent_time += end - start
		
			if silent_time > 10:
				print("WAITED TOO LONG!")
				break

			start = time.time()

		wait_count += 1
        
    if not silent and not snd_started:
        snd_started = True

    if snd_started:
		if silent:
			num_silent += 1
		
		if num_silent > 30:
			print("DONE RECORDING!")
			break

stream.stop_stream()
stream.close()
p.terminate()

r = normalize(r)
r = trim(r)
r = add_silence(r, 0.5)

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(pack('<' + ('h'*len(r)), *r))
wf.close()

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import sugartensor as tf
import recognize_module
import data

print('Recognizing...')
data.print_index(recognize_module.recognize('recorded.wav'))
