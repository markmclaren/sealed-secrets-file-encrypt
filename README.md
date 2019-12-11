Use Python (I experimented with Go but it isn't very good at dealing with dyncamic types.  Can use yaml2go but that only gets you so far.
----
Read YAML file
Iterate YAML
Detected "DEC()" strings
Execute "kubeseal raw" to encrypt strings and write them back to the YAML


---
 ./encrypt-values.py > values.eyaml
 helm template -f values.eyaml ./sealed-secrets-encrypted-file-example