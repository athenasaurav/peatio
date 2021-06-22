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
def binance_buy(BUY_ID):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = config.sender_email
    receiver_email = config.receiver_email
    password = config.password
    if len(BUY_ID) == 0: 
        print("No Buyer Data Found - Binance")
    if len(BUY_ID) != 0:
        for i in range(len(BUY_ID)): 
            # print("Buyer Data Found - checking Done Buy order - Binance")
            client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
            api_key = config.PEATIO_API_KEY
            secret = config.PEATIO_API_SECRET
            nonce = int(time.time() * 1000)
            buy_volume = "0.13"
            buy_price = "37.37"
            symbol = 'btcusds'
            byte_key = bytes(secret, 'UTF-8')
            message = (str(nonce) + api_key).encode()
            signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
            conn = http.client.HTTPConnection("trade.cryptobarter.net")
            buy_payload = "{\r\n    \"market\": \"%s\",\r\n    \"side\" : \"sell\", \r\n    \"volume\" : \"%s\", \r\n    \"ord_type\" : \"limit\",\r\n    \"price\" : \"%s\"\r\n}"% (symbol, buy_volume, buy_price)
            headers = {
            'X-Auth-Apikey': api_key,
            'X-Auth-Nonce': nonce,
            'X-Auth-Signature': signature
            }
            conn.request("GET", "/api/v2/peatio/market/orders/{}".format(BUY_ID[i]), buy_payload, headers)
            data = json.loads(conn.getresponse().read().decode("utf-8"))
            # print(data)
            try:
                if data['trades_count'] == 1:
                    try:
                        print("BINANCE Exchange BUY_ID executed is :{}",format(data['id']))
                        symbol = config.BINANCE_SYMBOL
                        quantity = data['executed_volume']
                        print(quantity)
                        binance_order = client.order_market_sell(symbol=symbol, quantity=quantity)
                        print("binance SELL order is")
                        print(binance_order)
                    except Exception as e:
                        print("an exception occured - {}".format(e))
                        message = """\
                        Subject: Error @ BINANCE BUYING

                        The Program has encountered following error.The error has occured on BUYING at BINANCE Exchange. \n The error message read as follows\n{}""".format(e)
                        context = ssl.create_default_context()
                        with smtplib.SMTP(smtp_server, port) as server:
                            server.ehlo()  # Can be omitted
                            server.starttls(context=context)
                            server.ehlo()  # Can be omitted
                            server.login(sender_email, password)
                            server.sendmail(sender_email, receiver_email, message)
                else:
                    pass
            except Exception as e:
                        print("an exception occured at BINANCE BUY order")
        

    return BUY_ID