from robin_stocks.robin_stocks import robin_stocks

from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os


class UserCommandStockPredict(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        minPE = 256
        if '$stocks_from_market ' in self.content:
            stock = self.content.replace('$stocks_from_market ', '').upper().split()
            tag = stock[0]
            market_info = (r.markets.get_all_stocks_from_market_tag(str(tag).lower()))
            for i in market_info:
                fundList = r.stocks.get_fundamentals((i['symbol']))
                fundDict = fundList[0]
                print(fundDict)
                print(i)
                if(fundDict['pe_ratio'] != None):
                    if minPE >= float(fundDict['pe_ratio']):
                        minPE = float((fundDict['pe_ratio']))
                        symbol = i['symbol']

        message = 'My recommendation for the ' + str(tag).lower() + ' industry is ' + symbol
        self.response.add_response(message, True)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
