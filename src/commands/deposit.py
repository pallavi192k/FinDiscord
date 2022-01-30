from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

from purdue_brain.feature.nessie import Nessie


class UserCommandDeposit(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    def parse_transaction(self, args, display_arg, d):
        list_dict = r.account.deposit_funds_to_robinhood_account(d['url'], args)
        did_perform = True
        try:
            message = '✅ Deposit successful: ' + '${:,.2f}'.format(display_arg) + ' is currently ' + list_dict[
                'state']
        except:
            did_perform = False
            message = '❌ Deposit unsuccessful.'
        return did_perform, message

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        args = self.content.replace('$deposit ', '').upper()
        details = r.account.get_linked_bank_accounts()
        nessile = Nessie.get_nessile_from_user_id(author_id=self.author.id)
        for d in details:
            try:
                args = float(args)
                if args <= 0 or args > 500:
                    message = "🛑 Deposit Stopped: Amount needs to be between $0.01 and $499.99"
                    successful = False
                elif os.getenv('CONNECT') == 'True':
                    successful, message = self.parse_transaction(args, args, d)
                    nessile.perform_purchase(args, description='${:2f} added to Robinhood'.format(args))
                else:
                    successful, message = self.parse_transaction(0.01, args, d)
                    nessile.perform_purchase(args, description='${:2f} added to Robinhood'.format(args))
                self.response.add_response(message)
            except:
                message = '❌ Error: Make sure to include only numbers in your command!'
                self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True

class UserCommandWithdraw(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    def parse_withdraw(self, args, display_arg, d):
        list_dict = r.account.withdrawl_funds_to_bank_account(d['url'], args)
        did_perform = True
        try:
            message = '✅ Withdrawal successful: ' + '${:,.2f}'.format(display_arg) + ' is currently ' + list_dict[
                'state']
        except:
            did_perform = False
            message = '❌ Withdrawal unsuccessful.'
        return did_perform, message

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        args = self.content.replace('$withdraw ', '').upper()
        details = r.account.get_linked_bank_accounts()
        nessile = Nessie.get_nessile_from_user_id(author_id=self.author.id)
        for d in details:
            try:
                args = float(args)
                if args <= 0 or args > 500:
                    message = "🛑 Withdrawal Stopped: Amount needs to be between $0.01 and $499.99"
                    successful = False
                elif os.getenv('CONNECT') == 'True':
                    successful, message = self.parse_withdraw(args, args, d)
                    nessile.add_money_to_account(args, description='Money from Robinhood')
                else:
                    successful, message = self.parse_withdraw(0.01, args, d)
                    nessile.add_money_to_account(args, description='Money from Robinhood')
                self.response.add_response(message)
            except:
                message = '❌ Error: Make sure to include only numbers in your command!'
                self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
