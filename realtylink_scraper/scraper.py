"""Script for parsing https://realtylink.org/en/properties~for-rent"""
from __future__ import annotations

import json
from typing import Any, List
from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

from realtylink_scraper import scraper_config
from realtylink_scraper.scraper_config import Residence
from realtylink_scraper.loger import logging


class Scraper:
    """"""
    def __init__(
            self,
            web_driver: webdriver,
            base_url: str,
    ) -> None:
        self._web_driver = web_driver
        self._base_url = base_url
        self._number_of_pages = 20
        self._number_of_objects = 60
        self._delay = 3

    def get_pagination_number(self) -> int:
        """Function return number of pages."""

        try:
            pagination = self._web_driver.find_element(
                By.CLASS_NAME, scraper_config.CLASS_PAGE_PAGINATION
            ).text.split()[-1]
            logging.info(f"Time: {datetime.now()}, Pagination: {pagination}")
        except NoSuchElementException:
            return 1

        return int(pagination)

    def get_residential_links(self) -> List[str]:
        """Function returns list of links to residences"""
        if self._number_of_pages is None or self._number_of_pages > self.get_pagination_number():
            self._number_of_pages = self.get_pagination_number()

        residential_objects = self._web_driver.find_elements(
            By.CLASS_NAME,
            scraper_config.CLASS_RESID_LINK,
        )

        list_of_links = [
            residential.get_attribute('href')
            for residential in residential_objects
        ]

        sleep(0.4)

        for page in range(self._number_of_pages):
            pagination_button = self._web_driver.find_element(
                By.CLASS_NAME,
                scraper_config.CLASS_NEXT_BUTTON
            )

            if pagination_button is None:
                break

            pagination_button.click()

            residential_objects = self._web_driver.find_elements(
                By.CLASS_NAME,
                scraper_config.CLASS_RESID_LINK,
            )

            list_of_links.extend([
                residential.get_attribute('href')
                for residential in residential_objects
            ])
            logging.info(
                f"Time: {datetime.now()}, Quantity of page links = : {len(list_of_links)}"
            )

            sleep(0.4)

        return list_of_links

    def get_image_links_v2(self, residential_link: str) -> List[str] | None:
        """Function collects images link and returns list of it otherwise return None"""
        img_url_list = []

        self._web_driver.get(residential_link)

        sleep(0.4)

        try:
            images_library = WebDriverWait(
                self._web_driver, self._delay
            ).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, scraper_config.CSS_IMAGE_LIB))
            )

            images_library.click()

        except (NoSuchElementException, TimeoutException):
            return None

        sleep(0.2)

        img_obj = WebDriverWait(self._web_driver, self._delay).until(
            EC.presence_of_element_located((By.ID, "fullImg")))
        img_url = img_obj.get_attribute("src")

        sleep(0.2)

        while img_url not in img_url_list:
            try:
                img_url_list.append(img_url)
                img_obj.click()
            except ElementNotInteractableException:
                break

            img_obj = WebDriverWait(self._web_driver, self._delay).until(
                EC.presence_of_element_located((By.ID, "fullImg")))
            img_url = img_obj.get_attribute("src")

            sleep(0.4)

        logging.info(
            f"Time: {datetime.now()}, Found {len(img_url_list)} image links"
        )

        return img_url_list

    def find_element_by_xpath(self, xpath: str) -> Any:
        """Function return text from XPATH."""
        try:
            element = self._web_driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None

        return element.text

    @staticmethod
    def read_from_json(filename):
        try:
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            return []

    def write_to_json(self, residence: Residence, filename='residences_v4.json'):
        """Save JSON object to file."""
        existing_data = self.read_from_json(filename)
        existing_data.append(vars(residence))

        with open(filename, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)

        logging.info(
            f"Time: {datetime.now()}, residence {residence.title} saved"
        )

    def get_residential_data(self) -> json:
        """Collect information from page."""

        residence_links = self.get_residential_links()

        residence_counter = 0

        for link in residence_links:

            self._web_driver.get(link)

            sleep(0.5)

            residence = Residence(
                link=link,
                title=self.find_element_by_xpath(scraper_config.XPATH_TITLE),
                region=",".join(self.find_element_by_xpath(scraper_config.XPATH_REGION).split(",")[-2:]),
                address=self.find_element_by_xpath(scraper_config.XPATH_ADDRESS),
                description=self.find_element_by_xpath(scraper_config.XPATH_DESCR),
                publish_date=None,
                price=self.find_element_by_xpath(scraper_config.XPATH_PRICE),
                bedrooms=self.find_element_by_xpath(scraper_config.XPATH_BEDROOM).split()[0],
                floor_area=self.find_element_by_xpath(scraper_config.XPATH_FLOOR_AREA).split()[0],
                image_links=self.get_image_links_v2(link),
            )

            logging.info(
                f"Time: {datetime.now()}, residence object {residence.title} created"
            )

            self.write_to_json(residence)

            residence_counter += 1
            if residence_counter >= self._number_of_objects:
                break

            sleep(0.2)
