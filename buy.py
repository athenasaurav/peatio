import hmac
import hashlib 
import binascii
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
@ray.remote
def buy(BUY_ID):
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
            buy_volume = random.uniform(config.MIN_ORDER_SIZE,config.MAX_ORDER_SIZE)
            buy_volume = round(buy_volume, config.VOLUME_PRECISION)
            buy_volume = str(buy_volume)
            buy_price = float(depth['asks'][i][0])
            buy_price = float(buy_price*config.BUY_PRICE_DECREASE_PERCET)
            buy_price = round(buy_price, config.PRICE_PRECISION)
            buy_price = str(buy_price)
            symbol = config.PEATIO_SYMBOL
            byte_key = bytes(secret, 'UTF-8')
            message = (str(nonce) + api_key).encode()
            signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
            conn = http.client.HTTPConnection("trade.cryptobarter.net")
            buy_payload = "{\r\n    \"market\": \"%s\",\r\n    \"side\" : \"buy\", \r\n    \"volume\" : \"%s\", \r\n    \"ord_type\" : \"limit\",\r\n    \"price\" : \"%s\"\r\n}"% (config.PEATIO_SYMBOL, buy_volume, buy_price)
            headers = {
            'X-Auth-Apikey': api_key,
            'X-Auth-Nonce': nonce,
            'X-Auth-Signature': signature
            }
            conn.request("POST", "/api/v2/peatio/market/orders", buy_payload, headers)
            data = json.loads(conn.getresponse().read().decode("utf-8"))
            # print(data)
            # BUY_ID.append(data['id'])
            time.sleep(0.1)
            key_to_lookup = 'id'
            if key_to_lookup in data:
                print("Key exists")
                BUY_ID.append(data['id'])
            else:
                print("Key does not exist")
                try:
                    api_key = config.PEATIO_API_KEY
                    secret = config.PEATIO_API_SECRET
                    nonce = int(time.time() * 1000)
                    buy_volume = random.uniform(config.MIN_ORDER_SIZE,config.MAX_ORDER_SIZE)
                    buy_volume = round(buy_volume, config.VOLUME_PRECISION)
                    buy_volume = str(buy_volume)
                    buy_price = float(depth['asks'][i][0])
                    buy_price = float(buy_price*config.BUY_PRICE_DECREASE_PERCET)
                    buy_price = round(buy_price, config.PRICE_PRECISION)
                    buy_price = str(buy_price)
                    symbol = config.PEATIO_SYMBOL
                    byte_key = bytes(secret, 'UTF-8')
                    message = (str(nonce) + api_key).encode()
                    signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
                    conn = http.client.HTTPConnection("trade.cryptobarter.net")
                    buy_payload = "{\r\n    \"market\": \"%s\",\r\n    \"side\" : \"buy\", \r\n    \"volume\" : \"%s\", \r\n    \"ord_type\" : \"limit\",\r\n    \"price\" : \"%s\"\r\n}"% (config.PEATIO_SYMBOL, buy_volume, buy_price)
                    headers = {
                    'X-Auth-Apikey': api_key,
                    'X-Auth-Nonce': nonce,
                    'X-Auth-Signature': signature
                    }
                    conn.request("POST", "/api/v2/peatio/market/orders", buy_payload, headers)
                    data = json.loads(conn.getresponse().read().decode("utf-8"))
                    BUY_ID.append(data['id'])
                    time.sleep(0.1)
                except Exception as e:
                    print("an exception occured - {}".format(e))
                    message = """\
                    Subject: Error @ PEATIO BUYING TWICE in firstorder

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
            Subject: Error @ PEATIO BUYING FIRST time in firstorder

            The Program has encountered following error. The error has occured on BUYING at PEATIO Exchange. \n The error message read as follows: \n{}""".format(e)
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)

    return BUY_ID

