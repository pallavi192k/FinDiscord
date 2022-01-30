from robin_stocks.robin_stocks import robin_stocks

from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

def order_information(symbol, quantity, buy_sell=None, limit_price=None, stop_price=None, timeout_code=None):

    message = create_simple_message('Company', symbol)
    message = create_simple_message('Symbol', symbol, embed=message)
    message = create_simple_message('Quantity', quantity, embed=message)
    message = create_simple_message('Buy or Sell', buy_sell, embed=message)
    message = create_simple_message('Limit Price', limit_price, embed=message)
    message = create_simple_message('Stop Price', stop_price, embed=message)
    message = create_simple_message('Timeout Code', timeout_code, embed=message)
    message.title = '✅ Order Placed - Details:'
    return message


class UserCommandTrade(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        limit_price, stop_price, quantity, amountInDollars = 1.0, 1.0, 1, 1.0
        buy_sell = 'N/A'
        if '$order ' in self.content:
            stock = self.content.replace('$order ', '').upper().split()
            symbol, quantity, buy_sell, limit_price, stop_price, timeout_code = stock
            confirmation = r.order(str(symbol), int(quantity), (str(buy_sell)).lower(), float(limit_price),
                                   float(stop_price), (str(timeout_code)).lower())

        elif '$order_buy_market ' in self.content:
            stock = self.content.replace('$order_buy_market ', '').upper().split()
            symbol, quantity, timeout_code = stock
            confirmation = r.order_buy_market(str(symbol), int(quantity), str(timeout_code).lower())

        elif '$order_sell_market ' in self.content:
            stock = self.content.replace('$order_sell_market ', '').upper().split()
            symbol, quantity, buy_sell, limit_price, stop_price, timeout_code = stock
            confirmation = r.order_sell_market(str(symbol), int(quantity), str(timeout_code).lower())

        elif '$order_buy_limit ' in self.content:
            stock = self.content.replace('$order_buy_limit ', '').upper().split()
            symbol, quantity, limit_price, timeout_code = stock
            confirmation = r.order_buy_limit(str(symbol), int(quantity), float(limit_price), str(timeout_code).lower())

        elif '$order_sell_limit ' in self.content:
            stock = self.content.replace('$order_sell_limit ', '').upper().split()
            symbol, quantity, limit_price, timeout_code = stock
            confirmation = r.order_sell_limit(str(symbol), int(quantity), float(limit_price), str(timeout_code).lower())

        elif '$order_buy_stop_loss ' in self.content:
            stock = self.content.replace('$order_buy_stop_loss ', '').upper().split()
            symbol, quantity, stop_price, timeout_code = stock
            confirmation = r.order_buy_stop_loss(str(symbol), int(quantity), float(stop_price),
                                                 str(timeout_code).lower())

        elif '$order_sell_stop_loss ' in self.content:
            stock = self.content.replace('$order_sell_stop_loss ', '').upper().split()
            symbol, quantity, stop_price, timeout_code = stock
            confirmation = r.order_sell_stop_loss(str(symbol), int(quantity), float(stop_price),
                                                  str(timeout_code).lower())

        elif '$order_buy_trailing_stop ' in self.content:
            stock = self.content.replace('$order_buy_trailing_stop ', '').upper().split()
            symbol, quantity, trailAmount, trailType, timeout_code = stock
            confirmation = r.order_buy_trailing_stop(str(symbol), int(quantity), float(trailAmount),
                                                     (str(trailType)).lower(), str(timeout_code).lower())

        elif '$order_sell_trailing_stop ' in self.content:
            stock = self.content.replace('$order_sell_trailing_stop ', '').upper().split()
            symbol, quantity, trailAmount, trailType, timeout_code = stock
            confirmation = r.order_sell_trailing_stop(str(symbol), int(quantity), float(trailAmount), str(trailType),
                                                      str(timeout_code).lower())

        elif '$order_sell_stop_limit ' in self.content:
            stock = self.content.replace('$order_sell_stop_limit ', '').upper().split()
            symbol, quantity, limit_price, stop_price, timeout_code = stock
            confirmation = r.order_sell_stop_limit(str(symbol), int(quantity), float(limit_price), float(stop_price),
                                                   (str(timeout_code)).lower())

        elif '$order_buy_crypto_limit_by_price ' in self.content:
            stock = self.content.replace('$order_buy_crypto_limit_by_price ', '').upper().split()
            symbol, amountInDollars, limit_price, timeout_code = stock
            print(str(symbol), float(amountInDollars), float(limit_price), (str(timeout_code)).lower())
            confirmation = r.order_buy_crypto_limit_by_price(str(symbol), float(amountInDollars), float(limit_price), (str(timeout_code)).lower())

        elif '$order_buy_crypto_by_quantity ' in self.content:
            stock = self.content.replace('$order_buy_crypto_by_quantity ', '').upper().split()
            symbol, quantity, timeout_code = stock
            confirmation = r.order_buy_crypto_by_quantity(str(symbol), int(quantity), (str(timeout_code)).lower())

        elif '$order_sell_crypto_limit_by_price ' in self.content:
            stock = self.content.replace('$order_sell_crypto_limit_by_price ', '').upper().split()
            symbol, amountInDollars, limit_price, timeout_code = stock
            confirmation = r.order_sell_crypto_limit_by_price(str(symbol), float(amountInDollars), float(limit_price), (str(timeout_code)).lower())

        elif 'order_sell_crypto_limit ' in self.content:
            stock = self.content.replace('$order_buy_crypto_by_quantity ', '').upper().split()
            symbol, quantity, limit_price, timeout_code = stock
            confirmation = r.order_sell_crypto_limit(str(symbol), int(quantity), float(limit_price), (str(timeout_code)).lower())
        print(confirmation)
        message = order_information(symbol, quantity, buy_sell, limit_price, stop_price, timeout_code)

        if 'id' not in confirmation:
            message = create_simple_message('❌ Order Failed - Details', [j for i,j in confirmation.items()])


        self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
