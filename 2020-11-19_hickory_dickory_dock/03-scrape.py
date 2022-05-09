from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from gazpacho import Soup

options = Options()
options.headless = True
browser = Firefox(executable_path="/usr/local/bin/geckodriver", options=options)

url = "https://www.amazon.ca/Witcher-Nintendo-Switch-Games-Software/dp/B07T4D63YT/"

browser.get(url)
html = browser.page_source
soup = Soup(html)

"Witcher 3" in str(soup)

price = soup.find("span", {"id": "price"}, partial=True, mode='first').text
price = float(price.replace("CDN$\xa0", ""))

message = f"The Witcher 3 is ${price} on Amazon.ca right now"

print(message)
