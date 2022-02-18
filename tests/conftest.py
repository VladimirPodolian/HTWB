import logging

import pytest
import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from framework.web_driver import WebDriver


def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', help='Run in headless mode')


@pytest.fixture
def chrome_options(request):
    options = ChromeOptions()
    if request.config.getoption('headless'):
        options.headless = True
        # Following options are for docker support
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    return options


@pytest.fixture(autouse=True)
def wrapped_driver(chrome_options, request):
    """ Driver instance setup """
    logging.getLogger("urllib3").setLevel(logging.ERROR)

    wrapped_driver = WebDriver(driver=ChromeWebDriver(options=chrome_options))
    wrapped_driver.driver.implicitly_wait(5)
    wrapped_driver.driver.set_window_size(1200, 1200)
    wrapped_driver.driver.set_window_position(0, 0)
    request.node.node_driver = wrapped_driver.driver

    yield wrapped_driver
    wrapped_driver.driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Customised report generating:

    Original signature:
      https://docs.pytest.org/en/6.2.x/_modules/_pytest/hookspec.html#pytest_runtest_makereport

    Following code is an edited example from:
      https://github.com/pytest-dev/pytest-html/blob/master/docs/user_guide.rst#extra-content
    """
    outcome = yield
    result = outcome.get_result()
    driver = getattr(item, 'node_driver', None)
    xfail = hasattr(result, 'wasxfail')
    failure = (result.skipped and xfail) or (result.failed and not xfail)
    is_allure_connected = item.config.getoption('--alluredir')
    not_teardown = call.when != 'teardown'

    if failure and is_allure_connected and driver:

        if not_teardown:  # screenshot attaching on failure except teardown
            screenshot_name = f'screenshot_{item.name}'
            screenshot_binary = driver.get_screenshot_as_png()
            allure.attach(screenshot_binary, name=screenshot_name, attachment_type=AttachmentType.JPG)
