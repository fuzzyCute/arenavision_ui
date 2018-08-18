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

def get_data():
    #This funcion will allow the user to get all the data and url for the games so that the buttons can be created automatically
    # 1 - create the json variable 
    # 2 - create the session variable
    # 3 - get the arenavision data
    # 4 - get all channels url into an array so that it'll be added to the games, and their urls
    # 5 - get the events guide url, because it's always changing, dirty bastards
    # 6 - do a new request with the session with the new events guide url
    # 7 - get all games information
    # 8 - add that information to the json
    # 9 - in the channels part, add the url of those channels
    # 10 - return the json

    json_to_send = {} #json data to send to user
    json_to_send["flags"] = [] # for the languages of the flags
    json_to_send["games"] = {} # FOR ALL THE GAMES
    
    url_website = "http://arenavision.in/" #arenavision url, change this if link changes
    url_events = "" #this will be the url for the events guide which it's always changing
    url_channels = [] #this will be used for the channels urls, the order will be from 1 to x, so it'll be 1 = 0, 2 = 1, etc...
    
    now = time.time() + (19360000 * 1000) #needed for the session(stupid passby that is needed on the webside)
    
    #session part, to be able to access the webside
    s = requests.Session()
    s.cookies["beget"] = "begetok"
    s.cookies["expires"] = time.ctime(now)
    s.cookies["path"] = "/"
    #end of session passby

        
    soup = BeautifulSoup(s.get(url_website).text, 'html.parser') #all the data from the initial website
    #print(soup.prettify())

    for ulTag in soup.find_all('ul', {'class' : 'menu'}):
        for liTag in ulTag.find_all('li'):
            if liTag.text == "EVENTS GUIDE":
                link = liTag.find_all('a', href=True)
                for a in link:
                    url_events = url_website + a['href']
                    
            elif 'leaf' in liTag['class']:
                link = liTag.find_all('a' , href=True)
                for a in link:
                    if a['href'] not in url_channels and a['href'].startswith("http"):
                        url_channels.append(a['href'])

    
    soup = BeautifulSoup(s.get(url_events).text, 'html.parser') #get all data from the events website
    
    table = soup.find('table', attrs={'class': 'auto-style1', 'align': 'center', 'cellspacing': '1'})
    rows = table.find_all('tr')
    game_number = 1

    days = []

    for row in rows:
        cols = row.find_all('td')
        cols = [elem.text.strip() for elem in cols]
        if len(cols) is not 0 and cols[0] is not "" and len(cols) is 6:
            
            date_add = cols[0].split("/")
            cols[0] = date_add[0] + "/" + date_add[1]

            if cols[0] not in days:
                days.append(cols[0])


            #json para ser enviado para o outro lado
            temp_ch = cols[5].split()
            if len(temp_ch) is not 0 and len(temp_ch) > 2:
                while len(temp_ch) != 0:
                    json_to_send["games"]["game" + str(game_number)] = {}
                    game_language = temp_ch.pop()
                    game_channels = temp_ch.pop()
                    json_to_send["games"]["game" + str(game_number)]["date"] = cols[0]
                    json_to_send["games"]["game" + str(game_number)]["time"] = cols[1]
                    json_to_send["games"]["game" + str(game_number)]["type"] = cols[2]
                    json_to_send["games"]["game" + str(game_number)]["league"] = cols[3]
                    json_to_send["games"]["game" + str(game_number)]["players"] = cols[4]
                    json_to_send["games"]["game" + str(game_number)]["language"] = game_language
                    json_to_send["games"]["game" + str(game_number)]["Channels"] = [[url_channels[int(x) - 1], int(x)] for x in game_channels.split("-")]
                    game_number = game_number + 1
            else:
                json_to_send["games"]["game" + str(game_number)] = {}
                json_to_send["games"]["game" + str(game_number)]["date"] = cols[0]
                json_to_send["games"]["game" + str(game_number)]["time"] = cols[1]
                json_to_send["games"]["game" + str(game_number)]["type"] = cols[2]
                json_to_send["games"]["game" + str(game_number)]["league"] = cols[3]
                json_to_send["games"]["game" + str(game_number)]["players"] = cols[4]
                json_to_send["games"]["game" + str(game_number)]["language"] = temp_ch[1]
                json_to_send["games"]["game" + str(game_number)]["Channels"] = [[url_channels[int(x) - 1], int(x)] for x in temp_ch[0].split("-")]
                game_number = game_number + 1
    json_to_send["session"] = s # SEND THE SESSION TO BE REUSED

    json_to_send["days_to_Select"] = days # the days so you can select


    return json_to_send

def get_link_to_ace_streamer(session, url):
    soup = BeautifulSoup(session.get(url).text, 'html.parser')
    links = soup.body.find_all('a')
    for link in links:
        if "acestream://" in link.get('href'):
            return(link.get('href').split("//")[1])
