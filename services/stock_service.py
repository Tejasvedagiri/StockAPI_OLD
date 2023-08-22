import pandas as pd
from constants import rename_cols
import yfinance as yf
import random
import numpy as np

def get_dividens_bar_grap_data(db):
    query = f"SELECT * FROM `transaction` where TransactionCode = 'CDIV'"
    
    df = pd.read_sql(query, db)
    df['ProcessDate'] = pd.to_datetime(df['ProcessDate'])
    df["Year"] = df['ProcessDate'].dt.year
    df["Month"] = df['ProcessDate'].dt.month
    result = df.groupby([df['Instrument'], df['Year'], df["Month"] ])['Amount'].sum().reset_index()
    return result[["Year", "Month", "Instrument", "Amount"]]

def price_chart(db):
    query = f"SELECT Instrument, abs(sum(Amount)) as AMOUNT  FROM `transaction` GROUP BY Instrument ORDER BY AMOUNT DESC LIMIT 5"

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


    