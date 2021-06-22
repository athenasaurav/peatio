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
import ray
import smtplib, ssl
@ray.remote
def clear_buy(BUY_ID):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = config.sender_email
    receiver_email = config.receiver_email
    password = config.password
    try:
        print("Cancel remaining BUY Order")
        api_key = config.PEATIO_API_KEY
        secret = config.PEATIO_API_SECRET
        nonce = int(time.time() * 1000)
        byte_key = bytes(secret, 'UTF-8')
        message = (str(nonce) + api_key).encode()
        signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        conn = http.client.HTTPConnection("trade.cryptobarter.net")
        cancel_payload = "{\r\n \"side\" : \"buy\"\r\n}"
        headers = {
        'X-Auth-Apikey': api_key,
        'X-Auth-Nonce': nonce,
        'X-Auth-Signature': signature
        }
        conn.request("POST", "/api/v2/peatio/market/orders/cancel", cancel_payload, headers)
        data = json.loads(conn.getresponse().read().decode("utf-8"))
        # print(data)
        BUY_ID.clear()
    except Exception as e:
        print("an exception occured - {}".format(e))
        message = """\
        Subject: Error

        The Program has encountered following error.\n{}""".format(e)
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    return BUY_ID

@ray.remote
def clear_sell(SELL_ID):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = config.sender_email
    receiver_email = config.receiver_email
    password = config.password
    try:
        print("Cancel remaining SELL Order")
        api_key = config.PEATIO_API_KEY
        secret = config.PEATIO_API_SECRET
        nonce = int(time.time() * 1000)
        byte_key = bytes(secret, 'UTF-8')
        message = (str(nonce) + api_key).encode()
        signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        conn = http.client.HTTPConnection("trade.cryptobarter.net")
        cancel_payload = "{\r\n \"side\" : \"sell\"\r\n}"
        headers = {
        'X-Auth-Apikey': api_key,
        'X-Auth-Nonce': nonce,
        'X-Auth-Signature': signature
        }
        conn.request("POST", "/api/v2/peatio/market/orders/cancel", cancel_payload, headers)
        data = json.loads(conn.getresponse().read().decode("utf-8"))
        # print(data)
        SELL_ID.clear()

    except Exception as e:
        print("an exception occured - {}".format(e))
        message = """\
        Subject: Error

        The Program has encountered following error.\n{}""".format(e)
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)


    return SELL_ID