import time
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def scrape_season(year_end):
    # https://www.hockey-reference.com/leagues/NHL_2019_games.html
    url = f'https://www.hockey-reference.com/leagues/NHL_{year_end}_games.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='lxml')
    table = soup.find_all(class_='overthrow table_container', id='div_games')[0]
    df = pd.read_html(str(table))[0]
    df['season'] = f'{int(year_end-1)}-{str(year_end)[-2:]}'
    return df

def scrape(start=2018, end=2019):
    seasons = pd.DataFrame()
    for year in tqdm(range(start, end+1)):
        df = scrape_season(year)
        seasons = seasons.append(df)
        time.sleep(3)
    return seasons

raw = scrape(start=2018, end=2019)
df = raw.copy()

def clean(df):
    df.columns = [column.lower() for column in df.columns]
    df = df.dropna(subset=['g'])
    df = df.rename(columns={'g': 'away_goals', 'g.1': 'home_goals', 'visitor': 'away'})
    df = df[['season', 'date', 'home', 'away', 'home_goals', 'away_goals']]
    return df

df = clean(raw)
df.to_csv('data/games.csv', index=False)
