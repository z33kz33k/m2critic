"""

    Meta-metacritic - re-weigh ratings based on user cred.

    @author: z33k

"""
from pathlib import Path
from pprint import pprint

from m2critic.url import GameUserReviewsUrlBuilder, Platform
from m2critic.scrape import UserReviewsPageParser


def run():
    # builder = GameUserReviewsUrlBuilder(Platform.PC, "cyberpunk-2077")
    # print("URL is: ", next(builder.url))
    # pprint(f"Length: {len(read_html())}")
    # pprint(f"Name: {read_html()}")
    source = Path("data/example.html")
    parser = UserReviewsPageParser(source.read_text())
    pprint(parser.users)


if __name__ == '__main__':
    run()
