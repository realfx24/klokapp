import requests

def main(anchor):
    r = requests.post("http://47.236.227.93:5000/run-v3", json={"anchor": anchor})
    captcha = r.json()['result']

    return captcha
