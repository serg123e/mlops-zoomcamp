#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import click

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

@click.command()
@click.option('--year', default=2023, prompt='Year', help='Year.')
@click.option('--month', prompt='Month number', help='Month.')
def train(year,month):
   
    filename = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{int(month):02d}.parquet"
    print(f"Reading {filename}")
    df = read_data(filename)

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    mean = y_pred.mean()
    print(f"mean predicted duration for {year}-{month}: {mean}")

    # df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    
    # df_result = pd.DataFrame( {'prediction': y_pred, 'ride_id': df['ride_id']} )

    # output_file = f"result{year}-{month}.pyarrow"
    #df_result.to_parquet(
    #    output_file,
    #    engine='pyarrow',
    #    compression=None,
    #    index=False
    #)

    # Q2
    # get_ipython().system('ls -lh result*')

if __name__ == '__main__':
    train()