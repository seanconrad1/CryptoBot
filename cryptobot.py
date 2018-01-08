from bittrex.bittrex import *
from decimal import *
import json
import threading
import datetime


# Find coin, buy in to it, run bot, bot will access account, start checking prices, when it is first ran
# ask what coin and at what price did you buy in
# check every 15 min, if up 10% or lower, buy or sell
# Starts off as True because we already bought in.
# Bag_hold = True, if true don't buy at 10% loss, if false, buy
# if price = 20% and if Bag_hold = true , sell


# xlm use 0.00004359

class CryptoBot:
    '''
    Class for cryptobot
    '''

    ticker = input('Type ticker: ')
    ticker = ticker.upper()
    price_bought = Decimal((input('Enter price bought in BTC: ')))
    past_price = 0
    entry_price = price_bought
    my_bittrex = Bittrex("<KEY>", "<SECRET>", api_version=API_V2_0)
    bag_hold = True

    def __init__(self):
        pass

    def my_balance(self, ticker):
        '''
        Get balance of current coin
        '''
        try:
            return float(self.my_bittrex.get_balance(ticker)['result']['Balance'])
        except 'NoneType':
            print('No ' + self.ticker + ' currently being held')


    def last_price(self, ticker):
        '''
        Get current price of coin in BTC
        '''
        r = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-' + ticker)
        json_parse = json.loads(r.text, parse_float=Decimal)
        last_price = json_parse['result'][0]['Last']
        return last_price


    def fifteen_minute_check(self):
        '''
        Checks every fifteen minutes if the price has fluctuated 10%
        If it has gone up 10% it sells
        If it has gone down 10% it buys
        '''

        max_units_to_buy = self.my_balance('BTC')/float(self.last_price(self.ticker))

        # Set timer to 900 for 15min
        threading.Timer(900.0, self.fifteen_minute_check).start()

        print("\n{:%m-%d-%Y %H:%m:%S}".format(datetime.datetime.now()))
        print('Current {0} price: {1} BTC'.format(self.ticker, str(self.last_price(self.ticker))))
        print('Bought price: {0} BTC'.format(str(self.price_bought)))
        print('{0} holdings: {1} Coins\n'.format(self.ticker, str(self.my_balance(self.ticker))))

        # Price check. If price is greater than bought price, sell
        if float(self.last_price(self.ticker)) >= float(self.price_bought) + (float(self.price_bought) * .1):
            print("{:%m-%d-%Y %H:%m:%S}".format(
                datetime.datetime.now()) + ' Current coin price is higher than 10% of bought price.')
            # print(self.my_bittrex.trade_sell('BTC-' + self.ticker, 'LIMIT', self.my_balance(self.ticker), self.last_price(self.ticker), 'GOOD_TIL_CANCELLED', 'NONE', 0.0))
            print("{:%m-%d-%Y %H:%m:%S}".format(
                datetime.datetime.now()) + ' Sell limit has been placed for {0} {1} for {2} BTC. at \n'.format(str(self.my_balance(self.ticker)),
                                                                                 self.ticker,
                                                                                 str(self.last_price(self.ticker))))
            self.bag_hold = False

        # Price check. If price is less than bough price, buy
        if float(self.last_price(self.ticker)) <= float(self.price_bought) + (float(self.price_bought) * .1):
            print("{:%m-%d-%Y %H:%m:%S}".format(
                datetime.datetime.now()) + ' Current coin price is lower than 10% of bought price.')
            if self.bag_hold is True:
                print("{:%m-%d-%Y %H:%m:%S}".format(datetime.datetime.now()) +' Already holding coins, not buying more.\n')
            else:
                # self.my_bittrex.buy_limit(self.ticker, max_units_to_buy, self.last_price(self.ticker))
                print("{:%m-%d-%Y %H:%m:%S}".format(datetime.datetime.now()) + ' Buy limit has been placed for {0} {1} '
                                                                               'for {2} BTC.\n'.format(str(max_units_to_buy), self.ticker,
                                                                                    str(self.last_price(self.ticker))))


bot = CryptoBot()

bot.fifteen_minute_check()