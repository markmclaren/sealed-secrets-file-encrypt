#!/usr/bin/python3

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
            print(val)
            # https://stackoverflow.com/questions/58161224/how-to-use-kubeseal-to-seal-a-helm-templated-secret
            # https://stackoverflow.com/questions/9393425/python-how-to-execute-shell-commands-with-pipe
            # echo -n <secret-password> | kubeseal --raw --scope namespace-wide --from-file=/dev/stdin
            encryptedValue=subprocess.getoutput('echo -n {} | kubeseal --raw --scope namespace-wide --from-file=/dev/stdin'.format(val))
            print(encryptedValue)
            data[key] = encryptedValue # replace value
    print('\n')
yaml.dump(data, sys.stdout)
