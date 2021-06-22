import hmac
import hashlib 
import binascii
import http.client
import requests
import time
import http.client
from binance.client import Client
import pprint
import schedule
import config
import random
import json
import ray
import smtplib, ssl
from buy import buy
from sell import sell
from firstorder import firstorder
from clear import clear_buy
from clear import clear_sell
from binance_buy import binance_buy
from binance_sell import binance_sell
from buy_sell import buy_sell
from check_binance_balance import check_balance_1, check_balance_2
from cancel_buy import cancel_buy
from cancel_sell import cancel_sell
ray.init()
BUY_ID = []
SELL_ID = []
ASKS = [] 
BIDS = []
BUY_ID_1= clear_buy.remote(BUY_ID)
SELL_ID_1= clear_sell.remote(SELL_ID)
SELL_ID, BUY_ID = ray.get([SELL_ID_1, BUY_ID_1])
BUY_ID, SELL_ID = firstorder(BUY_ID, SELL_ID)

def job():
    global BUY_ID, SELL_ID
    print(BUY_ID, SELL_ID)
    print("BINANCE BUY and SELL Order")
    try:
        BUY_ID_1= binance_buy.remote(BUY_ID)
        SELL_ID_1= binance_sell.remote(SELL_ID)
        SELL_ID, BUY_ID = ray.get([SELL_ID_1, BUY_ID_1])
    except Exception as e:
        print("Binance Buy and Sell Program didnt run properly")
    print("PEATIO CANCEL_BUY and CANCEL_SELL Order")
    try:
        BUY_ID_1= cancel_buy.remote(BUY_ID)
        SELL_ID_1 = cancel_sell.remote(SELL_ID)
        BUY_ID, SELL_ID = ray.get([BUY_ID_1, SELL_ID_1])
    except Exception as e:
        print("Cancel Buy and Sell Program didnt run properly")

def job1():
    print("PEATIO BUY and SELL for CHART")
    buy_sell()

def balance():
    global BUY_ID, SELL_ID
    BUY_ID_1= check_balance_1.remote(BUY_ID)
    SELL_ID_1= check_balance_2.remote(SELL_ID)
    BUY_ID, SELL_ID = ray.get([BUY_ID_1, SELL_ID_1])

def clear():
    global ASKS, BIDS, BUY_ID, SELL_ID
    api_key = '3df0aa7f11e5f384'
    secret = 'b0fe5cb1bc8bccfd56259861ef310d49' 
    nonce = int(time.time() * 1000)
    byte_key = bytes(secret, 'UTF-8')
    message = (str(nonce) + api_key).encode()
    signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    clear_payload = {}
    headers = {
    'X-Auth-Apikey': api_key,
    'X-Auth-Nonce': nonce,
    'X-Auth-Signature': signature
    }
    conn = http.client.HTTPConnection("trade.cryptobarter.net")
    conn.request("GET", "/api/v2/peatio/market/orders?state=wait",clear_payload, headers)
    total_bids_asks = json.loads(conn.getresponse().read().decode("utf-8"))
    if len(total_bids_asks) > (config.NUMBER_OF_ORDER_FETCH_FROM_BINANCE_ORDER_BOOK*2):
        try:
            BUY_ID_1= clear_buy.remote(BUY_ID)
            SELL_ID_1= clear_sell.remote(SELL_ID)
            SELL_ID, BUY_ID = ray.get([SELL_ID_1, BUY_ID_1])
            BUY_ID, SELL_ID = firstorder(BUY_ID, SELL_ID)
        except Exception as e:
            print("Clear Buy and Sell or First Order Program didnt run properly inside schedule function.")
    else:
        print(" No need to run cancel.py")


schedule.every(config.REFRESH_TIME).seconds.do(job)
schedule.every(config.REFRESH_TIME_JOB1).seconds.do(job1)
schedule.every(config.REFRESH_TIME_BALANCE).seconds.do(balance)
schedule.every(config.REFRESH_TIME_CLEAR).seconds.do(clear)

while True:
    schedule.run_pending()
    time.sleep(1)
