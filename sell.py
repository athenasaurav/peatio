import hmac
import hashlib 
import binascii
import requests
import time
import http.client
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pprint
import schedule
import config
import random
import json
import ray
import smtplib, ssl
@ray.remote
def sell(SELL_ID):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = config.sender_email
    receiver_email = config.receiver_email
    password = config.password
    client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
    depth = client.get_order_book(symbol=config.BINANCE_SYMBOL)
    k = config.NUMBER_OF_ORDER_FETCH_FROM_BINANCE_ORDER_BOOK
    n = len(depth['asks'])
    for i in range(0, n - k ):
        depth['bids'].pop()
        depth['asks'].pop()  
        
    for i in range(0,k):
        # Sell code started
        try:
            api_key = config.PEATIO_API_KEY
            secret = config.PEATIO_API_SECRET
            nonce = int(time.time() * 1000)
            sell_volume = random.uniform(config.MIN_ORDER_SIZE,config.MAX_ORDER_SIZE)
            sell_volume = round(sell_volume, config.VOLUME_PRECISION)
            sell_volume = str(sell_volume)
            sell_price = float(depth['bids'][i][0])
            sell_price = float(sell_price*config.SELL_PRICE_INCREASE_PERCET)
            sell_price = round(sell_price, config.PRICE_PRECISION)
            sell_price = str(sell_price)
            byte_key = bytes(secret, 'UTF-8')
            message = (str(nonce) + api_key).encode()
            signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
            conn = http.client.HTTPConnection("trade.cryptobarter.net")
            sell_payload = "{\r\n    \"market\": \"%s\",\r\n    \"side\" : \"sell\", \r\n    \"volume\" : \"%s\", \r\n    \"ord_type\" : \"limit\",\r\n    \"price\" : \"%s\"\r\n}"% (config.PEATIO_SYMBOL, sell_volume, sell_price)
            headers = {
            'X-Auth-Apikey': api_key,
            'X-Auth-Nonce': nonce,
            'X-Auth-Signature': signature
            }
            conn.request("POST", "/api/v2/peatio/market/orders", sell_payload, headers)
            data = json.loads(conn.getresponse().read().decode("utf-8"))
            # print(data)
            # SELL_ID.append(data['id'])
            time.sleep(0.1)
            key_to_lookup = 'id'
            if key_to_lookup in data:
                print("Key exists")
                SELL_ID.append(data['id'])
            else:
                print("Key does not exist")
                try:
                    api_key = config.PEATIO_API_KEY
                    secret = config.PEATIO_API_SECRET
                    nonce = int(time.time() * 1000)
                    sell_volume = random.uniform(config.MIN_ORDER_SIZE,config.MAX_ORDER_SIZE)
                    sell_volume = round(sell_volume, config.VOLUME_PRECISION)
                    sell_volume = str(sell_volume)
                    sell_price = float(depth['bids'][i][0])
                    sell_price = float(sell_price*config.SELL_PRICE_INCREASE_PERCET)
                    sell_price = round(sell_price, config.PRICE_PRECISION)
                    sell_price = str(sell_price)
                    byte_key = bytes(secret, 'UTF-8')
                    message = (str(nonce) + api_key).encode()
                    signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
                    conn = http.client.HTTPConnection("trade.cryptobarter.net")
                    sell_payload = "{\r\n    \"market\": \"%s\",\r\n    \"side\" : \"sell\", \r\n    \"volume\" : \"%s\", \r\n    \"ord_type\" : \"limit\",\r\n    \"price\" : \"%s\"\r\n}"% (config.PEATIO_SYMBOL, sell_volume, sell_price)
                    headers = {
                    'X-Auth-Apikey': api_key,
                    'X-Auth-Nonce': nonce,
                    'X-Auth-Signature': signature
                    }
                    conn.request("POST", "/api/v2/peatio/market/orders", sell_payload, headers)
                    data = json.loads(conn.getresponse().read().decode("utf-8"))
                    SELL_ID.append(data['id'])
                    time.sleep(0.1)
                except Exception as e:
                    print("an exception occured - {}".format(e))
                    message = """\
                    Subject: Error @ PEATIO SELLING TWICE in Firstorder

                    The Program has encountered following error. The error has occured on BUYING at PEATIO Exchange. \n The error message read as follows: \n{}""".format(e)
                    context = ssl.create_default_context()
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.ehlo()  # Can be omitted
                        server.starttls(context=context)
                        server.ehlo()  # Can be omitted
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)
        except Exception as e:
            print("an exception occured - {}".format(e))
            message = """\
            Subject: Error @ PEATIO SELLING FIRST time in firstorder

            The Program has encountered following error. The error has occured on BUYING at PEATIO Exchange. \n The error message read as follows: \n{}""".format(e)
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)

    return SELL_ID
