
from machine import Pin, ADC
from time import sleep

pot = ADC(0)


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

