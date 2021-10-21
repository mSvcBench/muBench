#!/bin/bash

# script used to build the container of the service-cell
# change the repository msvcbench to one that you can access
# debug version run the main process of the service-cell within a screen so that you can enter the container and the screen to debug 

docker build -t msvcbench/microservice_v2:latest .
docker push msvcbench/microservice_v2:latest

echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"

docker build -f Dockerfile.debug -t msvcbench/microservice_v2-screen:latest .
docker push msvcbench/microservice_v2-screen:latest

echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"

docker build -f Dockerfile-mp.debug -t msvcbench/microservice_v3-screen:latest .
docker push msvcbench/microservice_v3-screen:latest
