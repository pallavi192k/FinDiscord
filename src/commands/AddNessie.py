from purdue_brain.feature.nessie import Nessie, get_merchant_details
from purdue_brain.wrappers.discord_wrapper import DiscordWrapper
from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message


class UserAddApiKey(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    def create_customer_and_user(self):
        nessie_property = DiscordWrapper.fire.get_property('nessie_customer_id', self.author.id, None)
        if nessie_property is None:
            nessie = Nessie(None, None)
            response = nessie.create_customer() and nessie.create_account()
            DiscordWrapper.fire.set_property('nessie_customer_id', self.author.id,
                                             {'customer_id': nessie.customer_id, 'account_id': nessie.account_id})
            return response
        else:
            return False

    async def run(self):
        response = self.create_customer_and_user()
        if response:
            message = create_simple_message('Added Account', 'Successfully Added Key to Profile')
            self.response.add_response(message, True)
            self.response.done = True
        else:
            message = create_simple_message('Error', 'You already connected a bank account.')
            self.response.add_response(message, False)
            self.response.set_state(False, done=True)


class GetAccountInfo(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    def add_recent_purchases(self, nessile):
        message = None
        purchases = nessile.get_purchases()
        if purchases is not None:
            purchases.reverse()
            for i in purchases[:15]:
                merchant_details = get_merchant_details(i['merchant_id'])
                title = merchant_details['name'] if merchant_details else 'Unknown'
                message = create_simple_message(title, 'Amount: ${:.2f}'.format(i['amount']), embed=message)
        if message is not None:
            message.title = "Recent Purchases"
            self.response.add_response(message)

    def account_details(self, nessile):
        account_details = nessile.get_customer_data()
        if account_details and 'nickname' in account_details and 'balance' in account_details:
            message = create_simple_message(f'Account: {account_details["nickname"]}',
                                            'Balance: ${:.2f}'.format(account_details["balance"]))
            self.response.add_response(message)
        else:
            self.response.set_error_response(0, True)

    async def run(self):
        nessile = Nessie.get_nessile_from_user_id(author_id=self.author.id)
        if nessile is None:
            message = create_simple_message('Bank Issue', 'DM bot $add_bank to add your bank')
            self.response.add_response(message, False)
            self.response.set_state(False, True)
        else:
            self.account_details(nessile)
            self.add_recent_purchases(nessile)
            self.response.done = True
