FROM python:alpine3.12

WORKDIR /root

RUN pip install ruamel.yaml
RUN wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.12.6/kubeseal-linux-amd64 -O kubeseal
RUN install -m 755 kubeseal /usr/local/bin/kubeseal
RUN rm kubeseal

COPY encrypt-values.py .
RUN chmod +x encrypt-values.py
VOLUME /root

ENTRYPOINT ["/usr/local/bin/python3", "-u", "encrypt-values.py"]

