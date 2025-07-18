FROM python:3.12-slim

WORKDIR /app/project

COPY requirements.txt  /app/project/

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*


RUN  pip install --upgrade pip
RUN pip install mysqlclient

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/project/

EXPOSE 8000

