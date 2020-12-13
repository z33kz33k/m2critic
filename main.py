"""

    Meta-metacritic - re-weigh ratings based on user cred.

    @author: z33k

"""
from pathlib import Path
from pprint import pprint

from m2critic.url import GameUserReviewsUrlBuilder
from m2critic import GamingPlatform
from m2critic.parse import UserReviewsPageParser, UserPageParser
from m2critic.scrape import scrape_pcgame_user_reviews


def run():
    # builder = GameUserReviewsUrlBuilder(Platform.PC, "cyberpunk-2077")
    # print("URL is: ", next(builder.url))
    # pprint(f"Length: {len(read_html())}")
    # pprint(f"Name: {read_html()}")
    # source = Path("debug/input/user_reviews.html")
    # parser = UserReviewsPageParser(source.read_text())
    # pprint(parser.users)
    # source = Path("debug/input/user.html")
    # parser = UserPageParser(source.read_text())
    # print(f"ratings count: {parser.ratingscount}, reviews count: {parser.reviewscount}")
    file = Path("debug/output/cyberpunk_2077_basic_users.txt")
    users = scrape_pcgame_user_reviews("cyberpunk-2077")
    file.write_text("\n".join(str(u) for u in users), encoding="utf-8")


if __name__ == '__main__':
    run()
