from bs4 import BeautifulSoup
import requests
from artist import Artist
from requests_html import HTMLSession
import re
import random

from typing import Dict, List, Tuple

AUTHORS = "https://www.wga.hu/cgi-bin/artist.cgi?"

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
    name = element.find("a").text
    url = element.find("a").get("href")
    art = Artist(name, url)

    return art


def get_image(**kwargs):
    parameters = {"Profession": "any", "School": "any",
                  "Period": "any", "Time-line": "any",
                  "from": "0", "max": "6000", "Sort": "Name",
                  "letter": "-", "width": "700", "targetleft": "0"}

    parse_parameters(parameters, kwargs)
    url = get_url(parameters)
    print(url)
    
    session = HTMLSession()
    response = session.get(url)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    element = soup.find("td", class_="ARTISTLIST")
    if not element:
        print("No artwork found")
        return -1

    artist = parse_artist(element)

    response = session.get(artist.url)
    response.encoding = "utf-8"

    all_pictures_url = re.findall(r"<img src=\"/preview/(.*?)\"", response.text)
    displayed_pic = random.choice(all_pictures_url)

    print(f"{Artist.ART_URL}{displayed_pic}")


if __name__ == "__main__":
    get_image(number=str(random.randint(0, 4000)))
