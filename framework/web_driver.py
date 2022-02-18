from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from framework.utils import log


class WebDriver:
    driver = None

    def __init__(self, driver):
        self.driver = driver
        self.alert = Alert(self.driver)
        self.wait = WebDriverWait(self.driver, 10)
        WebDriver.driver = self.driver

    @property
    def current_url(self):
        log('Getting current url')
        return self.driver.current_url

    def type_text_to_editor(self, text):
        log(f'Type text "{text}" into window.editor')
        self.driver.execute_script('window.editor.setValue(arguments[0]);', text)
        return self

    def clear_text_from_editor(self):
        log(f'Clear text from window.editor')
        self.driver.execute_script('window.editor.setValue("");')
        return self

    def accept_alert(self):
        log('Accepting alert')
        self.alert.accept()
        return self

    def wait_alert(self):
        log('Wait until alert presence')
        self.wait.until(EC.alert_is_present(), 'Timeout for waiting alert')
        return self

