import os
import sys

from subprocess import Popen, run, PIPE, STDOUT

files = list() 
for root, branches, leaves in os.walk('.'):
    for leaf in leaves:
        files.append(os.path.join(root, leaf))

for file in files:
    if '.ape' in file:
        cmd = ['ffmpeg', '-y', '-i', file, file.split('.ape')[0] + '.flac']
        success = False
        try:
            print(' '.join(cmd))
            conversion_job = run(cmd, capture_output=True, check=True)
            success = True
        except Exception as err:
            print("----\nUnknown Error\n--")
            print(err)
            print("--\nCommand was:")
            print(' '.join(cmd))
            print("----")
        if success:
            del_cmd = ['rm', file]
            deletion_job = run(del_cmd, capture_output=True, check=True)

