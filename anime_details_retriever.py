from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from anime import Anime


class AnimeDetailsRetriever:

    def __init__(self):
        chrome_driver_path = "C:\\Users\\falco\\OneDrive\\Desktop\\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)

    # Reach website page where the details can be extracted.
    def navigate_to_details(self, anime_name):
        self.driver.get("https://google.com")

        search_box = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")))
        search_box.send_keys(f"MyAnimeList {anime_name} Anime")
        search_box.submit()

        website_link = WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "h3")))
        website_link.click()

        if "/anime/" in self.driver.current_url:
            try:
                details_button = WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Details")))
                details_button.click()
                return True
            except TimeoutException:
                return False
        else:
            return False

    # Retrieving information about anime and constructing it into anime object.
    def get_details(self, anime_name):
        cont = self.navigate_to_details(anime_name)
        print(cont)
        if cont is True:
            score_block = WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".fl-l.score")))
            score_element = score_block.find_element_by_xpath("*")

            rank_block = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, ".numbers.ranked")))
            rank_element = rank_block.find_element_by_xpath("*")

            popularity_block = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, ".numbers.popularity")))
            popularity_element = popularity_block.find_element_by_xpath("*")

            try:
                genre_elements = WebDriverWait(self.driver, 5).until(ec.presence_of_all_elements_located((By.XPATH, "//span[@itemprop='genre']")))
            except TimeoutException:
                genre_elements = []

            ep, air, prod, stud = self.sort_table_info()

            episodes_element = ep
            air_date_element = air
            producers_element = prod
            studios_element = stud

            packaged_anime = self.package_details(anime_name, score_element, rank_element, popularity_element,
                                                  genre_elements, episodes_element, air_date_element, producers_element,
                                                  studios_element)
            return packaged_anime
        else:
            return None

    # Helper function for get_details() to ensure each element is identified correctly.
    def sort_table_info(self):
        episodes_element = None
        air_date_element = None
        producers_element = None
        studios_element = None

        info_blocks = WebDriverWait(self.driver, 5).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "spaceit")))
        for info_block in info_blocks:
            if "Episodes:" in info_block.text:
                episodes_element = info_block
            elif "Aired:" in info_block.text:
                air_date_element = info_block

        info_blocks = WebDriverWait(self.driver, 5).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "dark_text")))
        for info_block in info_blocks:
            if "Producers:" in info_block.text:
                producers_element = info_block.find_element_by_xpath("./..")
            elif "Studios:" in info_block.text:
                studios_element = info_block.find_element_by_xpath("./..")

        return episodes_element, air_date_element, producers_element, studios_element

    # Helper function to extract and clean information from retrieved elements.
    def package_details(self, anime_name, score_element, rank_element, popularity_element, genre_elements, episodes_element, air_date_element, producers_element, studios_element):
        score = score_element.text
        try:
            rank = rank_element.text.split("#")[1]
        except IndexError:
            rank = "?"
        popularity = popularity_element.text.split("#")[1]

        genres = ""
        for i in range(0, len(genre_elements)):
            if i != len(genre_elements) - 1:
                genres = genres + genre_elements[i].get_attribute("innerHTML") + ", "
            else:
                genres = genres + genre_elements[i].get_attribute("innerHTML")

        episodes = episodes_element.text.split(" ")[1]
        start_date = air_date_element.text.split(" to ")[0].split(": ")[1]
        try:
            end_date = air_date_element.text.split(" to ")[1]
        except IndexError:
            end_date = "?"
        producers = producers_element.text.split(": ")[1]
        studios = studios_element.text.split(": ")[1]

        return Anime(anime_name, score, rank, popularity, genres, episodes, start_date, end_date, producers, studios)
