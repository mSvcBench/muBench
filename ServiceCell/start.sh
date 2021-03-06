#!/bin/bash

# note that the process of the service-cell (CellController.py) is run within a screen for easier debugging
# this may impair kubernetes ability to detect failures because CellController.py may crash within the screen without closing container   

/usr/bin/screen -S service -s /bin/bash -t win0 -A -d -m
screen -S service -p win0 -X stuff $'prometheus_multiproc_dir=/app /usr/local/bin/python3 /app/CellController.py \n'
sleep infinity