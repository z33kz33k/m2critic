"""

    m2critic
    ~~~~~~~~~

    Meta-metacritic - re-weigh ratings based on user cred.

    @author: z33k

"""
from dataclasses import dataclass
from enum import Enum


__author__ = "z33k"
__contact__ = "zeek@int.pl"
__version__ = "0.1.5.dev0"
__description = f"{__name__} is a script that scrapes metacritic.com for user data and " \
                f"user ratings and then calculated a new cumulative rating that isn't a mundane " \
                f"average but rather a weighted arithmetic mean where weights are based on " \
                f"grokked user cred."


@dataclass
class BasicUser:
    name: str
    score: int


@dataclass
class User:
    """Metacritic user as scraped for the purposes of this script.
    """
    name: str
    score: int
    ratingscount: int
    reviewscount: int

    @property
    def cred(self) -> int:
        return self.reviewscount * 2 + self.ratingscount


class GamingPlatform(Enum):
    PC = "pc"
    PLAYSTATION_4 = "playstation-4"
    PLAYSTATION_5 = "playstation-5"
    XBOX_ONE = "xbox-one"
    XBOX_SERIES_X = "xbox-series-x"
    SWITCH = "switch"
    STADIA = "stadia"
    IOS = "ios"
