from account_data_manager import AccountDataManager
from anime_details_retriever import AnimeDetailsRetriever
from anime_name_retriever import AnimeNameRetriever
from datafile_manager import DatafileManager

anime_name_retriever = AnimeNameRetriever()
anime_details_retriever = AnimeDetailsRetriever()
datafile_manager = DatafileManager("all_anime_data.csv")

for anime_name in anime_name_retriever.anime_list:
    # If data already added, skip.
    if not datafile_manager.name_exists(anime_name):
        packaged_anime = anime_details_retriever.get_details(anime_name)
        if packaged_anime is not None:
            datafile_manager.save_data(packaged_anime)

account_data_manager = AccountDataManager()
account_data_manager.save_data()

