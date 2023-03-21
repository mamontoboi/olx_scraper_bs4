"""The module contains two functions, serving the same purpose: parsing of olx website. First """

import asyncio
from async_parser import async_main
from sync_parser import sync_main


if __name__ == '__main__':

    # 'https://www.olx.pl/elektronika/komputery/laptopy/q-macbook-air/'

    choice = input("Press 1 for traditional solution\nPress 2 for asynchronous solution\n")
    match choice:
        case '1':
            sync_main()
        case '2':
            asyncio.run(async_main())
