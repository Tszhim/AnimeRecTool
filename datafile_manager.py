import csv
import pandas


class DatafileManager:

    def __init__(self, save_location):
        self.save_location = save_location

    def save_data(self, anime):
        data = {
            "Name": [anime.name],
            "Score": [anime.score],
            "Rank": [anime.rank],
            "Popularity": [anime.popularity],
            "Genres": [anime.genres],
            "Episodes": [anime.episodes],
            "Start Date": [anime.start_date],
            "End Date": [anime.end_date],
            "Producers": [anime.producers],
            "Studios": [anime.studios]
        }
        df = pandas.DataFrame(data)
        df.to_csv(self.save_location, mode="a", index=False, header=False)

    def name_exists(self, anime_name):
        with open(self.save_location, "r", encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=",")
            for row in csv_reader:
                if len(row) != 0 and anime_name in row[0]:
                    f.close()
                    return True
            f.close()
            return False
