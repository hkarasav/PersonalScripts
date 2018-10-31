#!/bin/bash

# Add a cron job for user babis in the cron jobs file by running the command:
# crontab -e
# check with: 
# crontab -l
#
# Add at the end of the cron file the line below to check every 10 minutes of every hour, day, week, month
# */10 * * * * /home/babis/watcherInnovad.sh >> /home/babis/watcherInnovad.log 2>&1
#
# The script is based in the assumption that 1) "babis" is the user that owns innovad 

echo ----------------------------------
echo --- $(date)

echo --- Running innovadWatcher

innovadpresent=$(ps aux | grep babis.*innovad | grep -v grep | grep -v watcher)

if [[ ${innovadpresent} == '' ]]; then
    echo "--- innovad not found in ps aux...restarting it -----------------------"
    /home/babis/innovad
    sleep 300
    ~/innovad walletpassphrase 'MNpasswordHere' 2
    ~/innovad masternode start all
    exit 1
elif [[ {innovadpresent} != "" ]]; then
    echo --- innovad found. All good...
else
    echo --- Something strange has happened
fi
