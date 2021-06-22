import smtplib, ssl
import config
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = config.sender_email
receiver_email = config.receiver_email
password = config.password
from binance.client import Client
import ray

@ray.remote
def check_balance_1(BUY_ID):


    client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET, {"verify": False, "timeout": 20})
    balance_btc = client.get_asset_balance(asset=config.BINANCE_ASSET_TO_CHECK_1)
    print(balance_btc)

    message_1 = """\
    Subject: Balance Low

    We have detected low {} balance in your Binance account.\n{}""".format(balance_btc['asset'], balance_btc)

    if float(balance_btc['free']) < config.MAX_ORDER_SIZE:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message_1)
    else:
        print("{} Balance is optimum".format(config.BINANCE_ASSET_TO_CHECK_1))

    return BUY_ID

@ray.remote
def check_balance_2(SELL_ID):


    client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET, {"verify": False, "timeout": 20})
    balance_usdt = client.get_asset_balance(asset=config.BINANCE_ASSET_TO_CHECK_2)
    print(balance_usdt)

    message_2 = """\
    Subject: Balance Low

    We have detected low {} balance in your Binance account.\n{}""".format(balance_usdt['asset'], balance_usdt)

    if float(balance_usdt['free']) < config.MAX_ORDER_SIZE:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message_2)
    else:
        print("{} Balance is optimum".format(config.BINANCE_ASSET_TO_CHECK_2))

    return SELL_ID