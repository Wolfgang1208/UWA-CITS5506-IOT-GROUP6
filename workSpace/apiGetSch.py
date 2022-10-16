

import urequests

api1prefix = "http://3.26.197.0/hardware/?format=json"
username = "test123456"
password = "123456"

def getSch():
  response = urequests.get("http://3.26.197.0/hardware/?format=json&password=123456&username=test123456")
  parsed = response.json()
  time = parsed[username][0]['num_time'].replace(" ","")
  timeseq = time.split(",")
  dosage = parsed[username][0]['dosage']
  return timeseq,dosage
  

