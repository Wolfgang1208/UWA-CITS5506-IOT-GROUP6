

import urequests

#1==pill there check elders 0==pill there plz take
def send(medicine_status):
  if medicine_status == 1:
    urequests.get('http://3.26.197.0/send_email/?medicine_status=1&b_email=Wolfgang1208@outlook.com&s_email=907323782@qq.com')
  if medicine_status == 0:
    urequests.get('http://3.26.197.0/send_email/?medicine_status=0&b_email=Wolfgang1208@outlook.com&s_email=907323782@qq.com')
  print("email sent code: "+str(medicine_status))

