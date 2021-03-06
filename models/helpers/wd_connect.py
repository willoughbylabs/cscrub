import feedparser
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def start_webdriver():
    print("Starting webdriver...")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    return driver


def quit_webdriver(driver):
    print("Quitting webdriver...")
    driver.quit()


def fetch_rss_entries(url, type):
    """Fetch and return entries from an RSS feed."""

    if type == "meetings":
        try:
            document = feedparser.parse(url)
            return document.entries
        except Exception as e:
            print(
                "Error occurred. Unable to fetch and parse meetings entries from RSS feed.",
                e,
            )

    if type == "legislation":
        try:
            document = feedparser.parse(url)
            feed_title = {"feed_title": document.feed.title}
            document.entries.insert(0, feed_title)
            return document.entries
        except Exception as e:
            print(
                "Error occurred. Unable to fetch and parse legislation entries from RSS feed.",
                e,
            )
