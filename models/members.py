# from .helpers import wd_connect
from .helpers.db_connect import Base, engine, Session, reset_table
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from sqlalchemy import Column, String, Integer
import time


class Alderperson(Base):
    """Table of past and present city council members."""

    __tablename__ = "alderpersons"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        """Class constructor: id, name"""

        self.name = name

    def __repr__(self):
        """Represent alderperson object as <id, name>"""

        alderperson = self
        return f"<Alderperson {alderperson.id} {alderperson.name}>"

    @classmethod
    def fetch_members(cls, driver):
        """Fetch council members from City Clerk site and add <id, name> of members to Alderperson table."""

        members = []
        url = "https://chicago.legistar.com/People.aspx"
        # driver = wd_connect.start_webdriver()

        try:
            driver.get(url)
            time.sleep(1)

            # Select "all" from view menu
            view_btn = driver.find_element_by_xpath(
                "//*[@id='ctl00_ContentPlaceHolder1_menuPeople']/ul/li[4]/a"
            )
            view_btn.click()
            time.sleep(1)

            # Select "page 1" from view menu
            webdriver.ActionChains(driver).send_keys(Keys.ARROW_DOWN).send_keys(
                Keys.ARROW_DOWN
            ).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
            page1_members = driver.find_elements_by_xpath(
                "//*[contains(@id,'_hypPerson')]"
            )
            for member in page1_members:
                members.append(member.text)

            # Select "page 2" from view menu
            page2 = driver.find_element_by_xpath(
                "//*[@id='ctl00_ContentPlaceHolder1_gridPeople_ctl00']/thead/tr[1]/td/table/tbody/tr/td/div[1]/a[2]"
            )
            page2.click()
            time.sleep(1)
            page2_members = driver.find_elements_by_xpath(
                "//*[contains(@id,'_hypPerson')]"
            )
            for member in page2_members:
                members.append(member.text)
        except Exception as e:
            print(
                "Error occurred. Unable to fetch council members from City Clerk site.",
                e,
            )
        # wd_connect.quit_webdriver(driver)
        return members

    @classmethod
    def create_records(cls, members_arr):
        """Create new Alderperson row objects."""

        try:
            members = []
            for member in members_arr:
                new_member = Alderperson(name=member)
                members.append(new_member)
            return members
        except Exception as e:
            print(
                "Error occurred. Unable to create database records from members array.",
                e,
            )

    @classmethod
    def add_members_to_db(cls, records):
        """Add council members to database."""

        try:
            session = Session()
            session.query(cls).delete()
            reset_table("alderpersons")
            print("Adding council members to database...")
            session.add_all(records)
            session.commit()
            print(f"Council members added to database: {len(records)}")
            session.close()
        except Exception as e:
            print("Error occured. Unable to add records to PostgreSQL database.", e)
