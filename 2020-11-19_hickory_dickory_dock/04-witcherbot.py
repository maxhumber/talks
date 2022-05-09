from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from gazpacho import Soup

# NEW ---
from email.message import EmailMessage
import os
import smtplib
from dotenv import load_dotenv

load_dotenv(".env")

SENDER = os.environ.get("GMAIL_USER")
PASSWORD = os.environ.get("GMAIL_PASSWORD")
RECIPIENT = os.environ.get("RECIPIENT_EMAIL")
# ---

options = Options()
options.headless = True
browser = Firefox(executable_path="/usr/local/bin/geckodriver", options=options)

def scrape():
    url = "https://www.amazon.ca/Witcher-Nintendo-Switch-Games-Software/dp/B07T4D63YT/"
    browser.get(url)
    html = browser.page_source
    soup = Soup(html)
    price = soup.find("span", {"id": "price"}, partial=True, mode='first').text
    price = float(price.replace("CDN$\xa0", ""))
    return f"The Witcher 3 is ${price} on Amazon.ca right now"

# NEW ---
def send_email():
    body = scrape()
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = "WitcherBot"
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    # https://support.google.com/accounts/answer/185833
    send_email()
