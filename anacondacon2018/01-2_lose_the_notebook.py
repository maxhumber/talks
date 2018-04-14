# coding: utf-8

# In[1]:

import pandas as pd
from sklearn.model_selection import train_test_split

# In[2]:

df = pd.read_csv('max_bike_data.csv')

# In[3]:

for col in df:
    percent_missing = df[df[col].isnull() == True].shape[0] / df.shape[0]
    print(f'percent missing for column {col}: {percent_missing:.3f}')

# In[4]:

df = df[df['drop_off'].notnull()]
