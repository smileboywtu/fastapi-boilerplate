# -*- coding: utf-8 -*-


"""

serialization model for postgres record

"""

from pydantic import BaseModel, ValidationError, validator


# this is a json object serialization
# so you need to send json to request body
class UserSerialization(BaseModel):
    username: str
    age: int
    address: str
    mobile: str

    @validator("age")
    def validate_age(cls, value):
        if value < 0 or value > 200:
            raise ValidationError("age is between 0 ~ 200")
        return value
