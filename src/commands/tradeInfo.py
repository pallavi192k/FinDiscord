from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os


def company_trading_info(name, symbol, open, high, low, volume, average_volume_2_weeks, high52weeks, low52weeks,
                         dividend_yield, floatt, market, pb_ratio, pe_ratio, shares_outstanding,
                         link):
    message = create_simple_message('Company', name)
    message = create_simple_message('Symbol', symbol, embed=message)
    message = create_simple_message('Open price', '${:,.2f}'.format(float(open)), embed=message)
    message = create_simple_message('High price', '${:,.2f}'.format(float(high)), embed=message)
    message = create_simple_message('Low price', '${:,.2f}'.format(float(low)), embed=message)
    message = create_simple_message('High price average (52 weeks)', '${:,.2f}'.format(float(high52weeks)),
                                    embed=message)
    message = create_simple_message('Low price average (52 weeks)', '${:,.2f}'.format(float(low52weeks)), embed=message)
    message = create_simple_message('Volume', '{:,.2f}'.format(float(volume)), embed=message)
    message = create_simple_message('Average Volume (2 weeks)', '{:,.2f}'.format(float(average_volume_2_weeks)), embed=message)
    message = create_simple_message('Dividend Yield', dividend_yield, embed=message)
    message = create_simple_message('Float', '{:,.2f}'.format(float(floatt)), embed=message)
    message = create_simple_message('Market cap', '${:,.2f}'.format(float(market)), embed=message)
    message = create_simple_message('pb ratio', '{:,.4f}'.format(float(pb_ratio)), embed=message)
    message = create_simple_message('pe ratio', '{:,.4f}'.format(float(pe_ratio)), embed=message)
    message = create_simple_message('Shares outstanding', '{:,.2f}'.format(float(shares_outstanding)), embed=message)
    message = create_simple_message('More info', link, embed=message)
    return message


class UserCommandTradeInfo(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        stock = self.content.replace('$trade_info ', '').upper().split()
        for s in stock:
            instrumental_data = r.stocks.find_instrument_data(s)
            fund = r.stocks.get_fundamentals(s)

            for d, d2 in zip(fund, instrumental_data):
                if None in [d, d2]:
                    message = "'" + s + "' stock symbol doesn't exist."
                    self.response.set_state(False)
                    self.response.add_response(message)
                    continue
                name = d2['simple_name']
                symbol = d2['symbol']
                open = d['open']
                high = d['high']
                low = d['low']
                volume = d['volume']
                average_volume_2_weeks = d['average_volume_2_weeks']
                high52weeks = d['high_52_weeks']
                low52weeks = d['low_52_weeks']
                dividend_yield = d['dividend_yield']
                floatt = d['float']
                market = d['market_cap']
                pb_ratio = d['pb_ratio']
                pe_ratio = d['pe_ratio']
                shares_outstanding = d['shares_outstanding']
                link = 'https://robinhood.com/stocks/' + symbol

                message = company_trading_info(name, symbol, open, high, low, volume, average_volume_2_weeks,
                                               high52weeks, low52weeks,
                                               dividend_yield, floatt, market, pb_ratio, pe_ratio, shares_outstanding,
                                               link)
                self.response.set_state(True)
                self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
