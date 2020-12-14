"""

    m2critic.scrape
    ~~~~~~~~~~~~~~~

    Scrape Metacritic pages.

    @author: z33k

"""
import time
from pprint import pprint
from typing import List

import requests

from m2critic import BasicUser, User, GamingPlatform
from m2critic.url import GameUserReviewsUrlBuilder, get_user_url
from m2critic.parse import UserReviewsPageParser, UserPageParser, RequestBlockedError
from m2critic.utils import getdelay, countdown

MAX_BLOCKS_COUNT = 20
REVIEW_LATENCY_BASE, REVIEW_LATENCY_OFFSET = 5.0, 4.5
MINOR_USER_LATENCY_BASE, MINOR_USER_LATENCY_OFFSET = 1.0, 0.7
USER_LATENCY_BASE, USER_LATENCY_OFFSET = 90, 30
MAJOR_USER_LATENCY_BASE, MAJOR_USER_LATENCY_OFFSET = 450, 30
# using this trick:
# https://stackoverflow.com/questions/34643822/accessing-metacritic-api-and-or-scraping
# to avoid getting 403 Forbidden error
HEADERMAP = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/87.0.4280.88 Safari/537.36",
             "Referer": "https://www.metacritic.com/"}


def scrape_pcgame_user_reviews(url_game_name: str) -> List[BasicUser]:
    """Scrape PC game user reviews page for list of BasicUser structs.
    """
    builder = GameUserReviewsUrlBuilder(GamingPlatform.PC, url_game_name)
    users = []
    print(f"Scraping user data from user reviews pages for game: '{url_game_name}' started...")
    for i, url in enumerate(builder.urls, start=1):
        markup = requests.get(url, headers=HEADERMAP).text
        try:
            scraped_users = UserReviewsPageParser(markup).users[:]
        except ValueError:  # too high page index has been hit
            break
        users += scraped_users
        print(f"\n{'*' * 10} Users batch #{i} {'*' * 10}\n")
        pprint(scraped_users)
        latency = getdelay(REVIEW_LATENCY_BASE, REVIEW_LATENCY_OFFSET)
        print(f"\nWaiting for {latency:.2f}s to not get blocked...")
        time.sleep(latency)

    return users


def scrape_users(basic_users: List[BasicUser]) -> List[User]:
    """Scrape user pages for list of User objects.
    """
    def major_delay(base: int, offset: int) -> None:
        delay = getdelay(base, offset)
        print(f"\nDelaying server request for {delay} seconds...")
        countdown(delay)
        print()

    users = []
    print(f"Scraping user data from {len(basic_users)} user pages started...")
    for i, basic_user in enumerate(basic_users, start=1):
        markup = requests.get(get_user_url(basic_user.name), headers=HEADERMAP).text
        parser = None
        counter = 0
        while True:
            try:
                parser = UserPageParser(markup)
            except RequestBlockedError:
                if counter > MAX_BLOCKS_COUNT:
                    break
                print("*** Server has blocked requests! ***")
                major_delay(MAJOR_USER_LATENCY_BASE, MAJOR_USER_LATENCY_OFFSET)
                counter += 1
                continue
            break

        if not parser:
            raise ValueError("Nothing to parse. Server is blocking requests.")
        user = User(basic_user.name, basic_user.score, parser.ratingscount, parser.reviewscount)
        users.append(user)
        print(f"Scraped user #{i} '{user}'")
        if i % 200 == 0:
            major_delay(USER_LATENCY_BASE, USER_LATENCY_OFFSET)
        else:
            latency = getdelay(MINOR_USER_LATENCY_BASE, MINOR_USER_LATENCY_OFFSET)
            time.sleep(latency)

    return users

