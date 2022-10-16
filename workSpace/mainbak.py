
import urequests
import testntp


api1prefix = "http://3.26.197.0/hardware/?format=json"
username = "test123456"
password = "123456"

response = urequests.get("http://3.26.197.0/hardware/?format=json&password=123456&username=test123456")
print("phase1")
print(type(response))

parsed = response.json()
print("phase2")
print(type(parsed))

print(parsed)
data = parsed[username][0]['dosage']
print("phase3 "+"dosage is: "+data)

time = parsed[username][0]['num_time']



