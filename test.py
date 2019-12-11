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
            data[key] = val # replace value
            print(val)
            # https://stackoverflow.com/questions/9393425/python-how-to-execute-shell-commands-with-pipe
            # echo -n <secret-password> | kubeseal --raw --scope namespace-wide --from-file=/dev/stdin

            #p1 = subprocess.Popen(["echo", "-n", val], stdout=subprocess.PIPE)
            #p2 = subprocess.Popen(["kubeseal", "--raw",  "--scope",  "namespace-wide", "--from-file=/dev/stdin"], stdin=p1.stdout, stdout=subprocess.PIPE)
            #p2.communicate()
            #print("OUTPUT: " + p2.stdout.read().decode("utf-8") )

            mycmd=subprocess.getoutput('echo -n {} | kubeseal --raw --scope namespace-wide --from-file=/dev/stdin'.format(val))
            print(mycmd)

            #result = subprocess.run(['ls'], capture_output=True)
            #print(result.stdout)
    print('\n')
yaml.dump(data, sys.stdout)
