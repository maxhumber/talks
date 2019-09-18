import string
import time
import json
import re
import glob
from string import digits
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_player_links_from_letter(letter='a'):
    url = f'https://www.hockey-reference.com/players/{letter}/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    links = soup.find_all('strong')
    links = [a.find('a')['href'] for a in links if a.find('a') is not None]
    return links

def get_player_links():
    links = []
    for letter in string.ascii_lowercase:
        links_from_letter = get_player_links_from_letter(letter)
        links.extend(links_from_letter)
        time.sleep(0.5 + np.random.poisson(1))
    return links

with open('data/links.json', 'w') as f:
    f.write(json.dumps(links))

with open('data/links.json', 'r') as f:
    links = json.loads(f.read())

def save_player_html(link):
    file_name = re.findall('(?<=\/[a-z]\/).+?$', link)[0]
    url = f'https://www.hockey-reference.com/{link}'
    r = requests.get(url)
    with open(f'html/{file_name}', 'w') as f:
        f.write(r.text)

def save_all_html():
    for link in tqdm(links):
        save_player_html(link)
        time.sleep(3)

def parse_meta_container(soup):
    meta = ''.join([s.text for s in soup.select('#meta p')]).replace('\xa0', '')
    position = re.findall('(?<=\:\s).+?(?=\•|\n)', meta)[0]
    entry = int(re.findall('(?<=\)\,\s).+?(?=NHL)', meta)[0])
    draft = re.findall('(?<=round).+?(?=overall)', meta)[0]
    selected_in_draft = int(''.join(c for c in draft if c in digits))
    return position, entry, selected_in_draft

def extract_player_stats(soup):
    meta = parse_meta_container(soup)
    table = soup.find_all(class_='overthrow table_container')[0]
    df = pd.read_html(str(table))[0]
    df.columns = ['_'.join(col) for col in df.columns]
    df['name'] = soup.find('h1').text
    df['position'] = meta[0]
    df['entry'] = meta[1]
    df['selected_in_draft'] = meta[2]
    return df

def html_to_df(file_path):
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f.read())
    df = extract_player_stats(soup)
    df['id'] = re.findall('(?<=^).+?(?=\.html)', file_path)[0]
    return df

def parse_all_html_pages():
    htmls = glob.glob('html/*.html')
    skaters = pd.DataFrame()
    goalies = pd.DataFrame()
    for html in tqdm(htmls):
        try:
            df = html_to_df(html)
            if df['position'].unique()[0] == 'G':
                goalies = goalies.append(df, sort=False)
            else:
                skaters = skaters.append(df, sort=False)
        except:  # yolo
            pass
    return skaters, goalies

skaters, goalies = parse_all_html_pages()

columns = {
    'Unnamed: 0_level_0_Season': 'season',
    'Unnamed: 1_level_0_Age': 'age',
    'Scoring_Tm': 'team',
    'Unnamed: 4_level_0_GP': 'games_played',
    'Goals_G': 'goals',
    'Assists_A': 'assists',
    'Shots_PTS': 'points',
    'Ice Time_+/-': 'plus_minus',
    'Unnamed: 9_level_0_PIM': 'penalty_minutes',
    'Unnamed: 10_level_0_EV': 'goals_even_strength',
    'Unnamed: 11_level_0_PP': 'goals_power_play',
    'Unnamed: 12_level_0_SH': 'goals_short_handed',
    'Unnamed: 13_level_0_GW': 'goals_game_winning',
    'Unnamed: 14_level_0_EV': 'assists_even_strength',
    'Unnamed: 15_level_0_PP': 'assists_power_play',
    'Unnamed: 16_level_0_SH': 'assists_short_handed',
    'Unnamed: 17_level_0_S': 'shots_on_goal',
    'Unnamed: 18_level_0_S%': 'shooting_percentage',
    'Unnamed: 19_level_0_TSA': 'shots_attempted_total',
    'Unnamed: 20_level_0_TOI': 'time_on_ice_total',
    'Unnamed: 21_level_0_ATOI': 'time_on_ice_average',
    'Unnamed: 22_level_0_FOW': 'face_off_wins',
    'Unnamed: 23_level_0_FOL': 'face_off_losses',
    'Unnamed: 24_level_0_FO%': 'face_off_win_percentage',
    'Unnamed: 25_level_0_BLK': 'blocks',
    'Unnamed: 26_level_0_HIT': 'hits',
    'Unnamed: 27_level_0_TK': 'take_aways',
    'Unnamed: 28_level_0_GV': 'give_aways',
    'Unnamed: 29_level_0_Awards': 'awards',
}

skaters = skaters.rename(columns=columns)
skaters = skaters[
    ['id', 'name', 'position', 'entry', 'selected_in_draft'] +
    list(columns.values())
]
skaters = skaters.dropna(subset=['age'])
skaters = skaters[skaters.groupby(['id', 'age']).cumcount() + 1 == 1]
skaters.loc[skaters.team == 'TOT', 'team'] = 'Multiple'
skaters.to_csv('data/skaters.csv', index=False)
