import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

# quotes for audiobooks:

books = [
    'Fluke: Or, I Know Why the Winged Whale Sings',
    'Shades of Grey Fforde',
    'Neverwhere Gaiman',
    'The Graveyard Book'
]

import requests
from bs4 import BeautifulSoup
import re

book = 'Fluke: Or, I Know Why the Winged Whale Sings'

payload = {'q': book, 'commit': 'Search'}
r = requests.get('https://www.goodreads.com/quotes/search', params=payload)
soup = BeautifulSoup(r.text, 'html.parser')

for s in soup(['script']):
    s.decompose()

s = soup.find_all(class_='quoteText')[5]

s = s.text.replace('\n', '').strip()
quote = re.search('“(.*)”', s, re.IGNORECASE).group(1)
meta = re.search('”(.*)', s, re.IGNORECASE).group(1)
meta = re.sub('[^,.a-zA-Z\s]', '', meta)
meta = re.sub('\s+', ' ', meta).strip()
meta = re.sub('^\s', '', meta).strip()

def get_quotes(book):
    payload = {'q': book, 'commit': 'Search'}
    r = requests.get('https://www.goodreads.com/quotes/search', params=payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    # remove scripts
    for s in soup(['script']):
        s.decompose()
    # parse text
    book = {'quote': [], 'author': [], 'title': []}
    for s in soup.find_all(class_='quoteText'):
        s = s.text.replace('\n', '').strip()
        quote = re.search('“(.*)”', s, re.IGNORECASE).group(1)
        meta = re.search('”(.*)', s, re.IGNORECASE).group(1)
        meta = re.sub('[^,.a-zA-Z\s]', '', meta)
        meta = re.sub('\s+', ' ', meta).strip()
        meta = re.sub('^\s', '', meta).strip()
        try:
            author, title = meta.split(',')
        except ValueError:
            author, title = meta, None
        book['quote'].append(quote)
        book['author'].append(author)
        book['title'].append(title)
    return book

books = [
    'Fluke: Or, I Know Why the Winged Whale Sings',
    'Shades of Grey Fforde',
    'Neverwhere Gaiman',
    'The Graveyard Book'
]

all_books = {'quote': [], 'author': [], 'title': []}
for b in books:
    print(f"Getting: {b}")
    b = get_quotes(b)
    all_books['author'].extend(b['author'])
    all_books['title'].extend(b['title'])
    all_books['quote'].extend(b['quote'])

audio = pd.DataFrame(all_books)
audio.to_csv('audio.csv', index=False, encoding='utf-8-sig')
