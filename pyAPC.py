import requests

url = "http://192.168.1.218/Forms/login1"

payload='login_username=apc&login_password=apc&submit=Log%2BOn'
headers = {
  'Connection': 'keep-alive',
  'Cache-Control': 'max-age=0',
  'Upgrade-Insecure-Requests': '1',
  'Origin': 'http://192.168.1.218',
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Referer': 'http://192.168.1.218/logon.htm',
  'Accept-Language': 'en-US,en;q=0.9',
  'Cookie': 'C0=apc; C0=apc'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)



