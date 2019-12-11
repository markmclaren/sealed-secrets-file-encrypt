#!/usr/bin/python3

import sys
import ruamel.yaml
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", required=True, type=str, help="Filename")

args = parser.parse_args()
filename = args.f

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
with open(filename) as fp:
    data = yaml.load(fp)
for key in data:
    val = data.get(key)
    if isinstance(val, str):
        if val.startswith('DEC(') & val.endswith(')'):
            val = val.replace("DEC(", "", 1)  # remove first instance of prefix
            val = val[:val.rfind(")")] # remove suffix
            # https://stackoverflow.com/questions/58161224/how-to-use-kubeseal-to-seal-a-helm-templated-secret
            # https://stackoverflow.com/questions/9393425/python-how-to-execute-shell-commands-with-pipe
            # echo -n <secret-password> | kubeseal --raw --scope namespace-wide --from-file=/dev/stdin
            encryptedValue=subprocess.getoutput('echo -n {} | kubeseal --raw --scope namespace-wide --from-file=/dev/stdin'.format(val))
            data[key] = encryptedValue # replace value
yaml.dump(data, sys.stdout)
