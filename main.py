import time
import os
import uvicorn
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By

# WEBDRIVER CONFIGURATIONS
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

# APP CONFIGURATIONS
fetch_data = True

# APP
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def run_app():
    """Run CScrub bot and API with the set configurations."""

    if fetch_data:
        fetch_data()


def fetch_data():
    """Fetch data from the Chicago City Clerk site using the CScrub bot."""

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
    print("Finished! Data fetched.")


run_app()
uvicorn.run("main:app")
