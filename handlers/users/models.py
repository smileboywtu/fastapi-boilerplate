# -*- coding: utf-8 -*-


"""

user orm

"""

from tortoise import fields
from tortoise.models import Model


class User(Model):
    class Meta:
        table = "users"

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32, null=False, unique=True)
    age = fields.SmallIntField()
    address = fields.CharField(max_length=256, null=False)
    mobile = fields.CharField(max_length=16)

    def __str__(self):
        return self.username
