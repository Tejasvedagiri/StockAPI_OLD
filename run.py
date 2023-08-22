from fastapi import FastAPI
from routes.stock_chart import stock_chart
from routes.data_loader import data_loader

app = FastAPI()
app.include_router(stock_chart)
app.include_router(data_loader)


# df = pd.read_csv("temp.csv")
# dividens = df[df["Trans Code"] == "CDIV"]
# dividens[["Process Date", "Instrument", "Amount"]] 

# rename_cols = {
#     'Activity Date': "ActivityDate",
#     'Process Date': "ProcessDate",
#     'Settle Date': "SettleDate",
#     'Instrument': "Instrument",
#     'Description': "Description",
#     'Trans Code': "TransactionCode",
#     'Quantity': "Quantity",
#     'Price': "Price",
#     'Amount': "Amount"
# }
# df.to_sql('transaction', cnx, index=False)
