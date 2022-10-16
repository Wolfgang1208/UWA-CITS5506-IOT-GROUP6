#hardware platform: FireBeetle-ESP8266

import time
from machine import Pin
led=Pin(14,Pin.OUT)          #create LED object from pin2,Set Pin2 to output

#1 == off 0 == on
def setLed(status):
  led.value(status)              #turn off
  


