"""

    m2critic.debug
    ~~~~~~~~~~~~~~~

    Debug functions.

    @author: z33k

"""
from pathlib import Path
from typing import List

from m2critic import BasicUser


def read_basic_users(filepath: Path) -> List[BasicUser]:
    """Read BasicUser structs from filepath.
    """
    users = []
    with filepath.open() as f:
        for line in f:
            users.append(eval(line))

    return users
