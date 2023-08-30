import pandas as pd
import yfinance as yf
import numpy as np
from utils import generate_color, generate_color_from_shades

import datetime
import pytz
import concurrent.futures
from services import data_services

def get_stock_sector(db):
    df = data_services.get_current_value(db)
    instruments = df["Instrument"].unique()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(getch_stock_sector, instruments)
        sectors = {instrument: sector for instrument, sector in results}
    df["Sector"] = df["Instrument"].map(sectors)

    sector_dict = {}
    for _, row in df.iterrows():
        content = {
            "name": row["Instrument"],
            "color": row["color"],
            "amount": row["Amount"]
        }
        if row["Sector"] not in sector_dict:
            sector_dict[row["Sector"]] = {
                "name" : row["Sector"],
                "color": "hsl(170, 70%, 50%)",
                "children": [],
                "amount": 0
            }
        sector_dict[row["Sector"]]["children"].append(content)
            

    result = {
        "name": "nivo",
        "color": "hsl(170, 70%, 50%)",
        "children" : list(sector_dict.values())
    }

    return result
def montly_dividens(db):
    query = f"SELECT * from `transaction` where TransactionCode = 'CDIV'"
    df = pd.read_sql(query, db)
    df = df[["ProcessDate", "Instrument", "Amount"]]
    df["ProcessDate"] = pd.to_datetime(df["ProcessDate"])
    df["Year"] = df["ProcessDate"].dt.year
    df["Month"] = df["ProcessDate"].dt.month
    df.sort_values(by=['ProcessDate'], inplace=True)
    color = generate_color("tab20", 3)

    df = df.groupby(['Year', 'Month']).agg({'Amount': 'sum'}).reset_index()
    content = {}
    content["id"] = "Dividends"
    content["color"] = color.pop()
    content["data"] = []
    for _, row in df.iterrows():
        content["data"].append({"x": f"{row['Year']}-{row['Month']}", "y": row['Amount']})

    return [content]

def current_dividends(db):
    query = f"SELECT * from `transaction` where TransactionCode = 'CDIV'"
    df = pd.read_sql(query, db)
    df = df[["ProcessDate", "Instrument", "Amount"]]
    df["ProcessDate"] = pd.to_datetime(df["ProcessDate"])
    df["Year"] = df["ProcessDate"].dt.year
    df["Month"] = df["ProcessDate"].dt.month


    df.sort_values(by=['ProcessDate'], inplace=True)
    color = generate_color("tab20", 30)
    aggregated_data = {}

    for _, row in df.iterrows():
        key = f"{row['Instrument']}"
        print(color)
        if key not in aggregated_data:
            aggregated_data[key] = {
                'data': [],
                'id': row['Instrument']
            }

        aggregated_data[key]['data'].append({'x': f"{row['Year']}-{row['Month']:02d}", 'y': row['Amount']})
        aggregated_data[key]['color'] = color.pop(1)

    # Convert the aggregated data dictionary to a list of dictionaries
    aggregated_data_list = list(aggregated_data.values())

    return aggregated_data_list

def get_dividens_bar_grap_data(db):
    query = f"SELECT Distinct Instrument as Instrument FROM `transaction` where TransactionCode = 'CDIV' and Instrument not in (Select Instrument from `transaction` where TransactionCode = 'Sell')"
    
    df = pd.read_sql(query, db)
    instruments = df["Instrument"].to_list()
    end_date = datetime.datetime.now(pytz.utc)
    start_date = end_date - datetime.timedelta(days=360)
    start_date = start_date.replace(day=1)


    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_dividend_data, instruments, [start_date]*len(instruments), [end_date]*len(instruments))
        dividend_data = {stock_symbol: dividends for stock_symbol, dividends in results}
    
    green = generate_color("tab20", 20)
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
    query = f"SELECT Instrument, abs(sum(Amount)) as AMOUNT  FROM `transaction` GROUP BY Instrument ORDER BY AMOUNT DESC LIMIT 11"

    df = pd.read_sql(query, db).dropna()
    instruments = df["Instrument"].to_list()
    
    lineData = []

    green_colors = generate_color_from_shades("green", len(instruments))
    red_colors = generate_color_from_shades("red", len(instruments))
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


def fetch_dividend_data(stock_symbol, start_date, end_date):
    ticker = yf.Ticker(stock_symbol)
    dividends = ticker.dividends.loc[start_date:end_date]
    if start_date not in dividends.index:
        dividends[start_date] = dividends[0]
    dividends = dividends.sort_index()
    dividends = dividends.resample('M').ffill()
    dividends = pd.DataFrame(dividends).reset_index()
    dividends['Year'] = dividends['Date'].dt.year
    dividends['Month'] = dividends['Date'].dt.month
    dividends.drop(columns=['Date'], inplace=True)
    dividends = dividends.dropna(subset=['Dividends'])

    return stock_symbol, dividends

def bar_portifolio(db):
    df = data_services.get_current_value(db)
    df["amount"] = df["CurrentValue"] - df["Amount"] 
    df["amount"] = df["amount"].round(2) 
    df["stock"] = df["Instrument"]
    return df[["color", "amount", "stock"]]

def getch_stock_sector(instrument):
    ticker = yf.Ticker(instrument)
    stock_info = ticker.info
    sector = stock_info.get('sector', 'ETF')

    return instrument, sector
