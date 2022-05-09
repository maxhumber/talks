from gazpacho import Soup
from tqdm import tqdm
import time
import random

# step 1: get the html and make it parsable

symbol = "LDCAP"
url = f"https://www.hsx.com/security/view/{symbol}"
soup = Soup.get(url)

# step 2: get the name and current price

name = soup.find("p", {"class": "security_name"}).text.split(" (")[0]
value = float(soup.find("p", {'class': "value"}).text[2:])

# step 3: find movies

lis = soup.find("ul", {"class": "credit"}).find("li")
li = lis[1]
movie_symbol = li.find("span").find("a").attrs["href"].split("/")[-1]

# step 4: get movie price (which is really just step 1 + 2)

url = f"https://www.hsx.com/security/view/{movie_symbol}"
soup = Soup.get(url)

name = soup.find("p", {"class": "security_name"}).text.split(" (")[0]
value = float(soup.find("p", {'class': "value"}).text[2:])

print(name, value)

# step 5: put it in a function

def price(symbol):
    url = f"https://www.hsx.com/security/view/{symbol}"
    soup = Soup.get(url)
    value = float(soup.find("p", {'class': "value"}).text[2:])
    return value

price("KOTFM")

# step 6: back to the list of movies

def extract_symbol(li):
    return li.find("span").find("a").attrs["href"].split("/")[-1]

symbols = [extract_symbol(li) for li in lis][:5]

# step 7: find all the

prices = []
for symbol in tqdm(symbols):
    prices.append(price(symbol))
    time.sleep(random.uniform(1, 10) / 10)

sum(prices) / len(prices)

# step 8: full function

def future(symbol):
    url = f"https://www.hsx.com/security/view/{symbol}"
    soup = Soup.get(url)
    lis = soup.find("ul", {"class": "credit"}).find("li")
    symbols = [extract_symbol(li) for li in lis][:5]
    prices = []
    for symbol in tqdm(symbols):
        prices.append(price(symbol))
        time.sleep(random.uniform(1, 10) / 10)
    return round(sum(prices) / len(prices), 2)

# step 9: ROI

fv = future("LDCAP")
pv = price("LDCAP")

(fv - pv) / pv
