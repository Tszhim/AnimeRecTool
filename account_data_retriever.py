import time
from selenium import webdriver

class AccountDataRetriever:

    def __init__(self, username):
        chrome_driver_path = "C:\\Users\\falco\\OneDrive\\Desktop\\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        self.endpoint = f"https://myanimelist.net/animelist/{username}"

    def retrieve_data(self):
        self.driver.get(self.endpoint)

        time.sleep(0.5)