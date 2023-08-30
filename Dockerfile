FROM python:3.11.4-alpine

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

WORKDIR /app

COPY . /app/
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "run:app", "--reload" ]
