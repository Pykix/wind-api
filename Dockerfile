FROM python:3.10

ENV PYTHONUNBUFERED 1

WORKDIR /app
RUN pip install -U pip
RUN apt update && apt install -y binutils libproj-dev gdal-bin libgeos-dev libgdal-dev python3-gdal gcc postgis

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

