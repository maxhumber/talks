import pandas as pd
from io import StringIO

# option 1
import pandas as pd

data = [
    ['conference', 'month', 'attendees'],
    ['ODSC', 'May', 5000],
    ['PyData', 'June', 1500],
    ['PyCon', 'May', 3000],
    ['useR!', 'July', 2000],
    ['Strata', 'August', 2500]
]
df = pd.DataFrame(data, columns=data.pop(0))

# option 2

data = {
    'package': ['requests', 'pandas', 'Keras', 'mummify'],
    'installs': [4000000, 9000000, 875000, 1200]
}
df = pd.DataFrame(data)

# option 3

df = pd.DataFrame([
    {'artist': 'Bino', 'plays': 100_000},
    {'artist': 'Drake', 'plays': 1_000},
    {'artist': 'ODESZA', 'plays': 10_000},
    {'artist': 'Brasstracks', 'plays': 100}
])

# option 4
from io import StringIO

csv = '''\
    food,fat,carbs,protein
    avocado,0.15,0.09,0.02
    orange,0.001,0.12,0.009
    almond,0.49,0.22,0.21
    steak,0.19,0,0.25
    peas,0,0.04,0.1
'''

# won't work
pd.read_csv(csv)

# ---------------------------------------------------------------------------
# FileNotFoundError                         Traceback (most recent call last)
# <ipython-input-22-b8ca875b07d1> in <module>()
# ----> 1 pd.read_csv(csv)
#
# FileNotFoundError: File b'food,fat,carbs,protein\n...' does not exist

df = pd.read_csv(StringIO(csv))
