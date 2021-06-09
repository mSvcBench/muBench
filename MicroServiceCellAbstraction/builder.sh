#!/bin/bash

docker build -t lucapetrucci/microservice_v2:latest .
docker push lucapetrucci/microservice_v2:latest

echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"

docker build -f Dockerfile.debug -t lucapetrucci/microservice_v2-ssh:latest .
docker push lucapetrucci/microservice_v2-ssh:latest
