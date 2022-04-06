from models.helpers import wd_connect
from .helpers.db_connect import Base, engine, Session
from .helpers import wd_connect
import time
from sqlalchemy import Column, String, Integer


class Legislation(Base):
    """Table of City Council legislation."""

    __tablename__ = "legislation"

    id = Column(Integer, autoincrement=True, primary_key=True)
    record_num = Column(String)
    type = Column(String)
    title = Column(String)
    result = Column(String)
    action_text = Column(String)
    mtg_date = Column(String)

    def __init__(self, record_num, type, title, result, action_text, mtg_date):
        """Class constructor: type, title, result, action_text, mtg_date."""

        self.record_num = record_num
        self.type = type
        self.title = title
        self.result = result
        self.action_text = action_text
        self.mtg_date = mtg_date

    def __repr__(self):
        """Represent legislation object as <id, record_num, mtg_date>."""

        legislation = self
        return f"<Legislation {legislation.id} {legislation.record_num} {legislation.mtg_date}>"

    @classmethod
    def fetch_legislation(cls, links):
        """Fetch legislation from City Clerk RSS feed."""

        legislation_entries = []
        driver = wd_connect.start_webdriver()

        for index, link in enumerate(links):
            try:
                driver.get(link)
                time.sleep(1)
                rss_btn = driver.find_element_by_xpath("//*[@id='ctl00_ButtonRSS']")
                rss_btn.click()
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])
                url = driver.current_url
                entries = wd_connect.fetch_rss_entries(url, "legislation")
                return entries
            except Exception as e:
                print(
                    f"Error occurred. Unable to fetch legislation from City Clerk RSS feeds.\nLink at index {index} may be incorrect:\n{link}\nSkipping link.",
                    e,
                )
            finally:
                wd_connect.quit_webdriver()
