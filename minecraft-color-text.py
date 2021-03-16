#!/usr/bin/env python3

import sys


def get_color(color):
    colors = ["red",           # 0
              "gold",          # 1
              "yellow",        # 2
              "green",         # 3
              "blue",          # 4
              "dark_purple",   # 5
              "light_purple"]  # 6

    return "\"color\":\"{}\"".format(colors[color])


def main():
    color_index = 0
    word_index = 0

    string = "["

    for word in sys.argv[1:]:
        for char in word:
            string += "{\"text\":\"%s\",%s}," % (char, get_color(color_index))
            if color_index < 6:
                color_index += 1
            else:
                color_index = 0
        if word_index < (len(sys.argv) - 2):
            string += "{\"text\":\" \"},"
            word_index += 1

    string = string[:-1] + "]"

    print(string)


main()
