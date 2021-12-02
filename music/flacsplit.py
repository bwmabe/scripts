import os
import sys

from shutil import copyfile
from subprocess import Popen, run, PIPE, STDOUT

class FLACCUE:
    def __init__(self, location):
        split = location.split('/')
        self.path = ('/').join(split[0:-1])
        self.file = split[-1]
        self.cue = self.find_cue()

    def find_cue(self):
        for file in os.listdir(self.path):
            if file.split('.')[-1] == 'cue':
                return file.split('/')[-1]

    def split(self):
        root = os.getcwd()
        os.chdir(self.path)
        split_cmd = ['shnsplit', '-f', self.cue, '-o', 'flac', '-t', '%n - %t', self.file]
        run(split_cmd)
        os.rename(self.file, ''.join(self.file.split('.')[0:-1]) + ".bak")
        tag_cmd = ['cuetag.sh', self.cue]
        for f in find_all_flacs(multifile=True):
            if '00 - pregap' not in f:
                tag_cmd.append(f)
        run(tag_cmd)
        os.chdir(root)

    def __str__(self):
        return f'{self.path}\n\t{self.file}\n\t{self.cue}'


def find_all_flacs(start_dir='.', multifile=False):
    tree = list()
    for root, branches, leaves in os.walk(start_dir):
        for leaf in leaves:
            tree.append(os.path.join(root, leaf))
    all_flacs = dict()
    for file in tree:
        key = '/'.join(file.split('/')[0:-1])
        ext = file.split('.')[-1]
        if ext == 'flac':
            if key in all_flacs.keys():
                all_flacs[key].append(file)
            else:
                all_flacs[key] = [file]
    single_flacs = list()
    for key, values in all_flacs.items():
        if len(values) == 1:
            single_flacs.append(values[0])
        elif multifile:
            for flac in values:
                single_flacs.append(flac)
    return single_flacs


flacs = [FLACCUE(f) for f in find_all_flacs()]
for flac in flacs:
    flac.split()
