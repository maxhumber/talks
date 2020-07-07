from gazpacho import get, Soup
import json

html = get('http://quotes.toscrape.com/')
soup = Soup(html)
quotes = soup.find('div', {'class': 'quote'})

def parse(quote):
    return {
        'author': quote.find('small').text,
        'text': quote.find('span', {'class': 'text'}).text
    }

quotes = [parse(quote) for quote in quotes]

with open('quotes.json', 'w') as f:
    json.dump(quotes, f)
