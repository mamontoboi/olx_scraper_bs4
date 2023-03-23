import requests
import re
import datetime
from bs4 import BeautifulSoup
from db_postgres import DBManagement


class SyncScraper:
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

    def __init__(self):
        self.url = input("Provide url: ")

    def count_sync_pages(self):
        response = requests.get(self.url + '?page=1')
        soup = BeautifulSoup(response.text, "lxml")
        pages = soup.find_all('a', class_="css-1mi714g")[-1].text
        urls = [self.url + '?page=' + str(page_number) for page_number in range(1, int(pages) + 1)]
        return urls

    def work_with_db(self, values):
        database = DBManagement()
        database.create_db()
        database.create_table()
        database.insert_values(values)
        print("DB ops completed.")

    def get_data(self):
        urls = self.count_sync_pages()
        values = []
        for url in urls:
            response = requests.get(url)
            print(url)
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.find_all('div', class_="css-1venxj6")
            for item in items:
                description = item.find('h6', class_="css-16v5mdi er34gjf0").text.strip()
                date = re.search(r'\s(2[0-2]\d{2}|19[7-9]\d)', description)
                if date:
                    year = date.group(1)
                    year = datetime.datetime.strptime(year, '%Y').date()
                else:
                    year = datetime.date(9999, 1, 1)
                price = item.find('p', class_="css-10b0gli er34gjf0").text.strip()
                num_price = re.findall(r'(\d[\d\s]*)\s*[A-z]+', price)
                if num_price:
                    price = int(num_price[0].replace(' ', ''))
                else:
                    price = 0
                location_date = item.find('p', class_="css-veheph er34gjf0").text
                if location_date:
                    location_date = re.match(r'(.+) - (.+)$', location_date)
                location = location_date.group(1)
                date_posted = location_date.group(2)
                today_keywords = ["today", "сегодня", "dzisiaj", "сьогодні"]
                if any(keyword in date_posted.lower() for keyword in today_keywords):
                    date_posted = datetime.datetime.now().date()
                else:
                    date_posted = re.findall(r"\d{1,2}\s\w+\s\d{4}", date_posted)[0]
                    for month_pl, month_en in SyncScraper.month_names.items():
                        date_posted = date_posted.replace(month_pl, month_en)
                    date_posted = datetime.datetime.strptime(date_posted, "%d %B %Y").date()
                values.append((description, year, location, price, date_posted))

        self.work_with_db(values)


def sync_main():
    scraper = SyncScraper()
    scraper.get_data()
