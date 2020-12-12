"""

    Meta-metacritic - re-weigh ratings based on user cred.

    @author: z33k

"""
from m2critic.url import GameUserReviewsUrlBuilder, Platform


def run():
    builder = GameUserReviewsUrlBuilder(Platform.PC, "cyberpunk-2077")
    print("URL is: ", next(builder.url))


if __name__ == '__main__':
    run()
