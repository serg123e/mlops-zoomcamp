import batch
from datetime import datetime
import pandas as pd


input_file = batch.get_input_path(2023, 1)
print("saving df to input_file: "+input_file)

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

S3_ENDPOINT_URL = "http://localhost:4566"

options = {
    'client_kwargs': {
        'endpoint_url': S3_ENDPOINT_URL
    }
}

data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']

df_input = pd.DataFrame(data, columns=columns)

df_input.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)
