# poetry run python .\program3.py -f output.json
# cd .\lab\lab03\

import argparse
from textwrap import indent
from matplotlib import pyplot as plt
import numpy as np
from rich.console import Console
import rich.traceback
from rich.progress import track
import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import json

console = Console()
console.clear()
console.rule('Web-scraping.')
console.print()
rich.traceback.install()

parser = argparse.ArgumentParser(description="Web Scraping")
parser.add_argument('-f', help='Nazwa pliku do zapisu', default='output.json', type=str)

args = parser.parse_args()

output_file = args.f

website = "https://en.wikipedia.org/wiki/COVID-19_pandemic_death_rates_by_country"

req = requests.get(website)
console.print(f'{req.status_code = }')

soup = BeautifulSoup(req.text, 'html.parser')
wiki_talbe = soup.find('table',{'class':"wikitable"})

df_init=pd.read_html(str(wiki_talbe))
df=pd.DataFrame(df_init[0])

cov = df.drop(["Unnamed: 4", "Unnamed: 5","Unnamed: 6", "Unnamed: 7"], axis=1)
cov = cov[1:-1]
cov = cov.replace('—', "0")

cov[["Deaths per million", "Deaths", "Cases"]] = cov[["Deaths per million", "Deaths", "Cases"]].apply(pd.to_numeric)
cov.sort_values(by='Deaths per million')

cov.to_json(f'data/{output_file}', orient="split", indent = 4)

cov_top = cov.head(10)
console.print(cov_top)

chart = sns.barplot(data=cov_top, x = 'Country', y = 'Deaths per million')
chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='center')
plt.show()