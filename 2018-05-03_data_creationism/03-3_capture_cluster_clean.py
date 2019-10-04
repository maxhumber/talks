import os
import mechanicalsoup
import pandas as pd
import numpy as np
import requests
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler, LabelEncoder
import altair as alt
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# https://developers.google.com/maps/documentation/geocoding/intro

# load environment variables
BIKESHARE_USERNAME = os.environ.get('BIKESHARE_USERNAME')
BIKESHARE_PASSWORD = os.environ.get('BIKESHARE_PASSWORD')
GEOCODING_KEY = os.environ.get('GEOCODING_KEY')

import mechanicalsoup

def fetch_data():
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='MyBot/0.1: mysite.example.com/bot_info',
    )
    browser.open('https://bikesharetoronto.com/members/login')
    browser.select_form('form')
    browser['userName'] = BIKESHARE_USERNAME
    browser['password'] = BIKESHARE_PASSWORD
    browser.submit_selected()
    browser.follow_link('trips')
    browser.select_form('form', nr=2)  # need nr to move down the input rows
    browser['startDate'] = '2017-10-01'
    browser['endDate'] = '2018-04-01'
    browser.submit_selected()
    html = str(browser.get_current_page())
    df = pd.read_html(html)[0]
    return df

df = fetch_data()

# clean data
df = df[~(df['Start Station'] == df['End Station'])]
df['Start Station'] = [l.replace(' - SMART', '') for l in df['Start Station'].values.tolist()]
df['Start Station'] = [l.replace(' Green P', '') for l in df['Start Station'].values.tolist()]
df['End Station'] = [l.replace(' - SMART', '') for l in df['End Station'].values.tolist()]
df['End Station'] = [l.replace(' Green P', '') for l in df['End Station'].values.tolist()]
# df.to_csv('df.csv', index=False)

def get_unique_docks(df=df):
    df = df[~(df['Start Station'] == df['End Station'])]
    df_1 = df[['Start Station', 'End Station']]
    df_2 = df[['Start Station', 'End Station']].rename(columns={'Start Station': 'End Station', 'End Station': 'Start Station'})
    docks = df_1.append(df_2)['Start Station'].unique().tolist()
    return docks

docks = get_unique_docks()
locations = docks

def get_geocode(query):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    payload = {'address': query + 'Toronto', 'key': GEOCODING_KEY}
    r = requests.get(url, params=payload)
    results = r.json()['results'][0]
    return {
        'query': query,
        'place_id': results['place_id'],
        'formatted_address': results['formatted_address'],
        'lat': results['geometry']['location']['lat'],
        'lng': results['geometry']['location']['lng']
    }

get_geocode('joe rockheads')

location_data = pd.DataFrame()
for l in locations:
    try:
        place = get_geocode(l)
        location_data = location_data.append(pd.DataFrame([place]))
    except:
        pass

location_data = location_data.reset_index(drop=True)
