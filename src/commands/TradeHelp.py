from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

class UserCommandTradeHelp(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        message = create_simple_message('Stocks:', 'Gives a brief description of each stock command. ')
        message = create_simple_message('Generic Order', '$order [SYMBOL] [QUANTITY] ["BUY" OR "SELL"] [LIMIT PRICE] [STOP PRICE] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Market Buy', '$order_buy_market [SYMBOL] [QUANTITY] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Market Sell', '$order_sell_market [SYMBOL] [QUANTITY] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Limit Buy', '$order_buy_limit [SYMBOL] [QUANTITY] [LIMIT PRICE] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Limit Sell', '$order_sell_limit [SYMBOL] [QUANTITY] [LIMIT PRICE] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Stop Loss Buy', '$order_buy_stop_loss [SYMBOL] [QUANTITY] [STOP PRICE] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Stop Loss Sell', '$order_sell_stop_loss [SYMBOL] [QUANTITY] [STOP PRICE] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Trailing Stop Buy', '$order_buy_trailing_stop [SYMBOL] [QUANTITY] [TRAIL AMOUNT] [TRAIL TYPE] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Trailing Stop Sell', '$order_sell_trailing_stop [SYMBOL] [QUANTITY] [TRAIL AMOUNT] [TRAIL TYPE] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Stop Limit Sell', '$order_sell_stop_limit [SYMBOL] [QUANTITY] [LIMIT PRICE] [STOP PRICE] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Notes:','Timeout codes: gtc’ = good until cancelled.‘gfd’ = good for the day.‘ioc’ = immediate or cancel.‘opg’ execute at opening.\nTrailType: could be “amount” or “percentage"', embed=message)

        message = create_simple_message('\nCrypto:', 'Gives a brief description of each crypto command. ', embed=message)
        message = create_simple_message('Buy Crypto Limit By Price', '$order_buy_crypto_limit_by_price [SYMBOL] [QUANTITY] [STOP PRICE] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Buy Crypto By Quantity', '$order_buy_crypto_by_quantity [SYMBOL] [QUANTITY] [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Sell Crypto Limit', '$order_sell_crypto_limit [SYMBOL] [QUANTITY] [LIMIT PRICE]  [TIMEOUT CODE]', embed=message)
        message = create_simple_message('Sell Crypto Limit By Price','$order_sell_crypto_limit [SYMBOL] [AMOUNT] [LIMIT PRICE]  [TIMEOUT CODE]', embed=message)



        self.response.set_state(True)
        self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
