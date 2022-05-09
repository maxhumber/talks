import os
import sqlite3

from dotenv import find_dotenv, load_dotenv # pip install python-dotenv
from gazpacho import Soup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from slack import WebClient # pip install slackclient
from slack.errors import SlackApiError
import pandas as pd

load_dotenv(find_dotenv())
options = Options()
options.headless = True

slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

browser = Firefox(executable_path="/usr/local/bin/geckodriver", options=options)
con = sqlite3.connect("games.db")
cur = con.cursor()

def make_soup():
    url = 'https://www.amazon.ca/hz/wishlist/ls/17CRUYWGYZ5Y2'
    browser.get(url)
    html = browser.page_source
    soup = Soup(html)
    return soup

def parse_item(item):
    title = item.find('a', {'id': 'itemName'}, strict=False).attrs['title']
    price = float(item.find('span', {'class': 'a-offscreen'}).text.split('\xa0')[-1])
    return (title, price)

def get_games(soup):
    items = soup.find('ul', {'id': 'g-items'}).find('li')
    games = pd.DataFrame(
        [parse_item(item) for item in items],
        columns=['title', 'price']
    )
    games['date'] = pd.Timestamp('now')
    return games

if __name__ == '__main__':
    soup = make_soup()
    games = get_games(soup)
    games.to_sql('games', con, if_exists='append', index=False)
    average = pd.read_sql("select title, avg(price) as average from games group by title", con)
    df = pd.merge(games[['title', 'price']], average)
    string = f"```\n{df.to_markdown(index=False, tablefmt='grid')}\n```"
    client.chat_postMessage(
        channel="bots",
        text=string,
        username='GameBot',
        icon_emoji=':joystick:'
    )
