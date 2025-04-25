from web3.auto import w3
from eth_account import Account
from eth_account.messages import encode_defunct
from colorama import init, Fore, Style
import uuid
from datetime import timezone
from datetime import datetime
import secrets
import requests
import random
from fake_useragent import UserAgent
import time
import json
import os
import v3

init()

def get_current_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def read_wallet(private_key):
    acct = Account.from_key(private_key)
    return {"address": acct.address, "private_key": private_key}

def get_current_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def sign_message(private_key, address, nonce):
    try:
        current_time = get_current_time()
        message = f"""klokapp.ai wants you to sign in with your Ethereum account:
{address}


URI: https://klokapp.ai/
Version: 1
Chain ID: 1
Nonce: {nonce}
Issued At: {current_time}"""

        message_hash = encode_defunct(text=message)
        signed_message = w3.eth.account.sign_message(message_hash, private_key=private_key)
        return signed_message.signature.hex(), message
    except Exception as e:
        print(f"{Fore.RED}Error signing message: {str(e)}{Style.RESET_ALL}")
        return None, None
    
def get_headers():
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://klokapp.ai',
        'referer': 'https://klokapp.ai/',
        'authority': 'api1-pp.klokapp.ai',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="133", "Not(A:Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }

def get_chat_headers(session_token):
    return {
        'Host': 'api1-pp.klokapp.ai',
        'X-Session-Token': session_token,
        'Sec-Ch-Ua-Platform': random.choice(['"Windows"', '"macOS"', '"Linux"']),
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Ch-Ua': '"Chromium";v="133", "Not(A:Brand";v="99"',
        'User-Agent': UserAgent().random,
        'Sec-Ch-Ua-Mobile': '?0',
        'Accept': '*/*',
        'Origin': 'https://klokapp.ai',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://klokapp.ai/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=1, i'
    }

def login(signature, message, ref_code=None):
    try:
        captcha = v3.main('https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LcZrRMrAAAAAKllb4TLb1CWH2LR7iNOKmT7rt3L&co=aHR0cHM6Ly9rbG9rYXBwLmFpOjQ0Mw..&hl=en&v=ItfkQiGBlJDHuTkOhlT3zHpB&size=invisible&cb=679dkivi4qe6')
        session = requests.Session()
        response = session.post(
            'https://api1-pp.klokapp.ai/v1/verify',
            headers=get_headers(),
            json={
                'signedMessage': signature,
                'message': message,
                'referral_code': ref_code,
                'recaptcha_token': captcha
            }
        )
        if response.status_code == 200:
            data = response.json()
            if data['message'] == 'Verification successful':
                return data['session_token']
            else:
                print(f"{Fore.RED}Verification failed: {data['message']}{Style.RESET_ALL}")
                return None
        print(f"{Fore.RED}Failed to login: {response.status_code}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}Error during login: {str(e)}{Style.RESET_ALL}")
        return None

def get_random_question():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'chat.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        questions = [line.strip() for line in f if line.strip()]  # buang baris kosong
    return random.choice(questions)

def send_chat(session,address,sisa):
    text = get_random_question()
    url = 'https://api1-pp.klokapp.ai/v1/chat'
    payload = {"id":str(uuid.uuid4()),"title":"","messages":[{"role":"user","content":text}],"sources":[],"model":random.choice(["llama-3.3-70b-instruct","deepseek-r1","gpt-4o-mini"]),"created_at":get_current_time(),"language":"english"}
    req = requests.post(url, headers=get_chat_headers(session), json=payload)
    if req.status_code == 200:
        print(f"{Fore.LIGHTYELLOW_EX}Chat sent successfully: {text}{Style.RESET_ALL}")
        print(f"response: {req.text}")
        get_point(session,address,sisa)
    else:
        print(f"{Fore.RED}Failed to send chat: {req.status_code} - {req.text}{Style.RESET_ALL}")

def get_point(session,address,sisa):
    url = 'https://api1-pp.klokapp.ai/v1/points'
    req = requests.get(url, headers=get_chat_headers(session))
    if req.status_code == 200:
        data = req.json()
        print(f"{Fore.LIGHTGREEN_EX}address : {address}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTGREEN_EX}points  : {data['total_points']}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTGREEN_EX}limit   : {sisa} chat{Style.RESET_ALL}")
        print('+==============================================+')

def get_limit(session):
    url = 'https://api1-pp.klokapp.ai/v1/rate-limit'
    req = requests.get(url, headers=get_chat_headers(session))
    if req.status_code == 200:
        data = req.json()
        return data['remaining']

def countdown(total_seconds):
    while total_seconds >= 0:
        days = total_seconds // (24 * 3600)
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        print(f"countdown {days:02}:{hours:02}:{minutes:02}:{seconds:02} seconds", end='\r')

        time.sleep(1)
        total_seconds -= 1

def run_daily():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'private_key.txt')
    while True:
        with open(file_path, 'r') as file:
            for line in file:
                private_key = line.strip()
                address = read_wallet(private_key)["address"]
                address = address.strip()
                nonce = secrets.token_hex(48)
                signature, message = sign_message(private_key, address, nonce)
                session = login(signature, message)
                if session:
                    print(f"address: {address} {Fore.LIGHTGREEN_EX}Verification successful{Style.RESET_ALL}")
                    sisa = get_limit(session)
                    while sisa > 0:
                        send_chat(session, address, sisa)
                        sisa -= 1

        countdown(86400)

