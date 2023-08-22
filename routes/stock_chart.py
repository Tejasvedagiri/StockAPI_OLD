from fastapi import APIRouter
from services import stock_service
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_database_engine
from fastapi import Response
from fastapi.responses import JSONResponse


stock_chart = APIRouter(prefix="/charts")

@stock_chart.get("/get_dividens/", tags=["charts"], )
async def get_dividens_bar_grap_data(db: Session = Depends(get_database_engine)):
    df = stock_service.get_dividens_bar_grap_data(db)
    return Response(df.to_json(orient="records"), media_type="application/json")

@stock_chart.get("/get_price_chart/", tags=["charts"], )
async def get_price_chart(db: Session = Depends(get_database_engine)):
    data = stock_service.price_chart(db)
    return JSONResponse(content=data)
