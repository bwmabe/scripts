import os
import sys

from mutagen.flac import FLAC

class Song:
    def __init__(self, filepath):
        print(f"\treading: {filepath}")
        self.flac = FLAC(filepath)

    def get_artist(self):
        return self.flac['artist'][0]

    def set_artist(self, artist):
        self.flac['artist'] = [artist]

    def fix_artist(self, correct_artist):
        if self.get_artist() != correct_artist:
            print(f"'{self.get_artist()}' -> '{correct_artist}'")
            self.set_artist(correct_artist)


def get_music(directory, filetype=None):
    files = list()
    print(f"Finding songs in {directory}")
    for path, subdirs, items in os.walk(directory):
        for item in items:
            if not filetype or filetype in item:
                files.append(os.path.join(path, item))
    print("Done!")
    return files


def find_all(directory, filetype=None, constructor=FLAC):
    return [constructor(song) for song in get_music(directory, filetype)]


def main(path, filetype, artist):
    for s in find_all(path, filetype=filetype, constructor=Song):
        s.fix_artist(artist)


main(sys.argv[1], sys.argv[2], sys.argv[3])
