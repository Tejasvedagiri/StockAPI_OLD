from fastapi import APIRouter, Depends
from services import StockServices, DataServices
from fastapi import Response
from fastapi.responses import JSONResponse
import logging
from dependecies.DataDependencies import DataDependencies
logger = logging.getLogger(__name__) 

stock_router = APIRouter(prefix="/charts")

@stock_router.get("/get_stock_dividends_charts/", tags=["charts"])
async def get_stock_dividends_charts(deps: DataDependencies = Depends()):
    data = StockServices.get_dividens_bar_grap_data(deps)
    return JSONResponse(content=data)

@stock_router.get("/get_price_chart/", tags=["charts"], )
async def get_price_chart(deps: DataDependencies = Depends()):
    data = StockServices.price_chart(deps)
    return JSONResponse(content=data)


@stock_router.get("/get_current_dividends_chart/", tags=["charts"], )
async def get_current_dividends_chart(deps: DataDependencies = Depends()):
    data = StockServices.current_dividends(deps)
    return JSONResponse(content=data)

@stock_router.get("/get_monthly_dividends_chart/", tags=["charts"], )
async def get_monthly_dividends_chart(deps: DataDependencies = Depends()):
    data = StockServices.montly_dividens(deps)
    return JSONResponse(content=data)

@stock_router.get("/get_bar_portifolio/", tags=["charts"], )
async def get_bar_portifolio(deps: DataDependencies = Depends()):
    data = StockServices.bar_portifolio(deps)
    return Response(data.to_json(orient="records"), media_type="application/json")

@stock_router.get("/get_amount_to_buy/", tags=["charts"], )
async def get_amount_to_buy(deps: DataDependencies = Depends()):
    data = DataServices.amount_to_buy(deps)
    return Response(data.to_json(orient="records"), media_type="application/json")

@stock_router.get("/get_stock_sector/", tags=["charts"], )
async def get_stock_sector(deps: DataDependencies = Depends()):
    data = StockServices.get_stock_sector(deps)
    return JSONResponse(content=data)



