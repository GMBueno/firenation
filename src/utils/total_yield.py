import boto3  # Already included in lambda

import ijson.backends.python as ijson

from functools import reduce

def get_total_yield_cfv(key: str, bucketName: str, bucketRegion: str, prop: str):
    # Bucket download
    s3 = boto3.resource('s3', region_name=bucketRegion)
    bucket = s3.Bucket(bucketName)
    obj = bucket.Object(key)

    # Download stream
    data = obj.get()
    stream = data['Body']

    # ijson FTW!
    features = ijson.items(stream, 'features.item', use_float=True)

    props = (f['properties'][prop] for f in features if f is not None)
    summ = reduce(lambda x, y:x+y, props)

    return summ