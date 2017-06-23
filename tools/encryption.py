#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
import subprocess
from utils import get_task_dict, save_output_json
import gzip
import shutil

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      input_file:
        type: string
        is_file: true
"""
input_file = task_dict.get('input').get('input_file')

task_start = int(time.time())

# gzip xml file
if input_file.endswith('xml'):
    try:
        file_dir = os.path.dirname(input_file)
        file_name = os.path.basename(input_file)
        filename = '.'.join(['analysis', file_name.rstrip('.xml'), 'GNOS', 'xml', 'gz'])
        with open(input_file, 'rb') as f_in, gzip.open(os.path.join(file_dir, filename), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        input_file = os.path.join(file_dir, filename)
    except Exception, e:
        with open('jt.log', 'w') as f: f.write(str(e))
        sys.exit(1)  # task failed    

try:
    r = subprocess.check_output(['java', '-jar', os.environ['EGA_CRY_JAR']+'/EgaCryptor.jar', '-file', input_file])
except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed


# complete the task
task_stop = int(time.time())

"""
    output:
      encrypted_file:
        type: string
        is_file: true
      encrypted_md5_file:
        type: string
        is_file: true
      unencrypted_md5_file:
        type: string
        is_file: true
"""

output_json = {
    'encrypted_file': input_file+'.gpg',
    'encrypted_md5_file': input_file+'.gpg.md5',
    'unencrypted_md5_file': input_file+'.md5',
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
