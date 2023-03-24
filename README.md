## Olx scraper
This Olx scraper is made with BeautifulSoup. It extracts the details of each item and stores them into a PostgreSQL database. 
Both async and traditional approaches to website parsing were used.

### Tools and libraries used in the project:
- BeautifulSoup
- aiohttp and asyncio for asynchronous parsing
- requests for synchronous parsing
- psycopg2 for interaction with the database

### To run the project
Windows:
- clone the projects `https://github.com/mamontoboi/olx_scraper_bs4.git`
- cd `olx_scraper_bs4`
- `python -m venv venv`
- `.\venv\Scripts\activate`
- `pip install -r requirements.txt`
- `python main.py`

Linux:
- clone the projects `https://github.com/mamontoboi/olx_scraper_bs4.git`
- cd `olx_scraper_bs4`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python3 main.py`
