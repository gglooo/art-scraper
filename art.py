from bs4 import BeautifulSoup
import requests
import os
import unidecode

from typing import Dict, List, Tuple

AUTHORS = "https://www.wga.hu/cgi-bin/artist.cgi?"

class Artist():

    def __init__(self, name: str, url: str):
        names = name.split(", ")

        if len(names) != 2:
            raise ValueError("Invalid artist name")

        self.surname = names[0].lower()
        self.other_names = names[1]
        self.url = url
        self.url_name = self.get_url_name()
    
    def __str__(self):
        return self.surname.capitalize() + ", " + self.other_names
    
    def get_url_name(self):


def parse_parameters(parameters: Dict[str, str],
                     kwargs: Dict[str, str]) -> None:

    for key in kwargs.keys():
        if key not in parameters and key.capitalize() not in parameters:
            raise KeyError(f"{key} is not a valid parameter")
        
        if key in parameters:
            parameters[key] = kwargs[key]
        else:
            parameters[key.capitalize()] = kwargs[key]
    
    return None


def get_url(parameters: Dict[str, str]) -> str:
    url = AUTHORS
    for key, value in parameters.items():
        url += f"{key}={value}&"
    return url[:-1] # returning without last '&' symbol


def parse_artist(element) -> Tuple[str, str]:
    name = element.find("a").text
    url = element.find("a").get("href")
    art = Artist(name, url)

    return art


def get_image(**kwargs):
    parameters = {"Profession": "any", "School": "any",
                  "Period": "any", "Time-line": "any",
                  "from": "3", "max": "50", "Sort": "Name",
                  "letter": "-", "width": "700", "targetleft": "0"}

    parse_parameters(parameters, kwargs)
    url = get_url(parameters)
    print(url)
    
    response = requests.get(url)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    element = soup.find("td", class_="ARTISTLIST")
    print(element)
    if not element:
        print("No artwork found")
        return -1
    artist = parse_artist(element)
    print(artist)


if __name__ == "__main__":
    get_image(school="Hungarian")
