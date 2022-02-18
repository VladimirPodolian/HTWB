import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from framework.web_driver import WebDriver


class WebPage:

    def __init__(self, locator, name=None, locator_type=None):
        self.locator_type = locator_type
        self.locator = locator
        self.name = name

        if not locator_type:
            self.locator_type = By.XPATH if '//' in locator else By.CSS_SELECTOR
        else:
            self.locator_type = locator_type

        self.selenium_driver = WebDriver.driver
        self.driver_wrapper = WebDriver(self.selenium_driver)
        self.wait = self.driver_wrapper.wait

    def wait_page_loaded(self):
        logging.info(f'Wait presence of {self.name}')
        self.wait.until(EC.visibility_of_element_located((self.locator_type, self.locator)))
        return self

    def open_page(self, url=''):
        url = getattr(self, 'url', '') if not url else url
        logging.info(f'Navigating to url {url}')
        self.selenium_driver.get(url)
        self.wait_page_loaded()
        return self
