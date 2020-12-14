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
__version__ = "0.1.6.dev0"
__description = f"{__name__} is a script that scrapes metacritic.com for user data and " \
                f"user ratings and then calculated a new cumulative rating that isn't a mundane " \
                f"average but rather a weighted arithmetic mean where weights are based on " \
                f"grokked user cred."


class Rating(Enum):
    NEGATIVE = (0, 4)
    MIXED = (5, 7)
    POSITIVE = (8, 10)


@dataclass
class BasicUser:
    name: str
    score: int

    @property
    def rating(self) -> Rating:
        if self.score in range(5):
            return Rating.NEGATIVE
        elif self.score in range(5, 8):
            return Rating.MIXED
        return Rating.POSITIVE


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

    def __repr__(self) -> str:
        result = f"{type(self).__name__}("
        result += f"name='{self.name}', "
        result += f"score='{self.score}', "
        result += f"cred={self.cred})"
        return result


class GamingPlatform(Enum):
    PC = "pc"
    PLAYSTATION_4 = "playstation-4"
    PLAYSTATION_5 = "playstation-5"
    XBOX_ONE = "xbox-one"
    XBOX_SERIES_X = "xbox-series-x"
    SWITCH = "switch"
    STADIA = "stadia"
    IOS = "ios"
