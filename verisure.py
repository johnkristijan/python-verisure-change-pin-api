import requests
import json


class Verisure:
    """
    """
    LOGIN_URL = 'https://mypages.verisure.com/login.html'
    SPRINT_SECURITY_CHECK_URL = "https://mypages.verisure.com/j_spring_security_check?locale=no_NO"

    def __init__(self, username, password):
        self.credentials = {'j_username': username, 'j_password': password}
        self._lines = None
        self._headers = None
        self._csrf_token = None

        self._login()

    def authenticate(self):
        req = requests.get(self.LOGIN_URL)
        self._lines = req.text.splitlines()
        self._headers = req.headers

        self._csrf_token = self._get_csrf_token()
        self._initiate_spring_security_check()

    def _get_csrf_token(self) -> str:
        if not self._lines:
            raise ValueError("Can't extract CSRF TOKEN - missing body data from login endpoint.")
        try:
            csrf = [x for x in lines if 'X-CSRF-TOKEN' in x][0]
            csrf = csrf.split(':')[-1]
            csrf = csrf.strip().replace("'", "")
        except IndexError as ie:
            print(f"Unable to extract X-CSRF-Token.. Not found in returned body from Verisure. Contact developer!")
            raise ie

        return csrf

    def _get_jsession_token(self) -> str:
        if not 'set-cookie' in self._headers:
            raise ValueError("Can't extract 'jsession' token. 'set-cookie' not part of returned headers from login endpoint.")
        jsess = self._headers['set-cookie']
        try:
            jsess = jsess.split("=")[1].split(";")[0]
        except IndexError as ie:
            print(f"Unable to extract JSESSIONID. Not returned in headers from Verisure. Contact developer!")
            raise ie

        return jsess

    def _initiate_spring_security_check(self):
        hdrs = {
            "Accept: application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding: gzip, deflate, br",
            "Accept-Language: en,en-US;q=0.9,nb-NO;q=0.8,nb;q=0.7,no;q=0.6,nn;q=0.5,da;q=0.4,pt;q=0.3,sv;q=0.2,de;q=0.1",
            "Connection: keep-alive",
            "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
        }
        data = {
            '_csrf': csrf,
            'spring-security-redirect':'/no/start.html',
            **self.credentials
        }
        req = requests.post(self.SPRINT_SECURITY_CHECK_URL, headers=hdrs, data=data)
        if req.ok:
            print("Successfully completed the Spring Security Check")
        else:
            print(f"Fack - bad return code: code={req.status_code}, reason={req.reason}")


if __name__ == "main":
    print("Welcome to the superduper awesome Verisure change PIN API.. CLI.")
    username = "kong.harald@kongehuset.no"
    password = "moonshine"

    v = Verisure(username, password)
