from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import keyring
import re
from getpass import getpass
import random
import time

driver = webdriver.Chrome()


def wait(timeout=5):
    return WebDriverWait(driver, timeout)


def isIdPresent(name):
    return expected_conditions.presence_of_element_located((By.ID, name))


def isValidEmail(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.fullmatch(regex, email)


def newUsername():
    username = ""
    while not isValidEmail(username):
        username = input("LinkedIn Email: ")
    keyring.set_password("jobscraper", "username", username)
    return username


def getUsername():
    username = keyring.get_password("jobscraper", "username")
    if username is None:
        username = newUsername()
    return username


def newPassword():
    password = getpass()
    keyring.set_password("jobscraper", "password", password)
    return password


def getPassword():
    password = keyring.get_password("jobscraper", "password")
    if password is None:
        password = newPassword()
    return password


def search():
    xpath = '//button[text()="Search"]'
    driver.find_element_by_xpath(xpath).click()

def s():
    time.sleep(random.uniform(0.5, 1.5))
    
def main():
    driver.implicitly_wait(4)

    driver.get("https://www.linkedin.com/login")
    driver.find_element_by_id("username").send_keys(getUsername())
    driver.find_element_by_id("password").send_keys(getPassword())
    driver.find_element_by_id("password").send_keys(Keys.RETURN)
    s()
    
    driver.get("https://www.linkedin.com/jobs/")

    bars = driver.find_elements_by_class_name("jobs-search-box__text-input")
    keywordSearch = bars[0]
    locationSearch = bars[3]

    s()
    keywordSearch.send_keys("Python")
    s()
    locationSearch.send_keys("Remote")
    s()
    search()
    s()
    
    datePostedDropdown = driver.find_element_by_xpath('//*[text()="Date Posted"]')
    datePostedDropdown.click()
    s()
    today = "timePostedRange-r86400"
    driver.execute_script(f"document.getElementById('{today}').click()")
    s()
    datePostedDropdown.click()
    s()

    datePostedDropdown = driver.find_element_by_xpath('//*[text()="Job Type"]')
    datePostedDropdown.click()
    s()
    driver.execute_script("document.getElementById('jobType-F').click()")
    s()
    datePostedDropdown.click()
    s()


if __name__ == "__main__":
    main()
