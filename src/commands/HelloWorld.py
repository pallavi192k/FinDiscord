from purdue_brain.commands.command import UserCommand
from purdue_brain.common import UserResponse, create_simple_message
import robin_stocks as r

class UserCommandHelloWorld(UserCommand):

    def __init__(self, author, content, response: UserResponse):
        super().__init__(author, content, response)
        print(content)

    async def run(self):
        message = create_simple_message("FinDiscord", "Says Hello")
        message = create_simple_message("AMZN", '$' + r.stocks.get_latest_price('Amzn')[0])
        self.response.add_response(message, True)

