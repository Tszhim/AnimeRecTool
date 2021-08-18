from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import time

from anime import Anime


class AnimeDetailsRetriever:

    def __init__(self):
        chrome_driver_path = "C:\\Users\\falco\\OneDrive\\Desktop\\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)

    # Reach website page where the details can be extracted.
    def navigate_to_details(self, anime_name):
        self.driver.get("https://google.com")

        time.sleep(0.5)
        search_box = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
        search_box.send_keys(f"MyAnimeList {anime_name} Anime")
        search_box.submit()

        time.sleep(0.5)
        website_link = self.driver.find_element_by_css_selector("h3")
        website_link.click()

        time.sleep(0.5)
        try:
            details_button = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/table/tbody/tr/td[2]/div[1]/div[2]/ul/li[1]/a")
        except NoSuchElementException:
            details_button = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[2]/table/tbody/tr/td[2]/div[1]/div[2]/ul/li[1]/a")
        details_button.click()

    # Retrieving information about anime and constructing it into anime object.
    def get_details(self, anime_name):
        self.navigate_to_details(anime_name)

        time.sleep(0.5)
        try:
            score_element = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[1]/div")
        except NoSuchElementException:
            score_element = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[1]/div")
        try:
            rank_element = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/strong")
        except NoSuchElementException:
            rank_element = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/strong")
        try:
            popularity_element = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]/strong")
        except NoSuchElementException:
            popularity_element = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]/strong")
        ep, air, prod, stud = self.sort_info()
        episodes_element = ep
        air_date_element = air
        producers_element = prod
        studios_element = stud

        score = score_element.text
        try:
            rank = rank_element.text.split("#")[1]
        except IndexError:
            rank = "?"
        popularity = popularity_element.text.split("#")[1]
        episodes = episodes_element.text.split(" ")[1]
        start_date = air_date_element.text.split(" to ")[0].split(": ")[1]
        try:
            end_date = air_date_element.text.split(" to ")[1]
        except IndexError:
            end_date = "?"
        producers = producers_element.text.split(": ")[1]
        studios = studios_element.text.split(": ")[1]

        packaged_anime = Anime(anime_name, score, rank, popularity, episodes, start_date, end_date, producers, studios)
        return packaged_anime

    # Helper function for get_details() to ensure each element is identified correctly.
    def sort_info(self):
        episodes_element = None
        air_date_element = None
        producers_element = None
        studios_element = None

        info_blocks = self.driver.find_elements_by_class_name("spaceit")
        for info_block in info_blocks:
            if "Episodes:" in info_block.text:
                episodes_element = info_block
            elif "Aired:" in info_block.text:
                air_date_element = info_block

        info_blocks = self.driver.find_elements_by_class_name("dark_text")
        for info_block in info_blocks:
            if "Producers:" in info_block.text:
                producers_element = info_block.find_element_by_xpath("./..")
            elif "Studios:" in info_block.text:
                studios_element = info_block.find_element_by_xpath("./..")

        return episodes_element, air_date_element, producers_element, studios_element


