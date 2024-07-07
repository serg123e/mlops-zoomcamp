import batch
from datetime import datetime
import pandas as pd
from pytest import approx
import os
import s3fs

S3_ENDPOINT_URL = "http://localhost:4566"
INPUT_FILE = batch.get_input_path(2023, 1)
OUTPUT_FILE = batch.get_output_path(2023, 1)

def init_envs():
    os.environ["INPUT_FILE_PATTERN"]="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
    os.environ["OUTPUT_FILE_PATTERN"]="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
    os.environ["S3_ENDPOINT_URL"] = S3_ENDPOINT_URL

def prepare_input_file():

    print("saving df to input_file: "+INPUT_FILE)

    def dt(hour, minute, second=0):
        return datetime(2023, 1, 1, hour, minute, second)



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
        INPUT_FILE,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )

def run_batch():
    os.system("python batch.py 2023 01")

def check_result():
    df_result = batch.read_data(OUTPUT_FILE)
    assert df_result['predicted_duration'].sum() == approx(36.28, rel=0.1) 

def cleanup():
    s3 = s3fs.S3FileSystem(
      anon=False,
      endpoint_url=S3_ENDPOINT_URL
    )

    s3.rm(INPUT_FILE)
    s3.rm(OUTPUT_FILE)


if __name__ == '__main__':
    init_envs()
    prepare_input_file()
    run_batch()
    check_result()
    cleanup()
