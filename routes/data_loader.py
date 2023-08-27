from fastapi import APIRouter, Query
from services import data_services
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_database_engine
from fastapi import Response
from fastapi.responses import JSONResponse

data_loader = APIRouter(prefix="/dataloader")

@data_loader.get("/load_base_csv/", tags=["data"])
async def load_base_csv(flag: bool = Query(default=True, description="Reset db contents"), 
                        db: Session = Depends(get_database_engine)):
    records = data_services.load_data(db, flag)
    return Response(f"Succefully inserted ==> {records}", media_type="application/text")

@data_loader.get("/current_value", tags=["data"])
async def current_value(db: Session = Depends(get_database_engine)):
    data = data_services.current_value(db)
    return JSONResponse(content=data)

@data_loader.get("/get_invested_amount", tags=["data"])
async def get_invested_amount(db: Session = Depends(get_database_engine)):
    
    data = data_services.invested_amount(db)
    return JSONResponse(content=data)

@data_loader.get("/get_dividend_amount", tags=["data"])
async def get_dividend_amount(db: Session = Depends(get_database_engine)):
    
    data = data_services.dividend_amount(db)
    return JSONResponse(content=data)

@data_loader.get("/get_current_month_dividend_amount", tags=["data"])
async def get_current_month_dividend_amount(db: Session = Depends(get_database_engine)):
    
    data = data_services.current_month_dividend_amount(db)
    return JSONResponse(content=data)

@data_loader.get("/get_transactions", tags=["data"])
async def get_transactions(db: Session = Depends(get_database_engine)):
    
    data = data_services.tansactions(db)
    return Response(data.to_json(orient="records"), media_type="application/json")

@data_loader.get("/get_calender_events", tags=["data"])
async def get_calender_events(db: Session = Depends(get_database_engine)):
    data = data_services.calender_events(db)
    return JSONResponse(content=data)
   

