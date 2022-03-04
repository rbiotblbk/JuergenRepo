from bs4 import BeautifulSoup
import contextlib
from pathlib import Path
import json
import os
import requests
import glob
import sys
import mechanicalsoup
# import pandas as pd
# import matplotlib.pyplot as plt

APP_DIR = Path(__file__).parent
os.chdir(APP_DIR)


@contextlib.contextmanager
def open_soup(html, headers=None):
    if 'https' in html:
        page = requests.get(html)
        soup = BeautifulSoup(page.text, "html.parser")
        yield soup
    else:
        with open(html, 'r', encoding="utf-8") as f:
            contents = f.read()
            soup = BeautifulSoup(contents, "html.parser")
            yield soup


def create_config(soup):
    Data = {}
    i = 0
    for a in soup.find_all("div", id="pagetop"):
        Data[i] = ['div', 'id', 'pagetop']
    i += 1

    for a in soup.find_all("div", id="footer"):
        Data[i] = ['div', 'id', 'footer']
    i += 1

    for a in soup.find_all("div", id="right"):
        Data[i] = ['div', 'id', 'right']
    i += 1

    for a in soup.find_all("div", id="mainLeaderboard"):
        Data[i] = ['div', 'id', 'mainLeaderboard']
    i += 1

    for a in soup.find_all("div", class_="w3-clear nextprev"):
        Data[i] = ['div', 'class_', 'w3-clear nextprev']
    i += 1

    for a in soup.find_all("div", id="topnav"):
        Data[i] = ['div', 'id', 'topnav']
    i += 1

    for a in soup.find_all("div", id="midcontentadcontainer"):
        Data[i] = ['div', 'id', 'midcontentadcontainer']
    i += 1

    for a in soup.find_all('div', id='getdiploma'):
        Data[i] = ['div', 'id', 'getdiploma']
    i += 1

    for a in soup.find_all('iframe'):
        Data[i] = ['iframe']
    i += 1

    for a in soup.find_all('argprec0'):
        Data[i] = ['argprec0']
    i += 1

    for a in soup.find_all('argprec1'):
        Data[i] = ['argprec1']
    i += 1

    for a in soup.find_all("style", class_="sf-hidden"):
        Data[i] = ['style', 'class_', 'sf-hidden']
    i += 1

    for a in soup.find_all('div', id='googleSearch'):
        Data[i] = ['div', 'id', 'googleSearch']
    i += 1

    for a in soup.find_all('div', id='google_translate_element'):
        Data[i] = ['div', 'id', 'google_translate_element']
    i += 1

    for a in soup.find_all('div', id='myAccordion'):
        Data[i] = ['div', 'id', 'myAccordion']
    i += 1

    for a in soup.find_all('div', id='snigel-cmp-framework'):
        Data[i] = ['div', 'id', 'snigel-cmp-framework']
    i += 1

    for a in soup.find_all('a', href='https://www.w3schools.com/'):
        Data[i] = ['a', 'href', 'https://www.w3schools.com/']
    i += 1
    return Data


def create_menue(soup):
    Data = {}
    h = soup.find('h2', class_="left")
    ltext = h.text
    inner = {}
    for a in h.find_next_siblings(['a', 'h2']):
        if 'h2' in repr(a):
            Data[ltext] = inner
            inner = {}
            ltext = a.text
        else:
            inner[a.text] = a.get('href')
    Data[ltext] = inner
    return Data


def scrap_soup(soup):
    with open("./config_extract.json", mode="r", encoding="utf-8") as f:
        json_dict = json.loads(f.read())

        for i in range(len(json_dict)):
            if len(json_dict[str(i)]) == 1:
                for a in soup.find_all(json_dict[str(i)][0]):
                    a.extract()
            else:
                ding = {}
                ding[json_dict[str(i)][1]] = json_dict[str(i)][2]
                for a in soup.find_all(json_dict[str(i)][0], attrs=ding):
                    a.extract()


# glob
for name in glob.glob("./Sourcefiles/*.html"):
    print(name)
    with open_soup(name) as soup:
        # config = create_config(soup)
        # json.dump(config, open('./config_extract.json', 'w'), indent=4)

        # menue = create_menue(soup)
        # json.dump(menue, open('./menue.json', 'w'), indent=4)

        scrap_soup(soup)
        file_name = name.replace("Sourcefiles", "Targets")
        with open(file_name, "w", encoding='utf-8') as file:
            file.write(str(soup))

sys.exit()
# mechanical soup
with open("./menue.json", mode="r", encoding="utf-8") as f:
    menu_dict = json.loads(f.read())

    # FIXME: trtreter
    for wert in menu_dict:
        print(wert, len(menu_dict[wert]))
        i = 0
        for wert2 in menu_dict[wert]:
            browser = mechanicalsoup.StatefulBrowser()
            browser.open(menu_dict[wert][wert2])
            scrap_soup(browser.page)
            file_name = "./ASP_HTML/" + \
                wert.replace(' ', '') + str(i) + '.html'
            with open(file_name, "w", encoding='utf-8') as file:
                file.write(str(browser.page))
            i += 1
# TODO: fdfd
