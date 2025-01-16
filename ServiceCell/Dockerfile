FROM python:3.8-slim-buster

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8080
EXPOSE 51313

COPY CellController-mp.py ExternalServiceExecutor.py InternalServiceExecutor.py mub.proto mub_pb2.py \
mub_pb2_grpc.py gunicorn.conf.py start-mp.sh ./

CMD [ "/usr/local/bin/python3", "/app/CellController-mp.py"]

