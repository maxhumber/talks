import pandas as pd
import sqlite3
from faker import Faker

# pip install Faker
from faker import Faker
fake = Faker()

fake.name()

fake.phone_number()

fake.bs()

fake.profile()

def create_rows(n=1):
    output = [{
        'created_at': fake.past_datetime(start_date='-365d', tzinfo=None),
        'name': fake.name(),
        'occupation': fake.job(),
        'address': fake.street_address(),
        'credit_card': fake.credit_card_number(card_type='visa'),
        'company_bs': fake.bs(),
        'city': fake.city(),
        'ssn': fake.ssn(),
        'paragraph': fake.paragraph()}
        for x in range(n)]
    return pd.DataFrame(output)

df = create_rows(10)


import pandas as pd
import sqlite3

con = sqlite3.connect('data/fake.db')
cur = con.cursor()

df.to_sql(name='users', con=con, if_exists="append", index=True)

pd.read_sql('select * from users', con)
