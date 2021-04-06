#!/usr/bin/env python3

import secrets
import base64
import re


def load_words():
    word_regex = re.compile('^[a-zA-Z][a-z]+$')
    words = []
    with open('/usr/share/dict/words', 'r') as source_file:
        words_raw = source_file.read().split('\n')
        for word in words_raw:
            if word_regex.match(word):
                words.append(word)
    return words


def gen_from_list(word_list, words=3, min_length=16, max_length=64, length=0):
    valid_password = False
    iterations = 0
    password = ''
    if length != 0:
        max_length = length
        min_length = length
    while(not valid_password): 
        for i in range(0, words):
            if i == 0:
                password += secrets.choice(word_list)
            else:
                password += secrets.choice(word_list).capitalize()
        if len(password) < min_length:
            password += secrets.choice(word_list).capitalize()
        elif len(password) <= max_length:
            valid_password = True
        else:
            password = ''
        iterations += 1
    return password


def charlen_to_bytes(charlen):
    charlen = charlen - (charlen % 4)
    return int(charlen / 4) * 3


# 3 bytes = 4 chars
def gen_from_bytes(length=16):
    b = charlen_to_bytes(length)
    pw = base64.b64encode(secrets.token_bytes(b), b'!+').decode()
    while len(pw) < length:
        padding = base64.b64encode(secrets.token_bytes(b), b'!+').decode()
        pw += secrets.choice(padding)
    return pw

p = gen_from_bytes(32)
print(p, len(p))
print(gen_from_list(load_words(), words=4, length=32))
