from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

class UserCommandHelp(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        message = create_simple_message('$help', 'Gives a brief description of each command')
        message = create_simple_message('$price [SYMBOL]', 'Gives the current price of the stock', embed=message)
        message = create_simple_message('$info [SYMBOL]', "Gives some general information about the stock and it's company", embed=message)
        message = create_simple_message('$trade_info [SYMBOL]', "Gives detailed information about the stock", embed=message)
        message = create_simple_message('$deposit [USD]', "Allows you to deposit money from your connected bank account", embed=message)
        message = create_simple_message('$withdraw [USD]', "Allows you to withdraw money to your connected bank account", embed=message)
        message = create_simple_message('$equity', "Gives you information about your total portfolio's equity, including daily gains/losses", embed=message)
        message = create_simple_message('$add_bank', "Connects your capital one bank account to the bot", embed=message)
        message = create_simple_message('$trade_help', 'Gives detailed information about trading commands', embed=message)
        message = create_simple_message('$stocks_from_market [MARKET TAG]', 'Possible Tags: https://mattrode.com/blog/robinhood-collections-list/', embed=message)
        self.response.set_state(True)
        self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
