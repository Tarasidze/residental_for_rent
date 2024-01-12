from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from realtylink_scraper.scraper import Scraper

CHROME_OPTIONS = "--headless=new"
BASE_URL = "https://realtylink.org/en/properties~for-rent"

# options = Options()
# options.add_argument("--headless=new")
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()

number_of_residential = 10


if __name__ == '__main__':

    driver.get(BASE_URL)
    sleep(1)

    scraper = Scraper(
        web_driver=driver,
        base_url=BASE_URL,
    )

    scraper.get_residential_data()
