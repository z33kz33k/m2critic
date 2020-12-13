"""

    m2critic.url
    ~~~~~~~~~~~~

    Build an URL for scraping.

    @author: z33k

"""
import itertools
from typing import Generator, Optional, Union

from m2critic import GamingPlatform

PREFIX = "https://www.metacritic.com/"


class UserReviewsUrlBuilder:
    """Generate user reviews URLs for scraping.
    """
    SUFFIX = "user-reviews"
    PAGESTR = "?page="

    def __init__(self, start: Optional[int] = None, stop: Optional[int] = None) -> None:
        self.start, self.stop = start, stop
        self.start = 0 if start is None and stop is not None else start
        self.urls: Optional[Union[str, Generator[str, None, None]]] = None

    # middle is determined in derived classes
    def _geturls(self, middle: str) -> Union[str, Generator[str, None, None]]:
        """Get URL.
        """
        prefix = PREFIX + middle
        if self.start is None and self.stop is None:
            counter = itertools.count()
        elif self.stop is not None:
            counter = range(self.start, self.stop)
        else:
            counter = itertools.count(self.start)
        return (f"{prefix}{self.SUFFIX}{self.PAGESTR}{i}" for i in counter)


class GameUserReviewsUrlBuilder(UserReviewsUrlBuilder):
    """Generate game user reviews URLs for scraping.

    Example (paginated): https://www.metacritic.com/game/pc/cyberpunk-2077/user-reviews?page=0
    """
    def __init__(self, platform: GamingPlatform, url_game_name: str,
                 start: Optional[int] = None, stop: Optional[int] = None) -> None:
        super().__init__(start, stop)
        self.urls = self._geturls(middle=f"game/{platform.value}/{url_game_name}/")
        self.platform, self.url_game_name = platform, url_game_name


def get_user_url(username: str) -> str:
    """Get user page's URL.
    """
    return f"{PREFIX}user/{username}"

