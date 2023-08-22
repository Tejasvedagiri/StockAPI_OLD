import pandas as pd
from constants import rename_cols
import yfinance as yf
import random
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytz
import concurrent.futures



def get_dividens_bar_grap_data(db):
    query = f"SELECT Distinct Instrument as Instrument FROM `transaction` where TransactionCode = 'CDIV' and Instrument not in (Select Instrument from `transaction` where TransactionCode = 'Sell')"
    
    df = pd.read_sql(query, db)
    instruments = df["Instrument"].to_list()
    end_date = datetime.datetime.now(pytz.utc)
    start_date = end_date - datetime.timedelta(days=200)


    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_dividend_data, instruments, [start_date]*len(instruments), [end_date]*len(instruments))
        dividend_data = {stock_symbol: dividends for stock_symbol, dividends in results}
    
    green = generate_color("tab20b", 20)
    lineData = []
    for key, df in dividend_data.items():
        content = {}
        content["data"] = []
        content["id"] = key
        content["color"] = green.pop()
        for _, row in df.iterrows():
            content["data"].append({"x": f"{row['Year']}-{row['Month']}", "y": row['Dividends']})
        lineData.append(content)
        
    return lineData

def price_chart(db):
    query = f"SELECT Instrument, abs(sum(Amount)) as AMOUNT  FROM `transaction` GROUP BY Instrument ORDER BY AMOUNT DESC LIMIT 10"

    df = pd.read_sql(query, db).dropna()
    instruments = df["Instrument"].to_list()
    
    lineData = []

    green_colors = generate_color_shades("green", len(instruments))
    red_colors = generate_color_shades("red", len(instruments))
    for symbol in instruments:
        content = {}
        content["id"] = symbol
        content["data"] = []

        data = yf.download(symbol, period='14d', progress=False)['Adj Close']
        for index, value in data.items():
            content["data"].append({"x": str(f"{index.month}-{index.day}"), "y": np.round(value, decimals=2)})
        content["color"] = green_colors.pop() if content["data"][0]["y"] < content["data"][-1]["y"] else red_colors.pop()
        lineData.append(content)
    
    return lineData

def generate_color_shades(base_color, num_shades):
    shades = []
    red = random.sample(range(150, 250 + 1), num_shades)
    green = random.sample(range(150, 250 + 1), num_shades)
    for i in range(num_shades):

        r = red[i] if base_color=="red" else 0 
        g = green[i] if base_color=="green" else 0  
        b = 0 

        hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        shades.append(hex_color)

    return shades

def generate_color(palette_name, num_colors):
    cmap = plt.get_cmap(palette_name)
    hex_colors = ['#%02x%02x%02x' % tuple(int(255 * rgba) for rgba in cmap(i)[:3]) for i in range(num_colors)]
    return hex_colors

def fetch_dividend_data(stock_symbol, start_date, end_date):
    ticker = yf.Ticker(stock_symbol)
    dividends = ticker.dividends.loc[start_date:end_date]
    dividends = dividends.resample('M').ffill()
    dividends = pd.DataFrame(dividends).reset_index()
    dividends['Year'] = dividends['Date'].dt.year
    dividends['Month'] = dividends['Date'].dt.month
    dividends.drop(columns=['Date'], inplace=True)

    return stock_symbol, dividends


    