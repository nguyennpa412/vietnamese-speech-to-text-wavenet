#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import re
from collections import Counter
from decimal import Decimal, getcontext
getcontext().prec = 20

letters = [ 'a', 'á', 'à', 'ả', 'ã', 'ạ',
            'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ',
            'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ',
            'b', 'c', 'd', 'đ',
            'e', 'é', 'è', 'ẻ', 'ẽ', 'ẹ',
            'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ',
            'f', 'g', 'h',
            'i', 'í', 'ì', 'ỉ', 'ĩ', 'ị',
            'j', 'k', 'l', 'm', 'n',
            'o', 'ó', 'ò', 'ỏ', 'õ', 'ọ',
            'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ',
            'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ',
            'p', 'q', 'r', 's', 't',
            'u', 'ú', 'ù', 'ủ', 'ũ', 'ụ',
            'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự',
            'v', 'w', 'x',
            'y', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ',
            'z' ]

def words(text): return re.findall(r'\w+', text.decode('utf-8').lower(), re.UNICODE)

WORDS = Counter(words(open('vnexpress_500.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return Decimal(WORDS[word]) / Decimal(N)

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    N = sum(WORDS.values())
    if (WORDS[word] < N // 1000000):
        return (known(edits1(word)) or known(edits2(word)) or [word])
    else:
        return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    # print('splits', splits)
    deletes    = [L + R[1:]               for L, R in splits if R]
    # print('deletes', deletes)
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    # print('transposes', transposes)
    replaces   = [L + c.decode('utf-8') + R[1:]           for L, R in splits if R for c in letters]
    # print('replaces', replaces)
    inserts    = [L + c.decode('utf-8') + R               for L, R in splits for c in letters]
    # print('inserts', inserts)
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def get_best_word(word):
    return correction(word.decode('utf-8'))

def get_best_sentence(sentence):
    words = sentence.split(' ')
    res = []
    for word in words:
        if (word):
            best_word = get_best_word(word)
            res.append(best_word)
    res = ' '.join(res)
    return res

def print_result(word):
    cands = candidates(word.decode('utf-8'))
    print('Candidates:')
    for i in cands:
        print(i + ' ' + str(P(i)))
    print('\nCorrection:\n' + correction(word.decode('utf-8')) + '\n')

def print_result_sentence(sentence):
    words = sentence.split(' ')
    for word in words:
        print_result(word)