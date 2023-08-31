from fastapi import FastAPI
from routes.stock_chart import stock_chart
from routes.data_loader import data_loader

app = FastAPI()
app.include_router(stock_chart)
app.include_router(data_loader)

