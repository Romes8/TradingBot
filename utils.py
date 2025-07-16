
import pandas as pd

from dotenv import load_dotenv

import matplotlib.pyplot as plt
import mplfinance as mpf
import json

import urllib

def build_dynamic_bars_url(symbol, timeframe_str, start_date, end_date, limit, adjustment='raw', feed='sip', currency='USD', sort='asc'):
    base_url = "https://data.alpaca.markets/v2/stocks/bars"
    
    # Format dates as ISO 8601 strings (e.g., '2024-07-15T00:00:00Z')
    start_iso = start_date.isoformat()
    end_iso = end_date.isoformat()
    
    # Query parameters as dict (insert pre-coded values)
    params = {
        'symbols': symbol,
        'timeframe': timeframe_str,  # e.g., '5Min'
        'start': start_iso,
        'end': end_iso,
        'limit': str(limit),  # Convert to string
        'adjustment': adjustment,
        'feed': feed,
        'currency': currency,
        'sort': sort
    }
    
    # Encode params safely (handles %3A for :, etc.)
    encoded_params = urllib.parse.urlencode(params, doseq=True)
    
    # Full URL
    full_url = f"{base_url}?{encoded_params}"
    return full_url

# Used to visualize data as an image
def visualize_tesla_data(response_json):        
    data = response_json.get('bars', {}).get('NVDA', []) #change this based on the stock name
    if not data:
        print("No data found in JSON.")
        return
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    
    # Rename columns to standard OHLCV for plotting
    df = df.rename(columns={
        'o': 'Open',
        'h': 'High',
        'l': 'Low',
        'c': 'Close',
        'v': 'Volume',
        't': 'Date'  # Timestamp column
    })
    
    # Convert timestamp to datetime and set as index
    df['Date'] = pd.to_datetime(df['Date'])  # Assumes ISO format like "2025-07-15T08:00:00Z"
    df = df.set_index('Date')
    
    # Ensure required columns are present and numeric
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
    
    # Plot candlestick chart with volume
    mpf.plot(
        df,
        type='candle',  # Candlestick style
        style='charles',  # A clean style (options: 'yahoo', 'binance', etc.)
        title=f'5-Minute Bars (Latest Data)',
        ylabel='Price ($)',
        volume=True,  # Overlay volume panel
        mav=(3, 6),  # Optional: Add moving averages (3-period and 6-period)
        figratio=(12, 6),  # Figure size
        savefig='latest_candlestick.png'  # Save to file (optional)
    )
    
    # Show the plot (non-blocking, so script continues)
    plt.show(block=False)
    print("Visualization complete. Chart displayed and saved as 'latest_candlestick.png'.")