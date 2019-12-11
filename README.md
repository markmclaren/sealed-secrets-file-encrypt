Use Python (I experimented with Go but it isn't very good at dealing with dyncamic types.  Can use yaml2go but that only gets you so far.
----
Read YAML file
Iterate YAML
Detected "DEC()" strings
Execute "kubeseal raw" to encrypt strings and write them back to the YAML


---
 ./encrypt-values.py -f values-prod._unencrypted_yaml > values-prod.yaml
 ./encrypt-values.py -f values-dev._unencrypted_yaml > values-dev.yaml

 helm template -f values-prod.yaml ./sealed-secrets-encrypted-file-example
 helm template -f values-dev.yaml ./sealed-secrets-encrypted-file-example