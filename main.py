"""

    Meta-metacritic - re-weigh ratings based on user cred.

    @author: z33k

"""
from pathlib import Path
from pprint import pprint

from m2critic.url import GameUserReviewsUrlBuilder, Platform
from m2critic.scrape import UserReviewsPageParser, UserPageParser


def run():
    # builder = GameUserReviewsUrlBuilder(Platform.PC, "cyberpunk-2077")
    # print("URL is: ", next(builder.url))
    # pprint(f"Length: {len(read_html())}")
    # pprint(f"Name: {read_html()}")
    # source = Path("data/user_reviews.html")
    # parser = UserReviewsPageParser(source.read_text())
    # pprint(parser.users)
    source = Path("data/user.html")
    parser = UserPageParser(source.read_text())
    print(f"ratings count: {parser.ratingscount}, reviews count: {parser.reviewscount}")


if __name__ == '__main__':
    run()
