import time
import machine
from machine import RTC, Pin, ADC
import math
import urequests
from time import sleep
import gc

timeRange = 1 # 1==debug 30==regular num stands for minutes

emailPrefix = "http://3.26.197.0/send_email/?medicine_status="
api1prefix = "http://3.26.197.0/hardware/?format=json"
username = "test123456"
password = "123456"
url = api1prefix+"&password="+password+"&username="+username
print(url)

led=Pin(14,Pin.OUT)          #create LED object from pin2,Set Pin2 to output

# set machine GPIO2 as p2
p2 = machine.Pin(2)
# configure PWM on pin p2
pwm2 = machine.PWM(p2)
# set the PWM frequency as 50Hz
# the frequency must be between 1Hz and 1kHz.
pwm2.freq(50)

pot = ADC(0)

def motorsp(dosage):
  for i in range(dosage):
    sleep(1)
    pwm2.duty(50)
    sleep(1)
    pwm2.duty(98)
    sleep(1)
    pwm2.duty(50)

#1 == off 0 == on
def setLed(status):
  led.value(status)              #turn off

def getSch(url):
  response = urequests.get(url)
  parsed = response.json()
  time = parsed[username][0]['num_time'].replace(" ","")
  timeseq = time.split(",")
  dosage = parsed[username][0]['dosage']
  bEmail = parsed[username][0]['email']
  sEmail = parsed['self_email']
  return timeseq,dosage,bEmail,sEmail
  
def readLdr():
  sleep(1)
  pot_value = 0
  pot_value_tt = 0
  for i in range(10):
    pot_value = pot.read()
    print(pot_value)
    pot_value_tt = pot_value_tt + pot_value
    sleep(0.5)
  
  pot_value_tt = pot_value_tt/10
  print(pot_value_tt)
  
  if pot_value_tt<50:
    return 1
  else:
    return 0

#1==pill there check elders 0==pill there plz take
def send(medicine_status,emailUrl):
  if medicine_status == 1:
    urequests.get(emailUrl)
  if medicine_status == 0:
    urequests.get(emailUrl)
  print("email sent code: "+str(medicine_status))

def init(url):
  timeseq,dosage,bEmail,sEmail = getSch(url)
  
  print("Dosage is: "+str(dosage))
  
  print(timeseq)
  
  for times in timeseq:
    print("Timing is: "+str(times))
  
  mins = []
  
  for times in timeseq:
    tmp = times.split(":")
    min = int(tmp[0])*60+int(tmp[1])
    mins.append(min)
  
  print(mins)
  return timeseq,int(dosage),str(bEmail),str(sEmail),mins
  
#drop pills and sense&email to notice, led:on->off
def s1(dosage,emailUrl):
  motorsp(int(dosage))
  print("motor done")
  setLed(1)
  print("led on")
  readLdr()
  print("ldr done")
  send(0,emailUrl)
  print("email done")
  setLed(0)
  print("led off")
  
#detect pills and send email to notice, led:on
def s2(emailUrl0):
  setLed(1)
  print("led on")
  ldr = readLdr()
  if ldr==1:
    print("ldr done")
    send(0,emailUrl0)
    print("email done")
  
#detect pills and send emergency email to notice, led:on
def s3(emailUrl1):
  setLed(1)
  print("led on")
  ldr = readLdr()
  if ldr==1:
    print("ldr done")
    send(1,emailUrl1)
    print("email done")


def medicationReminder():
  rtc = RTC()
  while True:
    #gc.collect()
    #scenario testing localtime
    localTime = rtc.datetime()
    print(str(localTime[4])+":"+str(localTime[5]))
    localMins = localTime[4]*60+localTime[5]
    print(localMins)
    
    timeseq,dosage,bEmail,sEmail,mins = init(url)
    for min in mins:
      print(min)
      print(min - localMins)
      if min - localMins == timeRange:
        print("USER email is:"+sEmail)
        print("Emergency contact email is: "+bEmail)
        #1==pill there check elders 0==pill there plz take
        emailUrl1 = emailPrefix+"1&b_email="+bEmail+"&s_email="+sEmail
        emailUrl0 = emailPrefix+"0&b_email="+bEmail+"&s_email="+sEmail
        #phase 1: 
        #  1, dispensing 
        #  2, sending email to notice USER to take pills 
        s1(dosage,emailUrl0)
        #wait for 60*timerange seconds to next phase
        sleep(60*timeRange)
        #phase 2: 
        #  1, sensing whether pills have been took
        #  2, sending email to notice USER to take pills 
        s2(emailUrl0)
        #wait for 60*timerange seconds to next phase
        sleep(60*timeRange)
        #phase 3: 
        #  1, sensing whether pills have been took
        #  2, sending email to emergency contact to check USER status
        s3(emailUrl1)
        setLed(0)
    sleep(60)

medicationReminder()
