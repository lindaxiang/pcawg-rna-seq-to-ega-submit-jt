#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json, get_md5

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      file:  # new field
        type: string
        is_file: true
      file_md5sum:
        type: string
"""
file_ = task_dict.get('input').get('file')
file_md5sum = task_dict.get('input').get('file_md5sum')

task_start = int(time.time())

# do the real work here
# get the md5sum for the input file
check_sum = get_md5(file_)
if not check_sum: 
    task_info = 'Error: file does not exist'
elif not check_sum == file_md5sum: 
    task_info = 'Error: mismatch file_md5sum'
else: 
    task_info = 'Pass md5sum check'


# complete the task
task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    },
    'task_info': task_info
}

save_output_json(output_json)

if task_info.startswith('Error'):
    sys.exit(1)

