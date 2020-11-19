from fastapi import FastAPI
from datetime import date

from utils.total_yield import get_total_yield_cfv

app = FastAPI()

accepted_crops = {
    'corn': 'ZCZ20.CBT',
    'corn': 'ZCZ20.CBT',
    'corn': 'ZCZ20.CBT',
    'corn': 'ZCZ20.CBT'
}

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('')


@app.get("/finance/{crop_type}/futures")
def read_futures_date(crop_type: str, price_date: date):
    return {
        "crop_type": crop_type, \
        "date": price_date.strftime("%x")
    }

@app.get("/finance/{crop_type}/futures/range")
def read_futures_date_range(crop_type: str, start_date: date, end_date: date):
    return {
        "crop_type": crop_type, 
        "start_date": start_date.strftime("%x"),
        "end_date": end_date.strftime("%x")
    }


@app.get("/finance/{crop_type}/prices")
def read_price_date_range(crop_type: str, price_date: date):
    return {
        "crop_type": crop_type, 
        "date": price_date.strftime("%x")
    }


@app.get("/finance/{crop_type}/prices/range")
def read_price_date_range(crop_type: str, start_date: date, end_date: date):
    return {
        "crop_type": crop_type, 
        "start_date": start_date.strftime("%x"),
        "end_date": end_date.strftime("%x")
    }


@app.get("/totalyield/")
def read_total_yield(key: str, bucketName: str, bucketRegion: str, prop: str):
    return {
        'total_yield' : get_total_yield_cfv(key, bucketName, bucketRegion, prop)
        }