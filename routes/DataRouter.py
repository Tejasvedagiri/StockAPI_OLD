from fastapi import APIRouter, UploadFile, Response
from fastapi.responses import JSONResponse
from services import DataServices
from fastapi import APIRouter, Depends
from dependecies.DataDependencies import DataDependencies
from services.AuthServices import get_current_active_user

data_router = APIRouter(prefix="/dataloader")

@data_router.post("/upload_csv", tags=["data"])
async def upload_file(file: UploadFile, deps: DataDependencies = Depends(get_current_active_user)):
    if not file.filename.endswith(".csv"):
        return JSONResponse(content={"error": "Only CSV files are allowed."}, status_code=400)
    try:
        count = DataServices.upload_csv(file, deps)
        return JSONResponse(content=f"Read file count ==> {count}")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@data_router.get("/current_value", tags=["data"])
async def current_value(deps: DataDependencies = Depends()):
    data = DataServices.current_value(deps)
    return JSONResponse(content=data)

@data_router.get("/get_invested_amount", tags=["data"])
async def get_invested_amount(deps: DataDependencies = Depends()):
    data = DataServices.invested_amount(deps)
    return JSONResponse(content=data)

@data_router.get("/get_dividend_amount", tags=["data"])
async def get_dividend_amount(deps: DataDependencies = Depends()):
    data = DataServices.dividend_amount(deps)
    return JSONResponse(content=data)

@data_router.get("/get_current_month_dividend_amount", tags=["data"])
async def get_current_month_dividend_amount(deps: DataDependencies = Depends()):
    data = DataServices.current_month_dividend_amount(deps)
    return JSONResponse(content=data)

@data_router.get("/get_transactions", tags=["data"])
async def get_transactions(deps: DataDependencies = Depends()):
    data = DataServices.tansactions(deps)
    return Response(data.to_json(orient="records"), media_type="application/json")

@data_router.get("/get_calender_events", tags=["data"])
async def get_calender_events(deps: DataDependencies = Depends()):
    data = DataServices.calender_events(deps)
    return JSONResponse(content=data)
   

