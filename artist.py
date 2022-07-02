from unidecode import unidecode

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
        return unidecode(self.surname.split(" ")[0])[:8]