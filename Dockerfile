FROM python:3.13.5-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl apt-transport-https gnupg gcc g++ make python3-dev unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY . .

RUN rm .env

EXPOSE 8080

CMD uvicorn main:app --host 0.0.0.0 --port 8080
