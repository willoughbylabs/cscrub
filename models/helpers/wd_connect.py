from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time


def start_webdriver():
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    return driver


def quit_webdriver(driver):
    driver.quit()


def search_bing():
    driver = start_webdriver()
    driver.implicitly_wait(10)
    driver.get("https://bing.com")
    element = driver.find_element_by_id("sb_form_q")
    element.send_keys("WebDriver")
    element.submit()
    time.sleep(5)

    quit_webdriver(driver)
