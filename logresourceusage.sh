#!/bin/bash

echo "--------------------------------------------------------------------------------------"
date
echo "--------------------------------------------------------------------------------------"
# tty -s && tput....means to run tput only if the session is interactive and there is a terminal associated with it. So if you run the script in an interactive mode the tput will run, if you run it in a non-interactive mode the tput will not run
echo "             $(tty -s && tput setaf 2)System          Bitsendd$(tty -s && tput sgr0)    "
echo -e "$(tty -s && tput setaf 3)Memory usage:$(tty -s && tput sgr0)"`free -m | awk 'NR==2{printf "%.2f%%\t\t", $3*100/$2 }'`"         "`top -b -n 1| grep -w bitsendd | tr -s ' ' | cut -d ' ' -f 11`%
echo -e "$(tty -s && tput setaf 3)Disk usage  :$(tty -s && tput sgr0)"`df -h | awk '$NF=="/"{printf "%s\t\t", $5}'`
echo -e "$(tty -s && tput setaf 3)CPU usage   :$(tty -s && tput sgr0)"`top -bn1 | grep load | awk '{printf "%.2f%%\t\t\n", $(NF-2)}'`"          "`top -b -n 1| grep -w bitsendd | tr -s ' ' | cut -d ' ' -f 10`%
