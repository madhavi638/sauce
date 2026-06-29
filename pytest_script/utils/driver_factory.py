# utils/driver_factory.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.config import BROWSER


def get_driver():
    """
    Factory method — returns a configured WebDriver instance based on
    the BROWSER value defined in utils/config.py.
    Supports: chrome, firefox.
    """
    if BROWSER.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    elif BROWSER.lower() == "firefox":
        options = FirefoxOptions()
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {BROWSER}")
    driver.maximize_window()
    return driver
