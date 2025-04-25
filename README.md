# KlokApp / MIRA Auto Bot
<p align="center">
    <img width="400" alt="image" src="img1.png">
</p>
*KlokApp Auto Bot is an automation script to earning point from send chat to AI platform, such as Daily and referrer*

- Register : [HERE](https://klokapp.ai?referral_code=L7USVPYL)

## Features
1. **Auto Chat (Daily)**: Send chat to AI repeat 24 Hours.
2. **Add Refferer**: Perform automatic mining to earn points.
3. **Saving Referrer Accounts**: Auto save referrer account into assets/klok_{your_referrer_code}.txt
4. **Free Bypass Features**: Bypassing ReCaptcha V3 Free

## Requirements
- Python 3.8 or latest

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/realfx24/klokapp.git
   cd klokapp
   ```

2. Activate Virtual Environment (Optional for VPS):
   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. Install dependencies (if error using Virtual Environment):
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
1. enter your private key into config/private_key.txt like this
   ```bash
   0x...1
   0x...2
   0x...3
   ```

2. Fill your referral code in config/ref_code.txt like this
   ```bash
   referral_code1
   referral_code2
   referral_code3
   ```

## How to use
Run the main script:
   ```bash
   python bot.py
   ```
   if in VPS or Linux:
   ```bash
   python3 bot.py
   ```
## Output Example
<p align="center">
    <img width="600" alt="image" src="img2.png">
</p>

## Dependencies
- **Asyncio** - A Python library used to write asynchronous code. It allows the program to handle multiple tasks concurrently, such as making API requests or performing background tasks without blocking the main thread.
- **AioHTTP** - An asynchronous HTTP client/server library for Python. It is used to make non-blocking HTTP requests, which is essential for interacting with APIs in an efficient way.
- **Loguru** - A modern logging library for Python. It simplifies logging by providing an easy-to-use interface and advanced features like structured logging, log rotation, and better formatting for debugging.
