from fastapi import FastAPI, Request
from routes.stock_chart import stock_chart
from routes.data_loader import data_loader
from fastapi.openapi.docs import get_swagger_ui_html
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a logger instance
logger = logging.getLogger(__name__)

# Create a handler for writing log messages to a file
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)  # Set the log level for the file handler
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

# Check if handlers already exist before adding them
if not logger.handlers:
    logger.addHandler(file_handler)

app = FastAPI(openapi_prefix="/api")

app.include_router(stock_chart)
app.include_router(data_loader)

@app.get("/")
async def example_route():
    logger.info("Log message inside route handler")
    return {"message": "Hello, World"}
