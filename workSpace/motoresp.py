import machine
from time import sleep
from machine import Pin

# set machine GPIO2 as p2
p2 = machine.Pin(2)
# configure PWM on pin p2
pwm2 = machine.PWM(p2)
# set the PWM frequency as 50Hz
# the frequency must be between 1Hz and 1kHz.
pwm2.freq(50)

def motorsp(dosage):
  for i in range(dosage):

    sleep(1)
    pwm2.duty(50)
    sleep(1)
    pwm2.duty(98)
    sleep(1)
    pwm2.duty(50)
