import datetime
import os
from dotenv import load_dotenv
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import CryptoBarsRequest

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, StopOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import pandas as pd

import os
from dotenv import load_dotenv
import datetime  # Add this for date handling
import pytz
import requests

import matplotlib.pyplot as plt
import mplfinance as mpf

import utils as ut

from zoneinfo import ZoneInfo  # Built-in for Python 3.9+; or import pytz
import datetime
import pytz


load_dotenv()

# Configuration (Customize!)
API_KEY =  os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL =  os.getenv('TEST_API_BASE_URL')
DATA_URL = os.getenv('DATA_URL')

#check the real stock https://app.alpaca.markets/trade/NVDA?asset_class=stocks
SYMBOL = 'NVDA'  # Asset
TIMEFRAME = TimeFrame(5, TimeFrame.Minute)  # Updated to SDK's TimeFrame for 5Min
RISK_PER_TRADE = 0.01  # 1% of account
STOP_LOSS_PCT = 0.005  # 0.5% for quick exits
TAKE_PROFIT_PCT = 0.01  # 1% target
DAILY_LOSS_LIMIT = 0.02  # Halt if >2% daily loss

data_client = StockHistoricalDataClient(API_KEY, API_SECRET)  # For market data
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)  # For trading in paper mode


def get_data(symbol, timeframe, limit=100):

    client = CryptoHistoricalDataClient()

    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=timeframe, 
        limit=limit,
        start=None,
        end=datetime.datetime.now()
    )

    bars = data_client.get_stock_bars(request_params)
    df = df[['open', 'high', 'low', 'close', 'volume']] #choose bars which you need
    return df

def fetch_data():
    copenhagen_tz = pytz.timezone('Europe/Copenhagen')

    current_time = datetime.datetime.now(copenhagen_tz)

    end_date = current_time - datetime.timedelta(days=1)

    start_date = current_time - datetime.timedelta(days=2)
    print(start_date)
    print(end_date)


    full_url = ut.build_dynamic_bars_url(
        symbol=SYMBOL,
        timeframe_str=TIMEFRAME,
        start_date=start_date,
        end_date=end_date,
        limit=5000,
        adjustment='raw',
        feed='sip',  # Or 'iex' for free tier
        currency='USD',
        sort='asc'
    )
    
    url = full_url
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": API_SECRET
    }

    response = requests.get(url, headers=headers)

    return response.json()


if __name__=="__main__":
    print("Staring the bot...")
    print("Getting data...")
    ut.visualize_tesla_data(fetch_data())  
