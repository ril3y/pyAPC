from enum import Enum
import json
import requests
import sys
from requests.exceptions import ConnectionError


class OutletCommand(Enum):
    NO_ACTION = 1
    ON_IMMEDIATE = 2
    ON_DELAYED = 3
    OFF_IMMEDIATE = 4
    OFF_DELAYED = 5
    REBOOT_IMMEDIATE = 6
    REBOOT_DELAYED = 7
    CANCEL_PENDING_COMMANDS = 8


class PyAPC:

    def __init__(self, _url: str, _username: str, _password: str):
        self.url = _url
        self.username = _username
        self.password = _password
        self.dynamic_url = ""
        self.logoff()

    def get_url(self) -> str:
        return self.url

    def login(self):
        try:
            _login_url = url = f"{self.url}/Forms/login1"
            self._set_header(self.url + '/logon.htm')
            payload = f'login_username={self.username}&login_password={self.password}&submit=Log%2BOn'
            response = requests.request("POST", _login_url, headers=self.headers, data=payload)
            if response.status_code != 200:
                # Try to log off then re-login 1x
                self.logoff()
                response = requests.request("POST", _login_url, headers=self.headers, data=payload)
                if response.status_code != 200:
                    print("Error logging in.  Exiting...")
                    sys.exit()
            self.dynamic_url = response.url.split('/')[4]
            print(f"Login Success, {self.dynamic_url}")
        except ConnectionError as e:
            print(f"Error Connecting to {self.url} - Exiting...")
            sys.exit(-1)

    def apply(self):
        pass

    def _set_header(self, ref):
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': self.url,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.114 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': ref,
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'C0=apc; C0=apc'
        }

    def logoff(self):
        try:
            _logoff_url = f"{self.url}/NMC/{self.dynamic_url}/logout.htm"
            self._set_header(self.url + "/" + self.dynamic_url + "/" + "outlctrl.html")
            payload = {}
            response = requests.request("GET", _logoff_url, headers=self.headers, data=payload)
        except ConnectionError as e:
            print(f"Error Connecting to {self.url} - Exiting...")
            sys.exit(-1)

    def apply_outlet_command(self, outlet_command: OutletCommand, outlets: []):
        try:
            self.logoff()  # Clears any previous logins that might be blocking.
            self.login()
            _ref = f"{self.url}/NMC/{self.dynamic_url}/outlctrl.htm"
            _url = f"{self.url}/NMC/{self.dynamic_url}/Forms/outlctrl1"
            payload = f'rPDUOutletCtrl={outlet_command.value}'
            _outlet_cmd = ""

            for outlet in outlets:
                if outlet <= 8:
                    outlet = outlet + 1
                    _outlet_cmd = _outlet_cmd + f'&OL_Cntrl_Col1_Btn=%3F{outlet}%2C2'
                else:
                    outlet = outlet - 7
                    _outlet_cmd = _outlet_cmd + f'&OL_Cntrl_Col2_Btn=%3F{outlet}%2C2%2C2'
                print(outlet)
            payload = payload + _outlet_cmd + "&submit=Next%2B%3E%3E"
            response = requests.request("POST", _url, headers=self._set_header(_ref), data=payload)
            #print(response.text)
            if response.status_code == 200:
                r = self._run_confirm()
                print(r.text)
                self.logoff()  # clean up so others can login
            else:
                print(f"Error running outlet command {response.status_code}")
                print(response.text)
                self.logoff()  # clean up so others can login
        except ConnectionError as e:
            print(f"Error Connecting to {self.url} - Exiting...")
            sys.exit(-1)

    def _run_confirm(self):
        payload = 'submit=Apply&Control='
        files = {}
        url = f"{self.url}/NMC/{self.dynamic_url}/Forms/rpduconf1"
        self._set_header(f"{self.url}/NMC/{self.dynamic_url}/rpduconf.htm")
        response = requests.request("POST", url, headers=self.headers, data=payload, files=files)
        return response

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                   sort_keys=True, indent=4)

if __name__ == "__main__":
    apc = PyAPC("http://192.168.1.218", "apc", "apc")
    apc.login()

    # apc.apply_outlet_command(OutletCommand.OFF_IMMEDIATE, [14, 6])
