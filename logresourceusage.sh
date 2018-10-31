#!/bin/bash
# Use this file with: ./logresourceusage.sh >> logresourceusage.log &

stopat=$((SECONDS+93600))
while [ $SECONDS -lt $stopat ]
do

   echo "--------------------------------------------------------------------------------------"
   date
   echo "--------------------------------------------------------------------------------------"
   echo "             System          Bitsendd    "
   echo -e "Memory usage:"`free -m | awk 'NR==2{printf "%.2f%%\t\t", $3*100/$2 }'`"         "`top -b -n 1| grep -w bitsendd | tr -s ' ' | cut -d ' ' -f 11`%
   echo -e "Disk usage  :"`df -h | awk '$NF=="/"{printf "%s\t\t", $5}'`
   echo -e "CPU usage   :"`top -bn1 | grep load | awk '{printf "%.2f%%\t\t\n", $(NF-2)}'`"          "`top -b -n 1| grep -w bitsendd | tr -s ' ' | cut -d ' ' -f 10`%

sleep 2
done
