#!/usr/bin/env python3

import argparse
import secrets
import base64
import sys
import re

from typing import List

def load_words() -> List[str]:
    word_regex = re.compile('^[a-zA-Z][a-z]+$')
    words = []
    with open('/usr/share/dict/words', 'r') as source_file:
        words_raw = source_file.read().split('\n')
        for word in words_raw:
            if word_regex.match(word):
                words.append(word)
    return words


def gen_from_list(word_list: List[str], words=3, min_length=16, max_length=64,
                  length=0) -> str:
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


def gen_from_words(wc=16) -> str:
    return gen_from_list(load_words(), )


def charlen_to_bytes(charlen: int) -> int:
    charlen = charlen - (charlen % 4)
    return int(charlen / 4) * 3


# 3 bytes = 4 chars
def gen_from_bytes(length=16) -> str:
    b = charlen_to_bytes(length)
    pw = base64.b64encode(secrets.token_bytes(b), b'!+').decode()
    while len(pw) < length:
        padding = base64.b64encode(secrets.token_bytes(b), b'!+').decode()
        pw += secrets.choice(padding)
    return pw


def main(argv: list) -> None:
    parser = argparse.ArgumentParser(description="Generates Random Passwords")
    parser.add_argument('cmd', metavar='TYPE_OF_PASSWORD', type=str, 
                        help="type of password to generate")
    parser.add_argument('--length', metavar='LENGTH', type=int, nargs=1, required=False,
                        help="lenght of the password in characters")
    args = parser.parse_args(argv)

    actions = {'words': gen_from_words, 'chars': gen_from_bytes}

    if args.cmd not in actions.keys():
        print("gen-password: error: not a valid type of password")
        exit(1)

    if args.length:
        print(actions[args.cmd](args.length[0]), end="")
    else:
        print(actions[args.cmd](), end="")

if __name__ == "__main__":
    main(sys.argv[1:])

# vi:syntax=python
