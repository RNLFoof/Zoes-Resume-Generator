import ahk
from enum import Enum
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Pages(Enum):
    SEARCH = "https://ca.indeed.com/jobs?q=developer&l=Remote&from=searchOnHP&vjk=55a2ec28ca868a2d"


def indeed_scrape():
    driver = webdriver.Firefox()
    driver.get(Pages.SEARCH.value)
    job_a_elements: list[WebElement] = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '[class*="JobTitle"]'))
    )
    job_links: list[str] = [a.get_property("href") for a in job_a_elements]
    breakpoint()


if __name__ == "__main__":
    indeed_scrape()
