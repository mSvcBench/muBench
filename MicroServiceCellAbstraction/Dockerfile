FROM python:slim

RUN apt update
COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 51313

COPY CellController.py ExternalServiceExecutor.py InternalServiceExecutor.py mss.proto mss_pb2.py \
mss_pb2_grpc.py start.sh ./

CMD [ "/usr/local/bin/python3", "/app/CellController.py"]
