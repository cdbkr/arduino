import os
import smtplib
import sys
import serial
import string
import threading
import time

from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate
from email.mime.text import MIMEText
from decimal import *
from time import sleep

WELCOME_MESSAGE = "\n\n-----------Temperature Email Alarm with Arduino-----------"

ARDUINO_PORT = "COM17"  #IMPORTANT TO CHANGE IT
ARDUINO_BAUDRATE = 9600
SEND_DIAGNOSTICS = True
SEND_DIAGNOSTICS_TIME = 300
ALARM_DELAY = 300
TEMPERATURE_THRESHOLD =  28.0

currentTemp = 0
averageTemp = 0
alarmInvoked = 0

EMAIL_FULL = "my@email.com"
EMAIL_USERNAME = "username"
EMAIL_PASSWORD = "password"

EMAIL_RECIP = "recipient"

def sendEmail(TO,FROM):
    HOST = "host"
    PORT = 25
 
    msg = MIMEMultipart()
    msg["From"] = FROM
    msg["To"] = TO
    msg["Subject"] = "Temperature Alarm"
    msg['Date']    = formatdate(localtime=True)
    bodyMessage = "Hey Administrator, current temperature is at " +str(currentTemp)

    body = MIMEText(bodyMessage, 'plain')
    msg.attach(body)
 
    # attach a file
    #part = MIMEBase('application', "octet-stream")
    #part.set_payload( open(filePath,"rb").read() )
    #Encoders.encode_base64(part)
    #part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filePath))
    #msg.attach(part)
 
    server = smtplib.SMTP(HOST, PORT)
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
 
    try:
        failed = server.sendmail(FROM, TO, msg.as_string())
        server.close()
    except Exception, e:
        errorMsg = "Unable to send email. Error: %s" % str(e)
        print errorMsg

def checkTemperature(stringTemperature):
    global currentTemp
    global averageTemp
    global alarmInvoked
    #analog = analog.encode('string-escape')
    #analog.translate(None, string.digits)
    arr = stringTemperature.split(".")
    if arr[0].isdigit():
        goodnumber =  Decimal(str(arr[0]))
        mTemperature = float(goodnumber)
        currentTemp = mTemperature
        averageTemp = (mTemperature + averageTemp)/2
        if mTemperature > 28.0:
            alarmInvoked += 1
            sendEmail(EMAIL_RECIP, EMAIL_FULL)
            print time.asctime( time.localtime(time.time())),"Please pay attention, we reached ", mTemperature, "degrees!!!!"
            sleep(ALARM_DELAY)

def printDiagnostics():
    localtime = time.asctime( time.localtime(time.time()) )
    print "\n\n-----------DIAGNOSTICS-------------"
    print "Executed on: " , localtime
    print "Current temperature(C): " , currentTemp
    print "Average temperature(C): ", averageTemp
    print "Alarm invoked over ", TEMPERATURE_THRESHOLD , " degrees: " , alarmInvoked
    print "--------END DIAGNOSTICS-------------\n\n"
    threading.Timer(SEND_DIAGNOSTICS_TIME, printDiagnostics).start()
    
if __name__ == "__main__":
    print WELCOME_MESSAGE
    try:
        print "Please wait, Im connecting to Arduino"
        ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUDRATE, timeout=1)
        print "Connection with Arduino estabilished"
    except Exception, e:
            errorMsg = "Ops, I got an error %s" % str(e)
            print "I cannot connect to Arduino."
            sys.exit(0)
    if SEND_DIAGNOSTICS:
        threading.Timer(SEND_DIAGNOSTICS_TIME, printDiagnostics).start()
        
    while 1:
        try:
            analog = ser.readline()
            string = str(analog.strip())
            checkTemperature(string)
        except Exception, e:
            errorMsg = "Cannot read data from Arduino. Error: %s" % str(e)
        
