#   Binance Credentials
BINANCE_API_KEY = 'YLBZsnOUI35ztCU3xI6IopH369nAa3111XqkZ5eOPe0BxX1xGxkJDVlKvCQ0mwuP'
BINANCE_API_SECRET = 'MBGeHQlb6ZTMnqwDRc6CxtSa9TKYa8nyh9ZWyJDWS6F1466i2DyFpINwMxtSIZdW'
BINANCE_SYMBOL = 'BTCUSDT'

PEATIO_API_KEY = '3df0aa7f11e5f384'
PEATIO_API_SECRET = 'b0fe5cb1bc8bccfd56259861ef310d49' 
PEATIO_SYMBOL = 'btcusds'


#   Refresh time, to create 10 Buy & Sell Orders, check any done orders, 
#   if yes create a back order on Binance and cancel the rest BUY & Sell orders. Time in Seconds
REFRESH_TIME = 5

#   Refresh time, to create 1 Buy Order & immedietly create one Sell Order or same Volume and Price to nullify. 
#   This creates charts for us. Time in Seconds
REFRESH_TIME_JOB1 = 5

#   Number of Bids and Asks data to be fetched from Binance. 
#   If the number is 15, 15 Best Bids and 15 Sell Bids will be fetched from Biannce
NUMBER_OF_ORDER_FETCH_FROM_BINANCE_ORDER_BOOK = 15


# We will select random values between MIN_ORDER_SIZE & MAX_ORDER_SIZE
MIN_ORDER_SIZE = 0.00005    # MIN_ORDER_SIZE to create on Binance
MAX_ORDER_SIZE = 0.005      # MAX_ORDER_SIZE to create on Binance


PRICE_PRECISION = 2         # Rounding the Price upto 2 decimal Places
VOLUME_PRECISION = 5        # Rounding the Volume upto 5 decimal Places

#99.5% price of the Biannce BUY Price, For Ex : Price on Binance for BUY is 100, on peotio it will be 99.5
BUY_PRICE_DECREASE_PERCET = 0.995
#100.5% price of the Biannce SELL Price, For Ex : Price on Binance for SELL is 100, on peotio it will be 100.5
SELL_PRICE_INCREASE_PERCET = 1.005

##Email setting for low Bianance Balance
sender_email = "tradingbotlogs@gmail.com"
receiver_email = "Kismatwala1@gmail.com", "ku.saurav@gmail.com"
password = "Aut07r@d3"

# Currency Pair to Moniter on Binance
BINANCE_ASSET_TO_CHECK_1 = 'BTC'
BINANCE_ASSET_TO_CHECK_2 = 'USDT'

# Refresh time to check Balance on Binance and report Low Balance via Email. Time in Seconds
REFRESH_TIME_BALANCE = 3600

# Refresh time to check PEATIO active buy + sell orders and if found more than twice of NUMBER_OF_ORDER_FETCH_FROM_BINANCE_ORDER_BOOK, cancel all. Time in Seconds
REFRESH_TIME_CLEAR = 5
