#!/bin/bash

docker build -t msvcbench/microservice_v2:latest .
docker push msvcbench/microservice_v2:latest

echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"

docker build -f Dockerfile.debug -t msvcbench/microservice_v2-ssh:latest .
docker push msvcbench/microservice_v2-ssh:latest
