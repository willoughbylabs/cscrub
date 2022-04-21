import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")


driver = webdriver.Chrome(
    executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options
)

url = "https://chicago.legistar.com/People.aspx"
driver.get(url)
view_btn = driver.find_element(
    By.XPATH, "//*[@id='ctl00_ContentPlaceHolder1_menuPeople']/ul/li[4]/a"
)
print(view_btn)
view_btn.click()
time.sleep(1)

driver.quit()

print("Finished!")
