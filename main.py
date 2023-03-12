from bs4 import BeautifulSoup
import requests
import re
import datetime

# https://www.olx.pl/elektronika/komputery/laptopy/q-macbook-air/


def get_data(url):
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

    # response = requests.get(url)
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        # print(soup.prettify())
        items = soup.find_all('div', class_="css-1venxj6")
        for item in items:
            description = item.find('h6', class_="css-16v5mdi er34gjf0").text.strip()
            price = item.find('p', class_="css-10b0gli er34gjf0").text
            location_date = item.find('p', class_="css-veheph er34gjf0").text
            location_date = re.match(r'(.+) - (.+)$', location_date)
            location = location_date.group(1)
            date = location_date.group(2)
            today_keywords = ["today", "сегодня", "dzisiaj", "сьогодні"]
            if any(keyword in date.lower() for keyword in today_keywords):
                date = datetime.datetime.now().date()
                date = datetime.datetime.strftime(date, "%Y-%m-%d")
            else:
                date = re.findall(r"\d{1,2}\s\w+\s\d{4}", date)[0]
                for month_pl, month_en in month_names.items():
                    date = date.replace(month_pl, month_en)
                date = datetime.datetime.strptime(date, "%d %B %Y")
                date = datetime.datetime.strftime(date, "%Y-%m-%d")

            print(f"Model: {description},\n\tprice: {price}, \n\tlocation: {location},\n\tposted on: {date}")


if __name__ == '__main__':
    # user_url = input("Provide url: ")
    get_data('https://www.olx.pl/elektronika/komputery/laptopy/q-macbook-air/')