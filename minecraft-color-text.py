#!/usr/bin/env python3

import sys

def get_color(color):
    #         1      2       3         4        5       6              7
    colors = ["red", "gold", "yellow", "green", "blue", "dark_purple", "light_purple"]
    return "\"color\":\"" + colors[color] + "\"" 

def main():
    opener = "["
    prefix = "{\"text\":\""
    joiner = "\","
    suffix = "},"
    closer = "]"

    c_index = 0

    string = opener

    # Ignore the name of the program in sys.argv
    program_name = True

    for i in sys.argv:
        if not program_name:
            for j in i:
                string += prefix + j + joiner + get_color(c_index) + suffix
                if c_index < 6:
                    c_index += 1
                else:
                    c_index = 0
            string += "{\"text\":\" \"},"

        program_name = False

    string = string[:-1] + closer

    print(string)

main()
