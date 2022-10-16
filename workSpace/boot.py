import gc

import os

import network

import time
from machine import Pin
led=Pin(2,Pin.OUT)          #create LED object from pin2,Set Pin2 to output
#import webrepl

#webrepl.start()

gc.collect()

ssid = "ROGM16"
password = "wu92387268"

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()                             # Scan for available access points
print("Connecting to: " + ssid)
sta_if.connect(ssid, password)    # Connect to an AP
while sta_if.isconnected()!=0:
  led.value(1)              #turn off
  time.sleep(0.2)
  led.value(0)              #turn on
  time.sleep(0.2)
if sta_if.isconnected()==0:
  print("Connected to: " + ssid)# Check for successful connection
  for x in range(5):
    led.value(0)              #turn on
    time.sleep(0.5)
    led.value(1)              #turn off
    time.sleep(0.5)
  #LED blink 5 times indicate that WIFI connected successfully

import ntptime
def sync_ntp():
     ntptime.NTP_DELTA = 3155644800   # UTC+8
     ntptime.host = 'pool.ntp.org'  # ntp server default"pool.ntp.org"
     ntptime.settime()   

sync_ntp()


