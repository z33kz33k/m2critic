"""

    m2critic.scrape
    ~~~~~~~~~~~~~~~

    Scrape Metacritic pages.

    @author: z33k

"""
import random
import time
from pprint import pprint
from typing import List

import requests

from m2critic import BasicUser, User, GamingPlatform
from m2critic.url import GameUserReviewsUrlBuilder
from m2critic.parse import UserReviewsPageParser, UserPageParser


LATENCY_FLOOR, LATENCY_CEILING = 0.03, 10.0


def scrape_pcgame_user_reviews(url_game_name: str) -> List[BasicUser]:
    """Scrape PC game user reviews page for list of BasicUser structs.
    """
    builder = GameUserReviewsUrlBuilder(GamingPlatform.PC, url_game_name)
    users = []
    print(f"Scraping user data from user reviews pages for game: '{url_game_name}' started...")
    for i, url in enumerate(builder.urls, start=1):
        # using this trick:
        # https://stackoverflow.com/questions/34643822/accessing-metacritic-api-and-or-scraping
        # to avoid getting 403 Forbidden error
        headermap = {"User-Agent": "Mac Firefox"}
        markup = requests.get(url, headers=headermap).text
        try:
            scraped_users = UserReviewsPageParser(markup).users[:]
        except ValueError:  # too high page index has been hit
            break
        users += scraped_users
        print(f"\n{'*' * 10} Users batch #{i} {'*' * 10}\n")
        pprint(scraped_users)
        time.sleep(random.uniform(LATENCY_FLOOR, LATENCY_CEILING))

    return users

