import subprocess, sys

try:
    from bs4 import BeautifulSoup
    import requests
except:
    p = subprocess.Popen(['pip', 'install', 'beautifulsoup4'])
    p.wait()
    p = subprocess.Popen(['pip', 'install', 'requests'])
    p.wait()

import re, requests, time
from bs4 import BeautifulSoup


def get_options_list():
    lista_opcoes = []
    url = 'http://www.arenavision.in/iguide/'
    now = time.time() + (19360000 * 1000)
    s = requests.Session()
    s.cookies["beget"]= "begetok"
    s.cookies["expires"] = time.ctime(now)
    s.cookies["path"] = "/"

    soup = BeautifulSoup(s.get(url).text, 'html.parser')
    table = soup.find('table', attrs={'class': 'auto-style1', 'align': 'center', 'cellspacing': '1'})

    if table is not None:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [elem.text.strip() for elem in cols]
            if len(cols) is not 0:
                lista_opcoes.append(cols)
    else:
        print("Fuck")
        exit(1)
    return lista_opcoes


def get_Url(canal):
    url = "http://arenavision.in/"+str(canal)
    now = time.time() + (19360000 * 1000)
    s = requests.Session()
    s.cookies["beget"] = "begetok"
    s.cookies["expires"] = time.ctime(now)
    s.cookies["path"] = "/"
    soup = BeautifulSoup(s.get(url).text, 'html.parser')
    links = soup.body.find_all('a')
    for link in links:
        if "acestream://" in link.get('href'):
            return (link.get('href'))


def format_string(row):
    return row[0] + "   |   " +  \
        " Hora: " + row[1] + "   |   " + \
        " Tipo: " + row[2] + "   |   " + \
        " Liga: " + row[3] + "   |   " + \
        " Jogo: " + row[4]
