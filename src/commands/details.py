from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

from purdue_brain.common.utils import get_attribute

def findEquity(market_value, crypto, total_equity, change, show_all_equity=True):
    message = None
    if show_all_equity:
        message = create_simple_message('Total Equity', '${:,.2f}'.format(float(total_equity)), embed=message)
        message = create_simple_message('Stock Value', '${:,.2f}'.format(float(market_value)), embed=message)
        message = create_simple_message('Crypto Value', '${:,.2f}'.format(float(crypto)), embed=message)
    message = create_simple_message('Daily Change', '{:,.5f}%'.format(float(change)), embed=message)
    return message


class UserCommandDetails(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)
        self.show_all = True

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        profile = r.account.load_phoenix_account()
        market_value = get_attribute(profile, ['equities', 'market_value', 'amount'], default=0)
        equity = get_attribute(profile, ['total_equity', 'amount'], default=0)
        crypto_value = get_attribute(profile, ['crypto', 'market_value', 'amount'], default=0)
        curr = float(get_attribute(profile, ['portfolio_equity', 'amount'], default=0))
        prev = float(get_attribute(profile, ['portfolio_previous_close', 'amount'], default=0))
        change = (curr - prev) / prev * 100
        message = findEquity(market_value, crypto_value, equity, change, self.show_all)
        self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
