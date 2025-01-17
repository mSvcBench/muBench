#!/bin/bash
req=600
echo "##### Starting with ${req} requests #####"
for i in 1 10 20 30 40 50 64
do 
  jmeter -n -t jmeter/jmeter-trace.jmx -Japp_num=18 -Jtrace_num=962 -Jusers=${i} -l autscaler_flat${req}_${i}us.csv
  #rm autscaler_flat${req}_${i}us.csv
  echo "Sleep 10..."
  sleep 10
done
echo "##### Ending ${req} requests #####"
