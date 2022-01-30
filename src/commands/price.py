from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

class UserCommandPrice(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)
        print(content)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        stock = self.content.replace('$price ', '').upper().split()

        # message = create_simple_message('self', self.content)
        # message = create_simple_message('title', self.content, embed=message)

        for s in stock:
            dict = r.stocks.find_instrument_data(stock)
            for d in dict:
                if None in [d]:
                    message = "❌ '" + s + "' stock symbol doesn't exist."
                    self.response.add_response(message)
                    continue

                message = create_simple_message(s, '$' + r.stocks.get_latest_price(s)[0])
                name = (d['simple_name'])
                stock = (d['symbol'])
                message = name + ' (' + stock + ')' + ' is currently worth ' + '${:,.2f}'.format(float(r.stocks.get_latest_price(stock)[0]))
        # message = create_simple_message('AAPL', '<a href="https://robinhood.com/stocks/aapl">APPL stock</a>', embed=message)
        self.response.add_response(message, True)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True