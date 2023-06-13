from enum import Enum

from selenium import webdriver
from selenium.webdriver import FirefoxProfile

class Pages(Enum):
    LOGIN = "https://secure.indeed.com/auth?continue=https%3A%2F%2Fprofile.indeed.com%2Fresume"
    RESUME = "https://profile.indeed.com/resume"


def indeed_sync():
    driver = webdriver.Firefox()
    driver.get(Pages.LOGIN.value)


if __name__ == "__main__":
    indeed_sync()
