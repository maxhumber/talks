import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from gazpacho import Soup
from tqdm import tqdm
import numpy as np
import pandas as pd

options = Options()
options.headless = True
browser = Firefox(executable_path="/usr/local/bin/geckodriver", options=options)

links = []
pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 101, 102, 200, 201, 202, 300, 301, 302]
for page in tqdm(pages):
    url = f"https://boardgamegeek.com/browse/boardgame/page/{page}"
    browser.get(url)
    soup = Soup(browser.page_source)
    li = [a.attrs["href"] for a in soup.find("a", {"class": "primary", "href": "boardgame"})]
    links.extend(li)
    time.sleep(1)

def parse(soup):
    name = soup.find("a", {"ui-sref": "geekitem.overview"}, mode="list")[1].text
    rating = soup.find("span", {"ng-show": "showRating"}, mode="first").text
    time = soup.find("div", {"class": "gameplay-item-primary"})[1].text
    age = soup.find("div", {"class": "gameplay-item-primary"})[2].find("span").text
    complexity = soup.find("span", {"class": "ng-binding gameplay-weight"}).text
    category = soup.find("a", {"href": "boardgamesubdomain"}, mode="first").text
    return [name, rating, time, age, complexity, category]

def scrape(link):
    id = link.split("/")[2]
    url = f"https://boardgamegeek.com" + link
    browser.get(url)
    html = browser.page_source
    with open(f"html/{id}.html", "w") as f:
        f.write(html)
    soup = Soup(html)
    return soup

data = []
for link in tqdm(links):
    try:
        soup = scrape(link)
        di = parse(soup)
        data.append(di)
    except:
        pass
    time.sleep(np.random.uniform(0, 1))

df = pd.DataFrame(data, columns=["name", "rating", "time", "age", "complexity", "category"])
df["time"] = df["time"].apply(pd.to_numeric, errors="coerce")
df["age"] = df["age"].apply(lambda x: pd.to_numeric(x.replace("+", ""), errors="coerce"))
df = pd.concat([df, pd.get_dummies(df["category"])], axis=1)
df.columns = [c.replace("'", "").lower() for c in df.columns]
df = df.dropna()
df = df.drop("category", axis=1)
df = df.reset_index(drop=True)
df.to_csv("data/games.csv", index=False)
