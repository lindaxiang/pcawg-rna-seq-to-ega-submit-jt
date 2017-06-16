#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json
import subprocess

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      encrypted_file:
        type: string
        is_file: true
      encrypted_md5_file:
        type: string
        is_file: true
      unencrypted_md5_file:
        type: string
        is_file: true
      project_code:
        type: string
      submitter_sample_id:
        type: string
      data_type:
        type: string

"""
encrypted_file = task_dict.get('input').get('encrypted_file')
encrypted_md5_file = task_dict.get('input').get('encrypted_md5_file')
unencrypted_md5_file = task_dict.get('input').get('unencrypted_md5_file')
project_code = task_dict.get('input').get('project_code')
submitter_sample_id = task_dict.get('input').get('submitter_sample_id')
data_type = task_dict.get('input').get('data_type')

# composite the batch folder
if data_type.endswith('unaligned'):
    batch_folder = '.'.join(['unaligned', project_code, data_type.split('-')[0]])
else:
    batch_folder = '.'.join(['alignment', project_code, data_type.split('-')[0:1]])

src_base = os.path.dirname(encrypted_file)
des_base = os.path.join(batch_folder, submitter_sample_id)

task_start = int(time.time())

# do the real work here
try:
    r = subprocess.check_output(["ascp", '-k', '1', "-d", "--src-base="+src_base, encrypted_file, encrypted_md5_file, unencrypted_md5_file, "ega-box-358@fasp.ega.ebi.ac.uk:/"+des_base+"/"])
except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed


# complete the task
task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)

