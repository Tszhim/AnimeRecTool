import requests
from bs4 import BeautifulSoup
from datetime import datetime


# Get current season for query.
def get_season():
    curr_month = datetime.now().month
    if curr_month < 4:
        return "winter"
    elif 3 < curr_month < 7:
        return "spring"
    elif 6 < curr_month < 10:
        return "summer"
    else:
        return "fall"


# Get current year for query.
def get_year():
    return datetime.now().year


class AnimeNameRetriever:

    # Information necessary to reach endpoint for info.
    def __init__(self):
        self.anime_list = []
        self.endpoint = "https://myanimelist.net/anime/season"
        self.iterating_season = get_season()
        self.iterating_year = get_year()

        # Change number here to retrieve all anime names from within the past x years.
        while get_year() - self.iterating_year < 5:
            self.retrieve_data()

    # Retrieving names and storing them.
    def retrieve_data(self):
        response = requests.get(self.endpoint)
        soup = BeautifulSoup(response.text, "html.parser")

        names = soup.find_all(class_="link-title")
        for name in names:
            self.anime_list.append(name.getText())

        self.update_endpoint()

    # Updating endpoint as it progresses through past seasons and years.
    def update_endpoint(self):
        if self.iterating_season == "fall":
            self.iterating_season = "summer"
        elif self.iterating_season == "summer":
            self.iterating_season = "spring"
        elif self.iterating_season == "spring":
            self.iterating_season = "winter"
        else:
            self.iterating_season = "fall"
            self.iterating_year = self.iterating_year - 1

        self.endpoint = f"https://myanimelist.net/anime/season/{self.iterating_year}/{self.iterating_season}"
