#!/bin/bash
set -e

echo "---------------------------------------------------"

balance=`~/innova-cli getbalance`
margintosend=1005
echo margintosend=$margintosend

currentbalance=`echo "${balance:0:4}"`
echo currentbalance=$currentbalance
innovatotransfer=`expr $currentbalance - $margintosend`
echo innovatotransfer=$innovatotransfer

if [ ${innovatotransfer} -gt 40 ]
then
   echo ${innovatotransfer} Innova to transfer exist
   ~/innova-cli walletpassphrase '<MNpasswordHere>' 2
   ~/innova-cli sendfrom <account> <exchangeAddress> ${innovatotransfer}
   echo `date`
   cat /dev/null > ~/.bash_history && history -c && exit
else
   echo No Innova to send. At least 40 should be available
fi

echo `date`
