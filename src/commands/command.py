from purdue_brain.common.user_response import UserResponse


class UserCommand:

    def __init__(self, author, content, response: UserResponse):
        self.author = author
        self.content = content
        self.response = response

    async def run(self):
        self.response.set_error_response(0, True)
