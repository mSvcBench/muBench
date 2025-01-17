#!/bin/bash

# script used to build the container of the service-cell
# change the repository msvcbench to one that you can access
# debug version run the main process of the service-cell within a screen so that you can enter the container and the screen to debug 

echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"
echo "----------------------------------------------------------------"

docker build . -f Dockerfile -t msvcbench/microservice:latest
docker push msvcbench/microservice:latest

docker build . -f Dockerfile-mp-screeen.debug -t msvcbench/microservice-screen:latest
docker push msvcbench/microservice-screen:latest
