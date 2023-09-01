import pandas as pd
from constants import rename_cols, TABLE_NAME
import math
import yfinance as yf
import concurrent.futures
import numpy as np
from datetime import datetime    
from utils import generate_color
from constants import stock_weightage, total_invested_value
from sqlalchemy import inspect
import tempfile


def upload_csv(file, db):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())

    df = pd.read_csv(temp_file.name)
    df = df.rename(columns=rename_cols)
    df['Price'] = df['Price'].str.replace(r'[^0-9.]', '', regex=True)
    records = df.to_sql("transaction", db, index=False)
    return records

    

def load_data(db, delete_flag):
    df = pd.read_csv("temp.csv")
    df = df.rename(columns=rename_cols)
    df['Price'] = df['Price'].str.replace(r'[^0-9.]', '', regex=True)
    if delete_flag:
        inspector = inspect(db)
        table_names = inspector.get_table_names()
        with db.connect() as connection:
            for table_name in table_names:
                connection.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
    records = df.to_sql("transaction", db, index=False)
    return records

def invested_amount(db):
    query = f"SELECT ProcessDate, Instrument, Description, TransactionCode, Quantity, CAST(Price as DECIMAL(32,32)) as Price, Amount FROM {TABLE_NAME} where TransactionCode = 'Buy' or TransactionCode = 'Sell' "
    
    df = pd.read_sql(query, db)
    main_df = df.groupby('Instrument').agg({'Quantity': 'sum', 'Amount': 'sum'}).reset_index()
    main_df = main_df[main_df["Amount"] < -1 ]
    main_df['Amount'] = main_df['Amount'].abs()
    invested_amount = main_df["Amount"].sum().round(2)
    difference = ((2600 - invested_amount) / invested_amount * 100).round(2)

    return_dict = {
        "title": invested_amount,
        "subtitle": "Reaming Value",
        "progress" : str(1 - difference / 100),
        "flag" : True,
        "increase" : (2600 - invested_amount).round(2)
    }

    return return_dict

def dividend_amount(db):
    query = f"SELECT sum(Amount) as Amount FROM {TABLE_NAME} where TransactionCode = 'CDIV'"

    df = pd.read_sql(query, db)
    content = {
      "title": df["Amount"][0],
      "subtitle": "Total Dividends",
      "flag": True,
      "increase": "",
    }
    return content

def current_month_dividend_amount(db):
    query = f"SELECT * FROM {TABLE_NAME} where TransactionCode = 'CDIV'"
    
    df = pd.read_sql(query, db)
    df['ProcessDate'] = pd.to_datetime(df['ProcessDate'])
    current_month = pd.Timestamp.now().month
    mask = df['ProcessDate'].dt.month == current_month
    cur_month = df[mask]

    df['ProcessDate'] = pd.to_datetime(df['ProcessDate'])
    current_date = pd.Timestamp.now()
    first_day_of_current_month = current_date.replace(day=1)
    first_day_of_previous_month = first_day_of_current_month - pd.DateOffset(months=1)
    last_day_of_previous_month = first_day_of_current_month - pd.DateOffset(days=1)
    mask = (df['ProcessDate'] >= first_day_of_previous_month) & (df['ProcessDate'] <= last_day_of_previous_month)
    pre_month = df[mask]
    currentMonthValue = cur_month["Amount"].sum()
    previousMonthValue = pre_month["Amount"].sum()
    difference = ((currentMonthValue - previousMonthValue) / previousMonthValue * 100).round(2)

    data_dict = {
      "title": currentMonthValue.round(2),
      "subtitle": "Month Dividends",
      "flag": True if difference > 0 else False,
      "increase": f"{ '+%' if difference > 0 else '-%'}{difference}",
    }
    

    return data_dict
def get_current_value(db):
    query = f"SELECT ProcessDate, Instrument, Description, TransactionCode, Quantity, CAST(Price as DECIMAL(32,32)) as Price, Amount FROM {TABLE_NAME} where TransactionCode = 'Buy' or TransactionCode = 'Sell' "

    df = pd.read_sql(query, db)
    main_df = df.groupby('Instrument').agg({'Quantity': 'sum', 'Amount': 'sum'}).reset_index()
    main_df = main_df[main_df["Amount"] < -1 ]
    main_df['Amount'] = main_df['Amount'].abs()
    instruments = main_df["Instrument"].to_list()
    color = generate_color("tab20b", len(instruments))
    current_price_dict = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_values, item) for item in instruments]
        results = [future.result() for future in futures]
        current_price_dict = {key: value for dictionary in results for key, value in dictionary.items()}

    
    main_df['CurrentPrice'] = main_df['Instrument'].map(current_price_dict)
    main_df['CurrentValue'] = main_df['CurrentPrice'] * main_df["Quantity"]
    main_df["color"] = color

    return main_df

def current_value(db):
    
    main_df = get_current_value(db)
    current_value = main_df['CurrentValue'].sum().round(2)
    invested_amount = main_df["Amount"].sum().round(2)
    difference = ((current_value - invested_amount) / invested_amount * 100).round(2)
    flag = True if difference > 0 else False

    return_dict = {
        "title": current_value,
        "subtitle": "Current Value",
        "difference": difference,
        "increase": f"{'+%' if flag else '-%'}{difference}",
        "flag" : flag,
        "progress": 1 - difference / 100
    }

    return return_dict 

def process_values(instrument):
    tickers = yf.Tickers(instrument)
    ticker = tickers.tickers[instrument]
    if "currentPrice" in ticker.info:
        return {instrument : ticker.info["currentPrice"]}
    elif ticker.info["ask"] != 0:
        return {instrument : ticker.info["ask"]}
    else:
        return {instrument : ticker.info["navPrice"]}

def tansactions(db):
    query = f"SELECT rowid as txId, Instrument as instrument, ProcessDate as date, Amount as amt, Quantity as quantity  FROM {TABLE_NAME} where TransactionCode = 'Buy' or TransactionCode = 'Sell'"

    df = pd.read_sql(query, db)
    return df

def calender_events(db):
    query = f"SELECT Distinct Instrument as Instrument FROM {TABLE_NAME} where TransactionCode = 'CDIV' and Instrument not in (Select Instrument from {TABLE_NAME} where TransactionCode = 'Sell')"

    df = pd.read_sql(query, db)
    instruments = df["Instrument"].to_list()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(getexDividendDate, item) for item in instruments]
        results = [future.result() for future in futures]
    
    return results


def getexDividendDate(instrument):
    content = yf.Ticker(instrument).info
    if 'exDividendDate' in content:
        date = datetime.fromtimestamp(content['exDividendDate'])
        data = {
            "id" : instrument,
            "title" : f"{instrument} Ex-Dividend-Date",
            "date" : date.strftime("%Y-%m-%d")
        }
        return data
    else:
        return {}
    
def amount_to_buy(db):
    df = get_current_value(db)
    df["CurrentValue"] = df["CurrentValue"].round(2)
    df["Weightage"] = df["Instrument"].map(stock_weightage)
    df["PlannedAmountToInvest"] = df["Weightage"] * total_invested_value / 100
    df["AmountToInvest"] = df["PlannedAmountToInvest"] - df["CurrentValue"]

    df["stock"] = df["Instrument"]
    df["amount"] = df["AmountToInvest"]

    return df[["stock", "amount", "color"]]