from fastapi import APIRouter
from services import stock_service, data_services
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_database_engine
from fastapi import Response
from fastapi.responses import JSONResponse


stock_chart = APIRouter(prefix="/charts")

@stock_chart.get("/get_stock_dividends_charts/", tags=["charts"], )
async def get_stock_dividends_charts(db: Session = Depends(get_database_engine)):
    data = stock_service.get_dividens_bar_grap_data(db)
    return JSONResponse(content=data)

@stock_chart.get("/get_price_chart/", tags=["charts"], )
async def get_price_chart(db: Session = Depends(get_database_engine)):
    data = stock_service.price_chart(db)
    return JSONResponse(content=data)


@stock_chart.get("/get_current_dividends_chart/", tags=["charts"], )
async def get_current_dividends_chart(db: Session = Depends(get_database_engine)):
    data = stock_service.current_dividends(db)
    return JSONResponse(content=data)

@stock_chart.get("/get_monthly_dividends_chart/", tags=["charts"], )
async def get_monthly_dividends_chart(db: Session = Depends(get_database_engine)):
    data = stock_service.montly_dividens(db)
    return JSONResponse(content=data)

@stock_chart.get("/get_bar_portifolio/", tags=["charts"], )
async def get_bar_portifolio(db: Session = Depends(get_database_engine)):
    data = stock_service.bar_portifolio(db)
    return Response(data.to_json(orient="records"), media_type="application/json")

@stock_chart.get("/get_amount_to_buy/", tags=["charts"], )
async def get_amount_to_buy(db: Session = Depends(get_database_engine)):
    data = data_services.amount_to_buy(db)
    return Response(data.to_json(orient="records"), media_type="application/json")

