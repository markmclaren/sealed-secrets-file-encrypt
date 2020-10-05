# sealed-secrets-encrypted-file
### Proof of concept

I am working with Kubernetes.  I am trying to get [Helm](https://helm.sh/) and [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) working nicely together.  

I got some ideas from [StackOverflow: How to use Kubeseal to seal a helm-templated secret?
](https://stackoverflow.com/questions/58161224/how-to-use-kubeseal-to-seal-a-helm-templated-secret)  However, I do not want to be manually running Kubeseal (sealed-secrets client) everytime I update a secret - so I thought I would create a script to encrypt the values.yaml files in a similar way to Puppet's [heira-eyaml](https://github.com/voxpupuli/hiera-eyaml) and the [jasypt-maven-plugin](https://github.com/ulisesbocchio/jasypt-spring-boot#maven-plugin).

I initally tried to write the script in Go (using [yaml2go](https://github.com/PrasadG193/yaml2go)) but Go doesn't seem to work very well currently with Yaml files where the structures are not known ahead of time, so I gave up and wrote it in Python instead.

The python script does the following:

* Read YAML file
* Iterate YAML
* Detect "DEC(password)" placeholder strings
* Execute "kubeseal raw" to encrypt strings and write them back to the YAML
* Inject the encrypted values back into the appropriate part of the YAML

## Pre-requirements

* a working instance of Kubernetes
* a working instance of Helm
* a working instance of the Sealed Secrets controller
* a working copy of the kubeseal command line script
* Python 3 installed
* Python library [ruamel.yaml](https://yaml.readthedocs.io/en/latest/install.html) installed

I wrote this script on a Windows 10 Pro laptop running WSL Ubuntu.  I couldn't get kubeseal working in a Windows command line terminal environment.


## Encryption

The tool transforms a values.yaml file containing unencrypted values (maybe with a file extension that can be added to .gitignore like unencrypted_yaml):

```
foo: DEC(bar)
```

to something that can be committed to git like:

```
foo: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq.....
```

More examples of usage:

```
./encrypt-values.py -f values-prod.unencrypted_yaml > values-prod.yaml
./encrypt-values.py -f values-dev.unencrypted_yaml > values-dev.yaml
```

To see the Helm template with the encrypted values in place try:

```
helm template -f values-prod.yaml ./sealed-secrets-encrypted-file-example
helm template -f values-dev.yaml ./sealed-secrets-encrypted-file-example
```

 Disclaimer: I don't write much Python so I'm sure the script could be much better if I knew what I was doing.

## Updated

I added support for supplying the public key as a parameter.  This means you no longer need to have direct access to Kubernetes to seal keys (you only need to public key that the sealed secrets controller uses - this usually changes pretty often).

I have added Dockerfile and docker-compose files.  I also added a test public key (snakeoil.pem) for demonstration purposes.

Build the image using docker-compose:

```
docker-compose build
```

Run the image, you should see the usage output.

```
# docker-compose run sealed-secrets-encrypt

Creating sealed-secrets-file-encrypt_sealed-secrets-encrypt_run ... done
usage: encrypt-values.py [-h] -f F -k K
encrypt-values.py: error: the following arguments are required: -f, -k
```


You can then run the image like this:
```
# docker-compose run sealed-secrets-encrypt -f values-prod.unencrypted_yaml -k snakeoil.pem > values-prod.yml
```

Alternatively uncomment the f and k command parameters in the docker-compose.yml file, it would then work like this:
```
docker-compose run sealed-secrets-encrypt > values-prod.yml
```