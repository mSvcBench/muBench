FROM python:3.8-slim-buster

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install gunicorn


COPY CellController-mp.py ExternalServiceExecutor.py InternalServiceExecutor.py mub.proto mub_pb2.py \
mub_pb2_grpc.py gunicorn.conf.py start-mp.sh /app/

EXPOSE 8080
EXPOSE 51313

ENV prometheus_multiproc_dir=/app 
CMD ["/bin/bash", "start-mp.sh"]

