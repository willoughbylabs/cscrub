import re
from models.helpers import wd_connect
from models.legislation import Legislation
from .helpers.db_connect import Base, engine, Session, reset_table
from selenium.webdriver.common.by import By
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
    def fetch_and_format_votes(cls, links_list):
        """Fetch votes for legislation."""

        driver = wd_connect.start_webdriver()

        def fetch_action_detail_links(links_list):
            """Fetch action detail links for each legislation in a meeting."""

            def extract_link(string):
                """Extract a portion of a link from an onclick string. Returns a string."""

                text = re.search("\('(.+?)',", string)
                return text.group(1)

            def prefix_links(links_arr):
                """Given an array of link fragments, prefixes the links with a domain."""

                links_with_domains = []
                domain = "https://chicago.legistar.com/"
                for link_fragment in links_arr:
                    link = domain + link_fragment
                    links_with_domains.append(link)
                return links_with_domains

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
            action_detail_links = prefix_links(action_detail_fragments)
            return action_detail_links

        def fetch_votes(links_arr):
            """Given a list of links to a legislation's votes, fetch member name and casting vote."""

            def extract_members(elements):
                """Given a list of web elements, extracts and returns list of council members' names."""

                members = []
                for e in elements:
                    member = e.text
                    members.append(member)
                return members

            def extract_votes(elements):
                """Given a list of elements, extract and return a list of votes from the sibling element."""

                votes = []
                for td in elements:
                    vote = td.find_element(By.XPATH, "./following-sibling::td").text
                    votes.append(vote)
                return votes

            def format_votes(record_num, members, votes):
                """Given a record_num (string), members (list), and votes (list), return a list of formatted dictionaries."""

                print(f"Formatting votes for legislation record {record_num}.")
                formatted_votes = []
                for i in range(len(votes)):
                    vote = {
                        "record_num": record_num,
                        "name": members[i],
                        "vote": votes[i],
                    }
                    formatted_votes.append(vote)
                return formatted_votes

            formatted_votes = []
            for link in links_arr:
                try:
                    driver.get(link)
                    record_num = driver.find_element(
                        By.XPATH, "//*[contains(@id,'_hypFile')]"
                    ).text
                    member_els = driver.find_elements(
                        By.XPATH, "//*[contains(@id,'_hypPerson')]"
                    )
                    if len(member_els) == 0:
                        print(
                            f"No votes for legislation record number {record_num}. Skipping..."
                        )
                        continue
                    td_els = driver.find_elements(
                        By.CSS_SELECTOR, "td[style='white-space:nowrap;']"
                    )
                    members = extract_members(member_els)
                    votes = extract_votes(td_els)
                    formatted_votes += format_votes(record_num, members, votes)

                except Exception as e:
                    print(
                        f"Unable to fetch votes for legistion record number {record_num}.",
                        e,
                    )
            return formatted_votes

        action_detail_links = fetch_action_detail_links(links_list)
        votes = fetch_votes(action_detail_links)
        wd_connect.quit_webdriver(driver)
        return votes

    @classmethod
    def create_records(cls, entries):
        """Create new Votes rows."""

        votes = []
        for vote in entries:
            new_vote = Vote(
                record_num=vote["record_num"],
                name=vote["name"],
                vote=vote["vote"],
            )
            votes.append(new_vote)
        return votes

    @classmethod
    def add_votes_to_db(cls, records):
        """Add vote records to database."""

        try:
            session = Session()
            session.query(cls).delete()
            reset_table("votes")
            print("Adding votes to database...")
            session.add_all(records)
            session.commit()
            session.close()
            print(f"{len(records)} vote(s) added to database.")
        except Exception as e:
            print("Error occurred. Unable to add votes to the database.", e)
