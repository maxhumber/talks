import pandas as pd
import numpy as np
import re


# won't work
with open('data/clippings.txt', 'r') as f:
    contents = f.read()


with open('data/clippings.txt', 'r', encoding='utf-8-sig') as f:
    contents = f.read().replace(u'\ufeff', '')

print(contents)

with open('data/clippings.txt', 'r', encoding='utf-8-sig') as f:
    contents = f.read().replace(u'\ufeff', '')
    lines = contents.rsplit('==========')
    lines[400:405]

with open('data/clippings.txt', 'r', encoding='utf-8-sig') as f:
    contents = f.read().replace(u'\ufeff', '')
    lines = contents.rsplit('==========')
    store = {'author': [], 'title': [], 'quote': []}
    for line in lines:
        try:
            meta, quote = line.split(')\n- ', 1)
            title, author = meta.split(' (', 1)
            _, quote = quote.split('\n\n')
            store['author'].append(author.strip())
            store['title'].append(title.strip())
            store['quote'].append(quote.strip())
        except ValueError:
            pass

df = pd.DataFrame(store)
df.to_csv('data/highlights.csv', index=False, encoding='utf-8-sig')
