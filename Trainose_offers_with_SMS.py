# I drafted this script to get SMS notifications of offers from the Greek public train transportation system.
# It utilises a free feature provided by the Greek mobile operator Cosmote, that when you receive an email in your Cosmote account then an SMS is sent free of chanrge to your mobile phone.

import urllib
import json
import time
import smtplib
import sys
import os
from threading import Timer, Lock
# import threading

# Need to Install Python
# Need to get gmail application password
# Need to have Cosmote as a mobile operator and use their free service to send you an SMS when you receive an email.
# http://mail.mycosmos.gr/mycosmos/MyCosmos.aspx
# <yourmobilenumber>@mycosmos.gr
# Might need to send sms to 54000 with "START" to begin sending sms for each email received
# For details check http://mail.mycosmos.gr/mycosmos/Terms%20and%20Conditions.htm

print "Departure from:"
print "1) Athens"
print "2) Thessaloniki"
departure = raw_input()

# Define variables for the correct syntax of the URL query
if departure == '1':
    # ATHENS
    apo = '%CE%91%CE%98%CE%97%CE%9D'
    # THESSALONIKI
    eos = '%CE%98%CE%95%CE%A3%CE%A3'
elif departure == '2':
    # THESSALONIKI
    apo = "%CE%98%CE%95%CE%A3%CE%A3"
    # ATHENS
    eos = "%CE%91%CE%98%CE%97%CE%9D"

date = raw_input("Departure date (YYYY-MM-DD): ")
rtn_date = raw_input("Return date (YYYY-MM-DD): ")

request = 'https://tickets.trainose.gr/dromologia/ajax.php?c=dromologia&op=vres_dromologia&apo=' + apo + '&pros=' + eos + '&date=' + date + '&rtn_date=' + rtn_date + '&travel_type=2&trena[]=apla&trena[]=ic&trena[]=ice&trena[]=bed&time=23%3A59&time_type=anaxwrhsh&rtn_time=23%3A59&rtn_time_type=anaxwrhsh'

print request

# Define monitored travel times
while True:
    try:
        travel_times_read = json.loads(urllib.urlopen(request).read())
        break
    except:
        print "Network connection problem...In 5 seconds another attempt shall be made"
        time.sleep(5)

print "Pick travel route during transition e.g. 0,3,4"
for trip_time in range(0,len(travel_times_read['data']['transition'])):
    print trip_time, ") " + travel_times_read['data']['transition'][trip_time]['segments'][0]['wra1']

chosen_times_d=[int(x) for x in raw_input().split(',')]
print chosen_times_d

print "...and also for the return route e.g. 2,3,6"
for trip_time in range(0,len(travel_times_read['data']['return'])):
    print trip_time, ") " + travel_times_read['data']['return'][trip_time]['segments'][0]['wra1']

chosen_times_r=[int(x) for x in raw_input().split(',')]
print chosen_times_r

def send_email(To_address, subject, message_body):
    import smtplib

    gmail_user = "myemail@gmail.com"

    # To generate application-specific pwd go to
    # https://accounts.google.com/b/0/IssuedAuthSubTokens#accesscodes
    # and request one from google
    # No need to memorize it
    gmail_pwd = "password"
    FROM = 'myemail@gmail.com'
    print "Setup ok!"

    # Prepare actual message
    server_message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(To_address), subject, message_body)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.ehlo()
        server.login(gmail_user,gmail_pwd)
        server.sendmail(FROM, To_address, server_message)
        server.close()
        print 'Successfully sent the mail'
    except:
        print "For some reason (connectivity/SMTP server failure) failed to send mail"

def find_offers(GET_for_trainose):

    while True:
        try:
            data = json.loads(urllib.urlopen(GET_for_trainose).read())
            break
            print "Exec flow moves here!"
        except:
            print "Problem with the connection to the server...trying again in 10secs"
            time.sleep(10)
    departure_offers_exist=False
    return_offers_exist=False
    
    transition_route=[]
    transition_route_time=[]
    transition_offers={}
    
    return_route=[]
    return_route_time=[]
    return_offers={}
    
    for x in chosen_times_d:
        transition_route.append(data['data']['transition'][x]['segments'][0]['offers']['b'])
        transition_route_time.append(data['data']['transition'][x]['segments'][0]['wra1'])
        print 'Departure:', transition_route_time[(len(transition_route_time)-1)]
        print transition_route[(len(transition_route)-1)], '\n'
        # Prosfores ton 29, 19, 9 euro antistoixa einai '5', '4', '3'. Gia elegxo mono sta 9 euro einai '3'
        if any(c in transition_route[len(transition_route)-1] for c in ('3')):
            print "FOUND OFFER IN DEPARTURE"
            transition_offers[transition_route_time[len(transition_route)-1]]=transition_route[len(transition_route)-1]
            departure_offers_exist = True

    for y in chosen_times_r:
        return_route.append(data['data']['return'][y]['segments'][0]['offers']['b'])
        return_route_time.append(data['data']['return'][y]['segments'][0]['wra1'])
        print 'Return:', return_route_time[(len(return_route_time)-1)]
        print return_route[(len(return_route)-1)], '\n'
        # Prosfores ton 29, 19, 9 euro antistoixa einai '5', '4', '3'. Gia elegxo mono sta 9 euro einai '3'
        if any(c in return_route[len(return_route_time)-1] for c in ('3')):
            print "FOUND OFFER IN RETURN"
            return_offers[return_route_time[len(return_route_time)-1]]=return_route[len(return_route_time)-1]
            return_offers_exist = True

#def check_for_offers(chosen_times, direction) #Either 'transition' or 'return'
#    for x in chosen_times:
#        dromologio.append(data['data'][direction][x]['segments'][0]['offers']['b'])
#        ora_dromol.append(data['data'][direction][x]['segments'][0]['wra1'])
#        print direction, ': ', ora_dromol[(len(ora_dromol)-1)]
#        print dromologio[(len(dromologio)-1)], '\n'
#        if any(c in dromologio[len(dromologio)-1] for c in ('3')):
#            print "FOUND OFFER IN " + direction
#        ???    transition_offers[transition_route_time[len(transition_route)-1]]=transition_route[len(transition_route)-1]
#        ???    departure_offers_exist = True

    if departure_offers_exist == True or return_offers_exist == True: # and wait_timer == False:
        send_email(['6936181961@mycosmos.gr'], 'Departure:' + str(sorted(transition_offers)) + '  Return:' + str(sorted(return_offers)) , 'Prosfores')
        sys.exit(0)
        # Address to send email: 6936181961@mycosmos.gr

serial = 1
while True:
    os.system('cls')
    print "'5'=29 euro, '4'=19 euro, '3'=9 euro...Monitoring for '3' only"
    print "Request SN:", serial
    find_offers(request)
    time.sleep(60)
    serial = serial + 1
