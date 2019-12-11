# sealed-secrets-encrypted-file
### Proof of concept

I am trying to get [Helm](https://helm.sh/) and [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) working nicely together.  

I got some ideas from [StackOverflow: How to use Kubeseal to seal a helm-templated secret?
](https://stackoverflow.com/questions/58161224/how-to-use-kubeseal-to-seal-a-helm-templated-secret).  However, I didn't want to be manually running Kubeseal everytime I updated a secret - so I thought I would create a script to encrypt the values.yaml files in a similar way to Puppet's [heira-eyaml](https://github.com/voxpupuli/hiera-eyaml) and the [jasypt-maven-plugin](https://github.com/ulisesbocchio/jasypt-spring-boot/tree/master/jasypt-maven-plugin).

I initally tried to write the script in Go (using [yaml2go](https://github.com/PrasadG193/yaml2go)) but Go doesn't work very well with Yaml files where the structures are not known ahead of time so I gave up and wrote it in Python instead.

The python script does the following:

* Read YAML file
* Iterate YAML
* Detect "DEC(password)" strings
* Execute "kubeseal raw" to encrypt strings and write them back to the YAML
* Inject the encrypted values back into the appropriate part of the YAML

## Pre-requirements

* a working instance of Kubernetes
* a working instance of the Sealed Secrets controller
* a working copy of the kubeseal command line script
* Python 3 installed
* Python library [ruamel.yaml](https://yaml.readthedocs.io/en/latest/install.html) installed

I am wrote and am using this on Windows but inside the WSL Ubuntu.  I couldn't get kubeseal working in a Windows/DOS command line terminal.

```
./encrypt-values.py -f values-prod.unencrypted_yaml > values-prod.yaml
./encrypt-values.py -f values-dev.unencrypted_yaml > values-dev.yaml

helm template -f values-prod.yaml ./sealed-secrets-encrypted-file-example
helm template -f values-dev.yaml ./sealed-secrets-encrypted-file-example
```

 Disclaimer: I don't write much Python so I'm sure the script could be much better if I knew what I was doing.