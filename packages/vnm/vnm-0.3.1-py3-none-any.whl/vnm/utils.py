import platform
import json
import os
from subprocess import PIPE, DEVNULL, Popen
def source(filename):
    if platform.system() == 'Linux':
        source_bash(filename)

def source_bash(filename):
    proc = Popen(f'source {filename};vnm dump-env --json', executable='/bin/bash', shell=True)
    stdout = proc.communicate()
    data = json.loads(stdout)
    os.environ.clear()
    os.environ.update(data)
