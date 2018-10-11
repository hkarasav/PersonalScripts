#!/bin/bash

echo "--------------------------------------------------------------------------------------"
date
echo "--------------------------------------------------------------------------------------"
echo "             $(tput setaf 2)System          Magnetd$(tput sgr0)    "
echo -e "$(tput setaf 3)Memory usage:$(tput sgr0)"`free -m | awk 'NR==2{printf "%.2f%%\t\t", $3*100/$2 }'`"         "`top -b -n 1| grep -w magnetd | tr -s ' ' | cut -d ' ' -f 10`%
echo -e "$(tput setaf 3)Disk usage  :$(tput sgr0)"`df -h | awk '$NF=="/"{printf "%s\t\t", $5}'`
echo -e "$(tput setaf 3)CPU usage   :$(tput sgr0)"`top -bn1 | grep load | awk '{printf "%.2f%%\t\t\n", $(NF-2)}'`"          "`top -b -n 1| grep -w magnetd | tr -s ' ' | cut -d ' ' -f 9`%
