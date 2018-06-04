import matplotlib.pyplot as plt
import librosa.display

wave_file = './asset/data/vais/train/audio/11.wav'

wave, sr = librosa.load(wave_file, mono=True, sr=None)
# re-sample ( 48K -> 16K )
#wave = wave[::3]

# get mfcc feature
mfcc = librosa.feature.mfcc(wave, sr=16000)

plt.figure(figsize=(10,4))
librosa.display.specshow(mfcc,x_axis='time')
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()
plt.show()