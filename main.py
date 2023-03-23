"""The module contains the main UI of the parser. It allows the user to
 choose the method of parsing (sync and async) and select the initial URL."""

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
