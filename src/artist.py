from unidecode import unidecode

class Artist():

    ART_URL = "https://www.wga.hu/art/"

    def __init__(self, name: str, url: str):
        names = name.split(", ")

        if len(names) < 2:
            names = name.split(" ")

        self.surname = names[0].lower()
        self.other_names = "" if len(names) < 2 else ", ".join(names[1:])
        self.url = url
        self.url_name = self.get_url_name()
        self.artist_url = Artist.ART_URL + self.url_name[0] + "/" + self.url_name
    
    def __str__(self):
        return self.surname.capitalize() + ", " + self.other_names
    
    def get_url_name(self):
        return unidecode(self.surname.split(" ")[0])[:8]