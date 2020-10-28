import requests
import json

# STEP 1
## Request verisure login page html body with headers
r1 = requests.get('https://mypages.verisure.com/login.html')
raw = r1
lines = raw.text.split("\n")
headers = raw.headers

## obtain CSRF
csrf_1 = [x for x in lines if 'X-CSRF-TOKEN' in x][0].split(':')[-1]
csrf_2 = csrf_1.replace('"','')
csrf_3 = csrf_2.replace(" ","")
csrf = csrf_3.replace("'","")
print(f'CSRF token: {csrf}')

## obtain JSESSION token
jsession_1 = headers['set-cookie']
jsession_2 = jsession_1.split('=')[1]
jsession_3 = jsession_2.split(';')[0]
jsession = jsession_3.replace("'","")
print(f'JSESSION token: {jsession}')

# STEP 2
## spring security check
url = 'https://mypages.verisure.com/j_spring_security_check?locale=no_NO'
h = {
      "Accept: application/json, text/javascript, */*; q=0.01",
      "Accept-Encoding: gzip, deflate, br",
      "Accept-Language: en,en-US;q=0.9,nb-NO;q=0.8,nb;q=0.7,no;q=0.6,nn;q=0.5,da;q=0.4,pt;q=0.3,sv;q=0.2,de;q=0.1",
      "Connection: keep-alive",
      "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
    #   f"Cookie: JSESSIONID={jsession}; country=NO; language=no",
    #   "Origin: https://mypages.verisure.com",
    #   "Referer: https://mypages.verisure.com/login.html",
    #   "Sec-Fetch-Mode: cors",
    #   "Sec-Fetch-Site: same-origin",
    #   "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
    #   F"X-CSRF-TOKEN: {csrf}",
    #   "X-Requested-With: XMLHttpRequest",
    #   "cache-control: no-cache"
}
d = {
    '_csrf': csrf,
    'spring-security-redirect':'/no/start.html',
    'j_username':'***',
    'j_password':'***'
}
r2 = requests.post(url, data=d, headers=h)
import pdb; pdb.set_trace
