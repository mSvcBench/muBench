#!/bin/bash

# Debug
service ssh start

/usr/bin/screen -S service -s /bin/bash -t win0 -A -d -m
screen -S service -p win0 -X stuff $'/usr/local/bin/python3 /app/ServiceController.py \n'

sleep infinity