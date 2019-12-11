#!/usr/bin/python

import sys
import ruamel.yaml
import subprocess

yaml = ruamel.yaml.YAML()
# yaml.preserve_quotes = True
with open('values.yaml') as fp:
    data = yaml.load(fp)
for key in data:
    val = data.get(key)
    print(key)
    print(val)
    print(isinstance(val, str))
    if isinstance(val, str):
        if val.startswith('DEC(') & val.endswith(')'):
            val = val.replace("DEC(", "", 1)  # remove first instance of prefix
            val = val[:val.rfind(")")] # remove suffix
            data[key] = val # replace value
            print(val)
            result = subprocess.run(['ls'], capture_output=True)
            print(result.stdout)
    print('\n')
yaml.dump(data, sys.stdout)
