import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from anime_details_retriever import AnimeDetailsRetriever
from datafile_manager import DatafileManager


class AccountDataManager:

    def __init__(self):
        self.username = input("Enter your MyAnimeList Username.")
        self.packaged_animes = []
        chrome_driver_path = "C:\\Users\\falco\\OneDrive\\Desktop\\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        self.endpoint = f"https://myanimelist.net/animelist/{self.username}"
        self.anime_details_retriever = AnimeDetailsRetriever()
        self.datafile_manager = DatafileManager("user_anime_data.csv")
        self.retrieve_names()

    def retrieve_names(self):
        self.driver.get(self.endpoint)
        self.select_completed()
        self.scroll_to_bottom()

        anime_names = []
        anime_blocks = WebDriverWait(self.driver, 5).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, ".data.title.clearfix")))
        for anime_block in anime_blocks:
            anime_link_element = anime_block.find_element_by_xpath("*")
            anime_names.append(anime_link_element.text)

        self.retrieve_data(anime_names)

    def select_completed(self):
        completed_button = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, ".status-button.completed")))
        completed_button.click()

    def scroll_to_bottom(self):
        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            curr_height = self.driver.execute_script("return document.body.scrollHeight")
            if prev_height == curr_height:
                break
            else:
                prev_height = curr_height

    def retrieve_data(self, anime_names):
        for anime_name in anime_names:
            if not self.datafile_manager.name_exists(anime_name):
                packaged_anime = self.anime_details_retriever.get_details(anime_name)
                self.packaged_animes.append(packaged_anime)

    def save_data(self):
        for packaged_anime in self.packaged_animes:
            self.datafile_manager.save_data(packaged_anime)
