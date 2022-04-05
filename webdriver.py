from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time


def start_webdriver():
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    return driver


def quit_webdriver(driver):
    driver.quit()


def search_bing():
    driver = start_webdriver()

    driver.get("https://bing.com")
    time.sleep(5)
    element = driver.find_element_by_id("sb_form_q")
    element.send_keys("WebDriver")
    element.submit()
    time.sleep(5)

    quit_webdriver(driver)
