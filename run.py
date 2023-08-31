from fastapi import FastAPI, Request
from routes.stock_chart import stock_chart
from routes.data_loader import data_loader
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI()
app.include_router(stock_chart)
app.include_router(data_loader)

@app.get("/docs", include_in_schema=False)
async def get_documentation(request: Request):
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    print(openapi_url)
    return get_swagger_ui_html(openapi_url=openapi_url, title="Swagger")
