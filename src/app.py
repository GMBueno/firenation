from fastapi import FastAPI, HTTPException
from datetime import date

from pandas_datareader import DataReader

from utils.total_yield import get_total_yield_cfv
from utils import files

app = FastAPI()

accepted_codes = {
  "ZCZ20.CBT": {
    "description": "corn future",
    "contractDate": "12/2020"
  },
  "ZCH21.CBT": {
    "description": "corn future",
    "contractDate": "03/2021"
  },
  "ZSK21.CBT": {
    "description": "soybeans future",
    "contractDate": "05/2021"
  },
  "ZSU21.CBT": {
    "description": "soybeans future",
    "contractDate": "09/2021"
  }
}

crop_codes = {
    'corn': ['ZCZ20.CBT', 'ZCH21.CBT'],
    'soybeans': ['ZSK21.CBT', 'ZSU21.CBT']
}

corn_bu = 56 # 1 bushel of corn = 56 pounds
soybeans_bu = 60 # 1 bushel of corn = 60 pounds

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/quote/date/{quote_date}')
def read_futures_by_date(quote_date: date):
    quote = dict()

    for code in accepted_codes:
        try:
            request = DataReader(code, 'yahoo', quote_date)
            quote[code] = request.at[str(quote_date), 'Adj Close']
        except KeyError:
            continue
    
    response = {
        "date": str(quote_date),
        "currency": 'USD'
    }

    for code in quote:
        response[code] = {
            'description': accepted_codes[code]['description'],
            'contractDate': accepted_codes[code]['contractDate'],
            'price': quote[code]
        }
    
    return response


@app.get('/quote/crop/{crop_code}')
def read_futures_by_date(crop_code: str, start_date: date, end_date: date = date.today()):

    if crop_code not in accepted_codes:
        raise HTTPException(status_code=404, detail="Crop code not found")

    try:
        request = DataReader(crop_code, 'yahoo', start_date, end_date)

        response = {
            "code": crop_code,
            'description': accepted_codes[crop_code]['description'],
            'contractDate': accepted_codes[crop_code]['contractDate'],
            'currency': 'USD',
            'price_history': dict()
        }

        for index in request.index:
            response['price_history'][index.date()] = request.at[index, 'Adj Close']
    
        return response
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date range.")
    except KeyError:
        raise HTTPException(status_code=404, detail="No data found in date range.")


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
def read_total_yield(key: str, bucketName: str, bucketRegion: str):
    return {
        'total_yield' : get_total_yield_cfv(key, bucketName, bucketRegion, 'yieldVolume')
        }

@app.get("/{id}")
def get_file(id: str):
    if id == dtn_file['id']:
        return dtn_file
    elif id == sample_file['id']:
        return sample_file

@app.get("/{id}/estimation")
def get_file(id: str):
    if id == files.dtn_file['id']:
        f = files.dtn_file
        key = files.dtn_key
        bucketName = files.dtn_bucket_name
        bucketRegion = files.dtn_region
    elif id == files.sample_file['id']:
        f = files.sample_file
        key = files.sample_key
        bucketName = files.sample_bucket_name
        bucketRegion = files.sample_region
    else:
        raise HTTPException(status_code=404, detail="File not found")


    total_yield = get_total_yield_cfv(key, bucketName, bucketRegion, 'yieldVolume')
    crop = f['summary']['properties']['crop'][0]
    endDate = f['operationEndTime'][0:10]

    estimation = dict()
    quotes = total_yield / 5000
    for c in crop_codes[crop]:
        estimation[c] = {
            'size': 5000,
            'quotes': quotes,
            c: accepted_codes[c]
        }

    return {
        "id": f['id'],
        "total_production": {
            'total_yield' : total_yield,
            'unit': 'bu'
        },
        'crop': crop,
        "harvestEnd": endDate,
        "currency": "USD",
        'estimation' : estimation
    }
