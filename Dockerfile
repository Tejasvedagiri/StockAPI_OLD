# Use an official Python runtime as a parent image
FROM python:3.11.4-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/mysql -lmysqlclient"

# Copy your FastAPI application code into the container
WORKDIR /app
COPY . /app


# Install FastAPI dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the port your FastAPI app will run on
EXPOSE 8000

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
