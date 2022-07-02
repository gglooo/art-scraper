from bs4 import BeautifulSoup
import requests
from artist import Artist
from requests_html import HTMLSession
import re
import random
import os
import json

from typing import Dict, List, Tuple

AUTHORS = "https://www.wga.hu/cgi-bin/artist.cgi?"
CACHE_FOLDER = "cache"

def parse_parameters(parameters: Dict[str, str],
                     kwargs: Dict[str, str]) -> None:
    changed = False
    for key in kwargs.keys():
        if key == "number":
            key = "from"
            changed = True
        if key not in parameters and key.capitalize() not in parameters:
            raise KeyError(f"{key} is not a valid parameter")
        
        if key in parameters:
            parameters[key] = kwargs[key if not changed else "number"]
        else:
            parameters[key.capitalize()] = kwargs[key]
    
    return None


def get_url(parameters: Dict[str, str]) -> str:
    url = AUTHORS
    for key, value in parameters.items():
        url += f"{key}={value}&"
    return url[:-1] # returning without last '&' symbol


def parse_artist(element) -> Artist:
    name = element.contents[0].text
    url = element.get("href")
    art = Artist(name, url)

    return art


def parse_and_cache(session, url: str, cache_file: str):
    response = session.get(url)
    response.encoding = "utf-8"
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    elements = [parse_artist(elem.next) for elem in soup.find_all("td", class_="ARTISTLIST") 
                if len(str(elem.next)) > 1 and str(elem.next)[0] == "<" and str(elem.next)[1] == "a"]
    
    data = [{"name": f"{elem.surname + ', ' + elem.other_names}", "url": f"{elem.url}"} for elem in elements]
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
    
    return elements


def parse_artist_from_dct(data: Dict[str, str]):
    return Artist(data["name"], data["url"])


def get_image(force_mode: bool=False, **kwargs):
    parameters = {"Profession": "any", "School": "any",
                  "Period": "any", "Time-line": "any",
                  "from": "0", "max": "6000", "Sort": "Name",
                  "letter": "-", "width": "700", "targetleft": "0"}

    parse_parameters(parameters, kwargs)
    url = get_url(parameters)
    session = HTMLSession()

    if not os.path.exists(CACHE_FOLDER):
        os.mkdir(CACHE_FOLDER)
    
    cache_file = CACHE_FOLDER + "/" + url.split("?")[1].split("from")[0]

    if os.path.exists(cache_file) and not force_mode:
        with open(cache_file, "r", encoding="utf-8") as f:
            artists = json.load(f)
            artist = parse_artist_from_dct(random.choice(artists))
    else:
        artists = parse_and_cache(session, url, cache_file)
        artist = random.choice(artists)

    if not artist:
        print("No artwork found")
        return -1

    response = session.get(artist.url)
    response.encoding = "utf-8"

    all_pictures_url = re.findall(r"<img src=\"/preview/(.*?)\"", response.text)
    if not all_pictures_url:
        print("No artwork found")
        return -1
    displayed_pic = random.choice(all_pictures_url)

    print(f"{Artist.ART_URL}{displayed_pic}")
    print(f"{artist.artist_url}")


if __name__ == "__main__":
    get_image(school="Bohemian")
