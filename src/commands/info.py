from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os


def cut_off_sentence(details):
    cut_it_off = len(details) > 500
    new_details = details[:500]
    last_period_idx = new_details.rfind('.')

    if cut_it_off:
        new_details = new_details[:last_period_idx + 1]

    return new_details


def company_stock_info(name, symbol, price, market, details, industry, link):
    message = create_simple_message('Company', name)
    message = create_simple_message('Symbol', symbol, embed=message)
    message = create_simple_message('Price per share', '${:,.2f}'.format(float(price)), embed=message)
    message = create_simple_message('Market cap', '${:,.2f}'.format(float(market)), embed=message)
    message = create_simple_message('About', f'{cut_off_sentence(details)}', embed=message)
    message = create_simple_message('Industry', industry, embed=message)
    message = create_simple_message('More info', link, embed=message)
    return message


class UserCommandInfo(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        stock = self.content.replace('$info ', '').upper().split()
        for s in stock:
            instrumental_data = r.stocks.find_instrument_data(s)
            fund = r.stocks.get_fundamentals(s)

            for d, f in zip(instrumental_data, fund):
                if None in [d, f]:
                    message = "❌ '" + s + "' stock symbol doesn't exist."
                    self.response.add_response(message)
                    continue
                name = d['simple_name']
                symbol = d['symbol']
                price = r.stocks.get_latest_price(symbol)[0]
                link = 'https://robinhood.com/stocks/' + symbol

                details = f['description']
                market = f['market_cap']
                industry = f['industry']

                message = company_stock_info(name, symbol, price, market, details, industry, link)
                self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
