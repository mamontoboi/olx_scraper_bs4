import re
import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup


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
        for page in results:
            await self.scrap_page(page)

    @staticmethod
    async def scrap_page(response):
        soup = BeautifulSoup(response, "lxml")
        items = soup.find_all('div', class_="css-1venxj6")
        for item in items:
            description = item.find('h6', class_="css-16v5mdi er34gjf0").text.strip()
            price = item.find('p', class_="css-10b0gli er34gjf0").text.strip()
            num_price = re.findall(r'(\d[\d\s]*)\s*[A-z]+', price)
            if num_price:
                price = int(num_price[0].replace(' ', ''))
            location_date = item.find('p', class_="css-veheph er34gjf0").text
            if location_date:
                location_date = re.match(r'(.+) - (.+)$', location_date)
            location = location_date.group(1)
            date = location_date.group(2)
            today_keywords = ["today", "сегодня", "dzisiaj", "сьогодні"]

            if any(keyword in date.lower() for keyword in today_keywords):
                date = datetime.datetime.now().date()
                date = datetime.datetime.strftime(date, "%Y-%m-%d")
            else:
                date = re.findall(r"\d{1,2}\s\w+\s\d{4}", date)[0]
                for month_pl, month_en in AsyncScraper.month_names.items():
                    date = date.replace(month_pl, month_en)
                date = datetime.datetime.strptime(date, "%d %B %Y")
                date = datetime.datetime.strftime(date, "%Y-%m-%d")

            print(f"Model: {description},\n\tprice: {price}, \n\tlocation: {location},\n\tposted on: {date}")


async def async_main():
    scraper = AsyncScraper()
    await scraper.count_pages()
