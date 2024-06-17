#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip freeze | grep scikit-learn')


# In[2]:


get_ipython().system('python -V')


# In[3]:


import pickle
import pandas as pd


# In[4]:


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[5]:


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[6]:


df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')


# In[7]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


# In[8]:


"Q1: %0.3f" % ( y_pred.std() )


# In[9]:


year = 2023
month = 3
df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


# In[10]:


df_result = pd.DataFrame( {'prediction': y_pred, 'ride_id': df['ride_id']} )


# In[11]:


output_file = 'result.pyarrow'
df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)


# In[12]:


# Q2
get_ipython().system('ls -lh result*')


# In[13]:


# Q3
get_ipython().system('jupyter nbconvert --to script starter.ipynb')


# In[ ]:





# In[ ]:




