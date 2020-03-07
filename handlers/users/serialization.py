# -*- coding: utf-8 -*-


"""

serialization model for postgres record

"""

from pydantic import BaseModel


# this is a json object serialization
# so you need to send json to request body
class UserSerialization(BaseModel):
    username: str
    age: int
    address: str
    mobile: str
