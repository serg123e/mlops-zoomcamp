import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):

    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """

    # List of categorical columns to check
    categorical = ['PULocationID', 'DOLocationID']

    assert output is not None, 'The output is undefined'
    assert all(col in output.columns for col in categorical), 'Categorical cloumns not defined'
    assert 'duration' in output.columns, 'duration cloumn not defined'

    # Check if the columns have the correct data type
    for col in categorical:
        assert output[col].dtype == 'object', f'{col} is not of type str'
