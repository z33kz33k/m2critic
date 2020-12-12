"""

    m2critic.url
    ~~~~~~~~~~~~

    Build an URL for scraping.

    @author: z33k

"""
from enum import Enum
import itertools
from typing import Generator, Optional, Union


class Platform(Enum):
    PC = "pc"
    PLAYSTATION_4 = "playstation-4"
    PLAYSTATION_5 = "playstation-5"
    XBOX_ONE = "xbox-one"
    XBOX_SERIES_X = "xbox-series-x"
    SWITCH = "switch"
    STADIA = "stadia"
    IOS = "ios"


class UserReviewsUrlBuilder:
    """Generate user reviews URLs for scraping.
    """
    BASEURL_PREFIX = "https://www.metacritic.com/"
    BASEURL_SUFFIX = "user-reviews"
    PAGESTR = "?page="

    def __init__(self, is_paginated: bool = True) -> None:
        self.is_paginated = is_paginated
        self.url: Optional[Union[str, Generator[str, None, None]]] = None

    # middle is determined in derived classes
    def _geturl(self, middle: str) -> Union[str, Generator[str, None, None]]:
        prefix = self.BASEURL_PREFIX + middle
        if self.is_paginated:
            return (f"{prefix}{self.BASEURL_SUFFIX}{self.PAGESTR}{i}" for i in itertools.count())
        return f"{prefix}{self.BASEURL_SUFFIX}"


class GameUserReviewsUrlBuilder(UserReviewsUrlBuilder):
    """Generate game user reviews URLs for scraping.
    """
    def __init__(self, platform: Platform, url_game_name: str, is_paginated: bool = True) -> None:
        super().__init__(is_paginated)
        self.url = self._geturl(middle=f"game/{platform.value}/{url_game_name}/")
        self.platform, self.url_game_name = platform, url_game_name


class UserReviewsPageParser:
    """Parse user reviews page for user names.
    """
    def __init__(self) -> None:
        ...

