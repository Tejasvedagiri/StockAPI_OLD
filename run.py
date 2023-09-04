from fastapi import FastAPI
from routes.StockRouter import stock_router
from routes.DataRouter import data_router
from routes.UserRouter import user_router
from routes.AuthRouter import auth_router
import logging
from fastapi.middleware.cors import CORSMiddleware

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

app = FastAPI(openapi_url="/api")
app.include_router(auth_router)
app.include_router(stock_router)
app.include_router(data_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your allowed origins
    allow_methods=["*"],  # Allow all HTTP methods (for development, restrict in production)
    allow_headers=["*"],  # Allow all headers (for development, restrict in production)
)

@app.get("/")
async def example_route():
    logger.info("Log message inside route handler")
    return {"message": "Hello, World"}
