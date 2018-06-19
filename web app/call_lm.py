import sys
from correct_spell import get_best_sentence

filetype = sys.argv[1]

res_wavenet = open('res_wavenet_%s.txt' % filetype, 'r')
output = res_wavenet.readline()
res_wavenet.close()

print('\n Correcting ... \n')

correctedOutput = get_best_sentence(output).encode('utf-8')

print('\n Corrected by Language Model: \n' + correctedOutput + '\n')

outputfile = open('res_lm_%s.txt' % filetype, 'w')
outputfile.write(correctedOutput)
outputfile.close()