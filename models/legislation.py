from models.helpers import wd_connect
from .helpers.db_connect import Base, engine, Session
from .helpers import wd_connect
import re
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
                rss_btn = driver.find_element_by_xpath("//*[@id='ctl00_ButtonRSS']")
            except Exception as e:
                print(
                    f"Error occurred. Unable to fetch legislation from City Clerk RSS feed. \nLink at index {index} may be incorrect:\n{link}\nSkipping link.",
                    e,
                )
                continue
            try:
                rss_btn.click()
                driver.switch_to.window(driver.window_handles[-1])
                url = driver.current_url
                entries = wd_connect.fetch_rss_entries(url, "legislation")
                if entries[1].title == "No records":
                    print(
                        "No legislation entries found for this meeting date. Continuing to next meeting(s)."
                    )
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                    continue
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
                legislation_entries.append(entries)
            except Exception as e:
                print(
                    "Error occurred. Unable to parse legislation entries from City Clerk RSS feed.",
                    e,
                )
                continue

        wd_connect.quit_webdriver(driver)
        return legislation_entries

    @classmethod
    def create_records(cls, entries):
        """Create new Legislation row objects."""

        def format_rss_entries(entries_arr):
            """Accepts list of RSS entries and returns list of formatted dictionaries."""

            def get_date_from_title(title):
                """Accepts a string, 'title', and splits on each hyphen to extract the meeting date. Returns meeting date."""

                match = re.search("\d{1,2}/\d{1,2}/\d{4}", title)
                return match.group()

            def other_keys(summary):
                """Extracts 'title', 'result', and 'action_text' from rss entry summary."""

                title = re.search("<br />Title:(.+?)<br />", summary)
                if title:
                    title = title.group(1).strip()
                action = re.search("<br />Action:(.+?)<br />", summary)
                if action:
                    action = action.group(1).strip()
                result = re.search("<br />Result:(.*)", summary)
                if result:
                    result = result.group(1).strip()
                other_keys = {"title": title, "result": result, "action_text": action}
                return other_keys

            formatted_entries = []
            for leg_per_mtg in entries_arr:
                mtg_title = leg_per_mtg[0]["feed_title"]
                date = get_date_from_title(mtg_title)
                leg_per_mtg.pop(0)
                for leg in leg_per_mtg:
                    formatted_entry = {}
                    formatted_entry["mtg_date"] = date
                    formatted_entry["record_num"] = leg.title
                    formatted_entry["type"] = leg.tags[0].term
                    other_entries = other_keys(leg.summary)
                    formatted_entry.update(other_entries)
                    formatted_entries.append(formatted_entry)
            return formatted_entries

        records = format_rss_entries(entries)
        return records
