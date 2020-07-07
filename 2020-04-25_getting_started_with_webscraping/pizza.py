#################################
##                             ##
##       P R E A M B L E       ##
##                             ##
#################################

from IPython.display import Image, IFrame, HTML
HTML('<h3>"Another Web Scraping Talk..."</h3>')
Image('images/01.png', width=500)
Image('images/02.png', width=1e3)
Image('images/03.png', width=900)
Image('images/04.png', width=800)
Image('images/05.png', width=700)
Image('images/06.png', width=600)
Image('images/07.png', width=500)
Image('images/08.png', width=500)
Image('images/09.png', width=500)
Image('images/10.png', width=500)
Image('images/11.png', width=500)
Image('images/12.png', width=500)
HTML('<h1><a style="color: white" href="https://github.com/maxhumber/pizza">https://github.com/maxhumber/pizza</a></h1>')
Image('images/13.gif', width=500)


#################################
##                             ##
##      W I K I P E D I A      ##
##                             ##
#################################

# target
url = 'https://en.wikipedia.org/wiki/Pizza'
IFrame(url, width=800, height=500)

# pip install gazpacho
from gazpacho import get, Soup

# get the Soup!
html = get(url)
soup = Soup(html)

# find
soup.find('a')
soup.find('h2')

# find 'first'
h2 = soup.find('h2', mode='first')
print(h2)

# isolate text
h2.text

# peel out attributes
h2.attrs
h2.attrs['id']

# find with attributes
sections = soup.find('span', {'class': 'mw-headline'})
print(sections)
print([s.text for s in sections])

# pip install rich
from rich import print
print([s.text for s in sections])

# go fishing for pizza "varieties"
soup.find('div', {'class': 'NavContent hlist'}) # nope...

# chaining finds
links = soup.find('table', {'class':'vertical-navbox nowraplinks'}).find('ul')[1].find('a')
links = [l.attrs['href'] for l in links]
print(links)

#################################
##                             ##
##      🍕 🍕 🍕 🍕 🍕 🍕 🍕     ##
##                             ##
#################################

# conference website
from gazpacho import get, Soup
url = 'https://remote.python.pizza/'
html = get(url)
soup = Soup(html)
print(soup)

Image('images/14.gif', width=500)
Image('images/15.png', width=500)

# pip install selenium
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
browser = Firefox(executable_path='/usr/local/bin/geckodriver', options=options)

# selenium "get"
browser.get(url)
html = browser.page_source
soup = Soup(html)
print(soup)

# find schedule elements
soup.find('li')

# strict find
lis = soup.find('li', {'class': "schedule-item"}, strict=True)

# isolate the first
li = lis[0]
print(li)

# talk title and name of presenter
li.find('h2').text
li.find('a', {'target': '_blank'}).text

# encapsulate
def parse(li):
    title = li.find('h2').text
    name = li.find('a', {'target': '_blank'}).text
    return title, name

# test it on the isolated element
parse(li)

# attempt to roll it over everything
for li in lis:
    parse(li)

# look at the bad li
print(li)

# second attempt
def parse(li):
    title = li.find('h2').text
    try:
        name = li.find('a', {'target': '_blank'}).text
    except:
        name = li.find('p', {'target': '_blank'}).text
    return title, name

talks = [parse(li) for li in lis]
print(talks)

Image('images/16.gif', width=500)

#################################
##                             ##
##          P L U G S          ##
##                             ##
#################################

HTML('<h1><a style="color: white" href="www.twitter.com/maxhumber">@maxhumber</a></h1>')
HTML('<h1><a style="color: white" href="www.linkedin.com/in/maxhumber">/in/maxhumber</a></h1>')

Image('images/17.png', width=500)

# The End.
