# -*- coding: utf-8 -*-

"""

manager user information

see more information about how fast api parse path params, query params, body params

you need to define path params first and query params, then define body params as pydantic model

recommend way: define path params use Path, define query params use Query, define body params use model


"""
from fastapi import APIRouter, Query

from .serialization import UserSerialization

user_router = APIRouter()


@user_router.get(path="/list")
async def get_user_list(
        page_size: int = Query(10, title="page size", description="how many user in a page", gt=1),
        page_number: int = Query(0, title="page number", description="current page of user list", ge=0)):
    pass


@user_router.post(path="/new")
async def add_new_user(user: UserSerialization):
    pass


@user_router.get(path="/{userid}")
async def get_user_detail(userid: str):
    pass
