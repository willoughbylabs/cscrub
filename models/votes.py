import re

from requests import session
from models.helpers import wd_connect
from models.legislation import Legislation
from .helpers.db_connect import Base, engine, Session, reset_index
from sqlalchemy import Column, Integer, String, extract


class Vote(Base):
    """Table of city council members' votes on legislation."""

    __tablename__ = "votes"

    id = Column(Integer, autoincrement=True, primary_key=True)
    record_num = Column(String)
    name = Column(String)
    vote = Column(String)

    def __init__(self, record_num, name, vote):
        """Class constructor: record_num, name, vote."""

        self.record_num = record_num
        self.name = name
        self.vote = vote

    def __repr__(self):
        """Represent vote object as <id, name, vote>."""

        vote = self
        return f"<Vote {vote.record_num} {vote.name} {vote.vote}>"

    @classmethod
    def fetch_votes(cls, links_list):
        """Fetch votes for legislation."""

        driver = wd_connect.start_webdriver()

        def fetch_action_detail_links(links_list):
            """Fetch action detail links for each legislation in a meeting."""

            def extract_link(string):
                """Extract a portion of a link from an onclick string. Returns a string."""

                text = re.search("\('(.+?)',", string)
                return text.group(1)

            action_detail_fragments = []
            for link in links_list:
                try:
                    driver.get(link)
                    action_details = driver.find_elements_by_xpath(
                        "//*[contains(@id,'_hypDetails')]"
                    )
                    for detail in action_details:
                        onclick = detail.get_attribute("onclick")
                        link_fragment = extract_link(onclick)
                        action_detail_fragments.append(link_fragment)
                except Exception as e:
                    print(
                        "Error occured. Unable to fetch action detail links from City Clerk site.",
                        e,
                    )
            wd_connect.quit_webdriver(driver)
            return action_detail_fragments

        action_detail_links = fetch_action_detail_links(links_list)
        return action_detail_links

    # @classmethod
    # def fetch_votes(cls, links):
    #     """Given a list of links to a vote result page, fetch votes of council members and returns a list with vote dictionaries."""

    #     def extract_members(elements):
    #         """Extract council members' name from selected DOM elements."""

    #         members = []
    #         for e in elements:
    #             member = e.text
    #             members.append(member)
    #         return members

    #     def extract_votes(elements):
    #         """Extract votes from the sibling of a selected element."""

    #         votes = []
    #         for td in elements:
    #             vote = td.find_element_by_xpath("./following-sibling::td").text
    #             votes.append(vote)
    #         return votes

    #     def format_votes(record_num, members, votes):
    #         """Create a dictionary for each vote's data."""

    #         print(f"Formatting votes for legislation record number {record_num}...")
    #         formatted_votes = []
    #         for i in range(len(votes)):
    #             vote = {"record_num": record_num, "name": members[i], "vote": votes[i]}
    #             formatted_votes.append(vote)
    #         return formatted_votes

    #     formatted_votes = []
    #     driver = wd_connect.start_webdriver()
    #     action_links = Legislation.fetch_action_details_links(links, driver)

    #     for link in action_links:
    #         try:
    #             driver.get(link)
    #             record_num_el = driver.find_element_by_xpath(
    #                 "//*[contains(@id,'_hypFile')]"
    #             )
    #             record_num = record_num_el.text
    #             members_el = driver.find_elements_by_xpath(
    #                 "//*[contains(@id,'_hypPerson')]"
    #             )
    #             if len(members_el) == 0:
    #                 print(
    #                     f"No votes for legislation record number {record_num}. Skipping..."
    #                 )
    #                 continue
    #             members = extract_members(members_el)
    #             td_el = driver.find_elements_by_css_selector(
    #                 "td[style='white-space:nowrap;']"
    #             )
    #             votes = extract_votes(td_el)
    #             wd_connect.quit_webdriver(driver)
    #             formatted_votes += format_votes(record_num, members, votes)
    #         except Exception as e:
    #             print(
    #                 f"Error occurred. Unable to fetch votes from result page for legislation record number {record_num}.",
    #                 e,
    #             )
    #     return formatted_votes

    # @classmethod
    # def create_records(cls, entries):
    #     """Create new Votes rows."""

    #     votes = []
    #     for vote in entries:
    #         new_vote = Vote(
    #             record_num=vote["record_num"],
    #             name=vote["name"],
    #             vote=vote["vote"],
    #         )
    #         votes.append(new_vote)
    #     return votes

    # @classmethod
    # def add_votes_to_db(cls, records):
    #     """Add vote records to database."""

    #     try:
    #         session = Session()
    #         session.query(cls).delete()
    #         reset_index("votes")
    #         print("Adding votes to database...")
    #         session.add_all(records)
    #         session.commit()
    #         session.close()
    #         print(f"{len(records)} vote(s) added to database.")
    #     except Exception as e:
    #         print("Error occurred. Unable to add votes to the database.", e)
