"""

    m2critic.scrape
    ~~~~~~~~~~~~~~~

    Scrape page.

    @author: z33k

"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from bs4 import BeautifulSoup
from bs4.element import Tag


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


class PageParser:  # abstract
    """Abstract page parser.
    """
    def __init__(self, markup: str) -> None:
        self._markup = markup


class UserReviewsPageParser(PageParser):
    """Parse user reviews page for user names.
    """
    def __init__(self, markup: str) -> None:
        super().__init__(markup)
        self.users: List[BasicUser] = self._parse()

    @staticmethod
    def _pre_filter(tag: Tag) -> bool:
        """Pre-filter soup search for relevant 'li' elements.
        """
        id_ = tag.get("id")
        class_ = tag.get("class")
        return tag.name == "li" and id_ and class_ and all("user_review" in a
                                                           for a in (id_, class_))

    @staticmethod
    def _filter_score(tag: Tag) -> bool:
        """Filter relevant 'li' element for user score.
        """
        class_ = tag.get("class")
        return tag.name == "div" and class_ and "metascore_w" in class_

    @staticmethod
    def _filter_name(tag: Tag) -> bool:
        """Filter relevant 'li' element for user name.
        """
        href = tag.get("href")
        return tag.name == "a" and href and "/user/" in href

    def _parse(self) -> List[BasicUser]:
        """Parse input markup for user name and user score coupled in basic struct.
        """
        users = []
        soup = BeautifulSoup(self._markup, "lxml")
        elements = soup.find_all(self._pre_filter)
        for element in elements:
            result = element.find(self._filter_name)
            name = result.text
            result = element.find(self._filter_score)
            score = int(result.text)
            users.append(BasicUser(name, score))

        return users


class UserPageParser(PageParser):
    """Parse user page for ratings and reviews counts.
    """
    def __init__(self, markup: str) -> None:
        super().__init__(markup)
        self.ratingscount, self.reviewscount = self._parse()

    @staticmethod
    def _filter_ratingscount(tag: Tag) -> bool:
        """Filter soup for ratings 'span' element.
        """
        class_ = tag.get("class")
        return tag.name == "span" and class_ and "total_summary_ratings" in class_

    @staticmethod
    def _filter_reviewscount(tag: Tag) -> bool:
        """Filter soup for reviews 'span' element.
        """
        class_ = tag.get("class")
        return tag.name == "span" and "total_summary_reviews" in class_

    @staticmethod
    def _filter_data(tag: Tag) -> bool:
        """Filter relevant 'span' element for data.
        """
        return tag.name == "span"

    def _parse(self) -> Tuple[int, int]:
        """Parse input markup for user name and user score coupled in basic struct.
        """
        soup = BeautifulSoup(self._markup, "lxml")
        result = soup.find(self._filter_ratingscount)
        newresult = result.find(self._filter_data)
        ratingscount = int(newresult.text)
        result = soup.find(self._filter_reviewscount)
        newresult = result.find(self._filter_data)
        reviewscount = int(newresult.text)

        return ratingscount, reviewscount

