import requests
import json

SES = requests.Session()

def headers():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'X-Client-Data': 'CP6JywE=',
        'Referer': 'https://www.netflix.com/'
    }

    return header

def main(anchor):
    req = SES.get(url=anchor,headers=headers()).text
    token = req.split('<input type="hidden" id="recaptcha-token" value="')[1].split('">')[0]
    data_anchor = anchor.split('&')
    data = f"v={data_anchor[4]}&reason=q&c={token}&k={data_anchor[4]}&co={data_anchor[2]}&hl=en&size=invisible"
    
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '/',
        'Origin': 'https://www.google.com',
        'X-Client-Data': 'CP6JywE=',
        'Referer': anchor
    }

    res = SES.post(url=f'https://www.google.com/recaptcha/enterprise/reload?{data_anchor[1]}',headers=header,data=data).text
    res = res.replace(")]}'","").strip()
    captcha = json.loads(res)[1]
    return captcha