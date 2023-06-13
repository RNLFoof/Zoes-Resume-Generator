from enum import Enum

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import FirefoxProfile
import ahk
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Pages(Enum):
    LOGIN = "https://secure.indeed.com/auth?continue=https%3A%2F%2Fprofile.indeed.com%2Fresume"
    RESUME = "https://profile.indeed.com/resume"


def indeed_sync():
    print("What is password???")
    password = input()

    driver = webdriver.Firefox()
    driver.get(Pages.LOGIN.value)

    email_input = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'input[name="__email"]'))
    )
    email_input.send_keys("z.zablotsky@gmail.com")

    submit_button = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    submit_button.click()

    password_instead_anchor = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.LINK_TEXT, 'Log in with a password instead'))
    )
    password_instead_anchor.click()

    password_input = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'input[name="__password"]'))
    )
    password_input.send_keys(password)

    submit_button = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    submit_button.click()

    # Logs in using KeepPass password manager
    # Autotype sequence is {USERNAME}{ENTER}{DELAY 1000}{TAB}{TAB}{TAB}{TAB}{ENTER}{PASSWORD}{ENTER}
    # ahk.send_input("^!a")
    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'input[name="__email"]'))
    #     )
    # except TimeoutException as e:
    #     raise ExceptionGroup("Never logged into Indeed. Is KeePass open and configured correctly?", [e])


if __name__ == "__main__":
    indeed_sync()
