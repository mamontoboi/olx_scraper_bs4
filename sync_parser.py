"""This module provides a traditional synchronous web scraper that collects data
from a website and saves it in a PostgreSQL database. The scraper uses requests
and BeautifulSoup libraries to fetch and parse web pages, and the db_postgres module
to handle database operations."""

import re
import datetime
import requests
from bs4 import BeautifulSoup
from db_postgres import DBManagement


class SyncScraper:
    """A web scraper that extracts data from a specified URL and saves it to
    a PostgreSQL database.
    """

    def __init__(self):
        self.url = input("Provide url: ")

    def count_sync_pages(self):
        """Retrieves the number of pages to be scraped from the URL and generates a list of URLs to scrape."""

        response = requests.get(self.url + '?page=1', timeout=5)
        soup = BeautifulSoup(response.text, "lxml")
        pages = soup.find_all('a', class_="css-1mi714g")[-1].text
        urls = [self.url + '?page=' + str(page_number) for page_number in range(1, int(pages) + 1)]
        return urls

    def work_with_db(self, values):
        """Creates a PostgreSQL database and table, and inserts the scraped data into the table."""

        database = DBManagement()
        database.create_db()
        database.create_table()
        database.insert_values(values)
        print("DB ops completed.")

    def date_converter(self, text):
        """Looks for date in text and returns date in datetime format."""

        date = re.search(r'\s(2[0-2]\d{2}|19[7-9]\d)', text)
        if date:
            year = date.group(1)
            year = datetime.datetime.strptime(year, '%Y').date()
        else:
            year = datetime.date(9999, 1, 1)

        return year

    def price_converter(self, text):
        """Looks for price in text and returns it as an integer."""

        num_price = re.findall(r'(\d[\d\s]*)\s*[A-z]+', text)
        if num_price:
            price = int(num_price[0].replace(' ', ''))
        else:
            price = 0
        return price

    def date_posted(self, date):
        """Processes date field. Converts relational days description into dates."""

        month_names = {
            "stycznia": "January",
            "lutego": "February",
            "marca": "March",
            "kwietnia": "April",
            "maja": "May",
            "czerwca": "June",
            "lipca": "July",
            "sierpnia": "August",
            "września": "September",
            "października": "October",
            "listopada": "November",
            "grudnia": "December"
        }

        today_keywords = ["today", "сегодня", "dzisiaj", "сьогодні"]
        if any(keyword in date.lower() for keyword in today_keywords):
            date_posted = datetime.datetime.now().date()
        else:
            date_posted = re.findall(r"\d{1,2}\s\w+\s\d{4}", date)[0]
            for month_pl, month_en in month_names.items():
                date_posted = date_posted.replace(month_pl, month_en)
            date_posted = datetime.datetime.strptime(date_posted, "%d %B %Y").date()

        return date_posted


    def get_data(self):
        """Parses the list of urls. Extracts the data and forwards it to db management method."""

        urls = self.count_sync_pages()
        values = []
        for url in urls:
            response = requests.get(url, timeout=5)
            print(url)
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.find_all('div', class_="css-1venxj6")
            for item in items:
                description = item.find('h6', class_="css-16v5mdi er34gjf0").text.strip()
                year = self.date_converter(description)
                price = item.find('p', class_="css-10b0gli er34gjf0").text.strip()
                price = self.price_converter(price)
                location_date = item.find('p', class_="css-veheph er34gjf0").text
                if location_date:
                    location_date = re.match(r'(.+) - (.+)$', location_date)
                location = location_date.group(1)
                date_posted = location_date.group(2)
                date_posted = self.date_posted(date_posted)
                values.append((description, year, location, price, date_posted))

        self.work_with_db(values)


def sync_main():
    """Initializes the instance of SyncScraper."""

    scraper = SyncScraper()
    scraper.get_data()
