from bs4 import BeautifulSoup
import requests
import contextlib
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
import os


os.chdir(Path(__file__).parent)

URL = "https://www.goflink.com/de-DE/shop/"

@contextlib.contextmanager
def open_soup(url, headers=None):
    """test"""
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    yield soup


with open_soup(URL) as soup:
    """"""
#    soup.body
    # print(soup.body)

    print(soup.prettify())
    Data = {}
#    Data['title'] = soup.title.string

#    Data['Links'] = {}
#    for a in soup.find_all('div', class_="swimlane"):
#    for a in soup.find_all('div', role="list"):
#        print(a)
#        Data['Links'][a.get('href')] = a.string

json.dump(Data, open('./test.json', 'w'), indent=4)

#for zeile in Data['Links']:
#    print(zeile)
