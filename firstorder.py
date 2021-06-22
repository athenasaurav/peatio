import hmac
import hashlib 
import binascii
import requests
import time
import http.client
import pprint
import schedule
import config
import random
import json
import smtplib, ssl
from buy import buy
from sell import sell
from binance.client import Client
import ray
def firstorder(BUY_ID, SELL_ID):
    if len(BUY_ID) == 0 & len(SELL_ID) == 0:
        print("No BUY  & Sell Order Found") 
        print("run BUY PY & SELL PY")
        BUY_ID_1= buy.remote(BUY_ID)
        SELL_ID_1= sell.remote(SELL_ID)
        BUY_ID, SELL_ID = ray.get([BUY_ID_1, SELL_ID_1])
    
    return BUY_ID, SELL_ID