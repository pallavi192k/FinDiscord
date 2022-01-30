from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r
import os

class UserCommandCryptoInfo(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)

    async def run(self):
        r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
        crypto = self.content.replace('$crypto_price ', '').upper().split()
        for c in crypto:
            curr = r.get_crypto_info(c)
            if not curr:
                message = "❌ '" + c + "' Crypto symbol doesn't exist."
                self.response.add_response(message)
                continue
            for d in [curr]:
                name = d['name']
                symbol = c
                price = r.crypto.get_crypto_quote(c)
                for p in [price]:
                    cost = p['ask_price']
                message = name + ' (' + symbol + ') is currently worth' + '${:,.2f}'.format(float(cost))
                self.response.add_response(message)

        if len(self.response.response) == 0:
            self.response.set_error_response(0)
        self.response.done = True
