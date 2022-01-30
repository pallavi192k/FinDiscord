import os
import robin_stocks
from dotenv import load_dotenv
load_dotenv()

robin_stocks.login('wenpurdue101@gmail.com', os.getenv('password'))
print(robin_stocks.stocks.get_latest_price('AMZN'))
print(robin_stocks.stocks.get_ratings('AMZN'))
print(robin_stocks.stocks.get_stock_historicals('AMZN'))



