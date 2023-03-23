import re
import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from db_postgres import DBManagement


class AsyncScraper:
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

    def work_with_db(self, values):
        database = DBManagement()
        database.create_db()
        database.create_table()
        database.insert_values(values)
        print("DB ops completed.")

    @staticmethod
    async def fetch_page(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def count_pages(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + '?page=1') as pages_count:
                soup = BeautifulSoup(await pages_count.text(), "lxml")
                pages = soup.find_all('a', class_="css-1mi714g")[-1].text
                urls = [self.url + '?page=' + str(page_number) for page_number in range(1, int(pages) + 1)]

        results = await asyncio.gather(*[self.fetch_page(url) for url in urls])
        values = []
        for page in results:
            values.extend(await self.scrap_page(page))

        self.work_with_db(values)

    @staticmethod
    async def scrap_page(response):
        soup = BeautifulSoup(response, "lxml")
        items = soup.find_all('div', class_="css-1venxj6")
        values = []
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
                for month_pl, month_en in AsyncScraper.month_names.items():
                    date_posted = date_posted.replace(month_pl, month_en)
                date_posted = datetime.datetime.strptime(date_posted, "%d %B %Y").date()
            values.append((description, year, location, price, date_posted))

        return values


async def async_main():
    scraper = AsyncScraper()
    await scraper.count_pages()
