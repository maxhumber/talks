import markovify
import pandas as pd

df = pd.read_csv('data/highlights.csv')

text = '\n'.join(df['quote'].values)

model = markovify.NewlineText(text)

for i in range(5):
    print(model.make_sentence())

for i in range(5):
    print(model.make_short_sentence(140))

model.make_short_sentence(140)

generated = '''
The person you aspire to be, you’ll never become that person.
Early Dates are Interviews; don't waste the opportunity to actually move toward a romantic relationship.
Pick a charity or two and set up autopay.
Everyone always wants money, which means you can implement any well-defined function simply by connecting with people’s experiences.
The more you play, the more varied experiences you have, the more people alive under worse conditions.
Men care about resources.
Everything can be swept away by the bear to avoid losing your peace of mind.
Make a spreadsheet. The cells of the future.
'''

[key for key in model.chain.model.keys() if "___BEGIN__" in key]
