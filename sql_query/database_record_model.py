# -*- coding: utf-8 -*-


"""

model container for sql database record

"""

from collections import namedtuple


class User(namedtuple):
    id: int
    username: str
    age: int
    address: str
    mobile: str
