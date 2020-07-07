from gazpacho import get, Soup
import pandas as pd
from tqdm import tqdm

url = 'https://www.goodreads.com/review/list/16626766-max'

def parse_tr(tr):
    return {
        'title': tr.find('a', {'href': '/book/show/'})[1].attrs['title'],
        'pages': tr.find('td', {'class': 'field num_pages'}).find('nobr').text,
        'read': tr.find('span', {'class': 'date_read_value'}).text,
    }

def scrape_page(user=16626766, shelf='textbook', page=1):
    url = f'https://www.goodreads.com/review/list/{user}'
    params = {
        'shelf': shelf,
        'order': 'd',
        'sort': 'date_read',
        'page': page
    }
    html = get(url, params)
    soup = Soup(html)
    trs = soup.find('tr', {'class': 'bookalike review'})
    books = [parse_tr(tr) for tr in trs]
    return books

books = []
for page in tqdm([1, 2]):
    books.extend(scrape_page(page=page))

pd.DataFrame(books).to_csv('data/textbooks.csv', index=False)
