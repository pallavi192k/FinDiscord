import asyncio
from random import random

import discord
import os
from dotenv import load_dotenv

from purdue_brain.commands.AddNessie import UserAddApiKey, GetAccountInfo
from purdue_brain.commands.HelloWorld import UserCommandHelloWorld
from purdue_brain.commands.NewCommand import UserCommandNewCommand
from purdue_brain.commands.cryptoInfo import UserCommandCryptoInfo
from purdue_brain.commands.deposit import UserCommandDeposit, UserCommandWithdraw
from purdue_brain.commands.help import UserCommandHelp
from purdue_brain.commands.TradeHelp import UserCommandTradeHelp
from purdue_brain.commands.Trade import UserCommandTrade
from purdue_brain.commands.stockprediction import UserCommandStockPredict
from purdue_brain.commands.price import UserCommandPrice
from purdue_brain.commands.info import UserCommandInfo
from purdue_brain.commands.command import UserCommand
from purdue_brain.commands.details import UserCommandDetails
from purdue_brain.commands.tradeInfo import UserCommandTradeInfo
from purdue_brain.common import UserResponse
from purdue_brain.common.utils import iterate_commands, create_simple_message
from purdue_brain.feature.nessie import get_merchants
from purdue_brain.feature.user_iterator import UserIterator
from purdue_brain.wrappers.discord_wrapper import DiscordWrapper
from purdue_brain.wrappers.firebase_wrapper import FirebaseWrapper

load_dotenv()
client = discord.Client()
DiscordWrapper.client = client
DiscordWrapper.fire = FirebaseWrapper()
discord_wrapper = DiscordWrapper()


@client.event
async def on_ready():
    pass


public_commands = [
    ('$price', UserCommandPrice), ('$info', UserCommandInfo),
    ('$trade_info', UserCommandTradeInfo), ('$help', UserCommandHelp), ('$trade_help', UserCommandTradeHelp),
    ('$order', UserCommandTrade),
    ('$order_buy_market', UserCommandTrade), ('$order_sell_market', UserCommandTrade),
    ('$order_buy_limit', UserCommandTrade),
    ('$order_sell_limit', UserCommandTrade), ('$order_buy_stop_loss', UserCommandTrade),
    ('$order_buy_trailing_stop', UserCommandTrade), ('$order_sell_trailing_stop', UserCommandTrade),
    ('$order_trailing_stop', UserCommandTrade),
    ('$order_sell_stop_limit', UserCommandTrade), ('$crypto_price', UserCommandCryptoInfo),
    ('$equity', UserCommandDetails), ('$stocks_from_market', UserCommandStockPredict),
]

private_commands = [
    ('$add_bank', UserAddApiKey), ('$deposit', UserCommandDeposit), ('$withdraw', UserCommandWithdraw),
    ('$equity', UserCommandDetails), ('$recent', GetAccountInfo)
]


def create_channel_command(content):
    return iterate_commands(content, public_commands)


def create_direct_command(content):
    return iterate_commands(content, public_commands + private_commands)


async def run(obj, message, response, is_dm=False):
    if obj is not None:
        inst: UserCommand = obj(message.author, message.content, response)
        if type(inst) == UserCommandDetails:
            inst.show_all = is_dm
        await response.send_loading(message)
        await inst.run()


async def handle_channel_message(message, response: UserResponse):
    if not response.done:
        if type(message.channel) is discord.TextChannel and str(message.channel.id) == os.getenv('DISCORD_CHANNEL'):
            content = message.content.lower()
            await run(create_channel_command(content), message, response)
        if type(message.channel) is discord.DMChannel:
            content = message.content.lower()
            await run(create_direct_command(content), message, response, is_dm=True)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response: UserResponse = UserResponse()
    await handle_channel_message(message, response)
    if response.done:
        await response.send_message(message)
        return


async def random_purchases_and_deposits():
    iterator = UserIterator()
    while True:
        all_merchants = get_merchants()
        for k, v in iterator:
            deposit_money = int(random() * 2) > 1
            if deposit_money:
                v.add_money_to_account(random() * 1000, 'Payment from mwenclubhouse')
            else:
                random_merchant_idx = int(random() * len(all_merchants))
                v.perform_purchase(random() * 1000, all_merchants[random_merchant_idx]['_id'])
        await asyncio.sleep(600)


async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    discord_channel = int(os.getenv('DISCORD_CHANNEL'))
    channel = client.get_channel(discord_channel)
    while True:
        counter += 1
        message = create_simple_message('Hello There', f'counter: {counter}')
        # await channel.send(embed=message)
        await asyncio.sleep(10)  # task runs every 60 seconds

def run_discord():
    client.loop.create_task(random_purchases_and_deposits())
    client.loop.create_task(my_background_task())
    client.run(os.getenv('TOKEN'))
