# -*- coding: utf-8 -*-

"""

manager user information

see more information about how fast api parse path params, query params, body params

you need to define path params first and query params, then define body params as pydantic model

recommend way: define path params use Path, define query params use Query, define body params use model


"""
from fastapi import APIRouter, Query

from handlers.tools import GeneralJSONResponse
from .models import User
from .serialization import UserSerialization

user_router = APIRouter()


@user_router.get(path="/list")
async def get_user_list(
        page_size: int = Query(10, title="page size", description="how many user in a page", gt=1),
        page_number: int = Query(0, title="page number", description="current page of user list", ge=0)
):
    total = await User.all().count()
    total_pages = total % page_size
    if page_number >= total_pages:
        page_number = total_pages

    offset = (page_number - 1) * page_size if page_number > 0 else 0
    limit = page_size
    users = await User.all().offset(offset).limit(limit).values()
    return GeneralJSONResponse(code=1000,
                               data=dict(total_page=total_pages, page_size=page_size, page_number=page_number,
                                         objects=users))


@user_router.post(path="/new")
async def add_new_user(user: UserSerialization):
    """
    create new user

    :param user:
    :return:
    """
    user_inst = await User.create(**user.dict())
    return GeneralJSONResponse(code=1000, data=dict(id=user_inst.id, username=user_inst.username))


@user_router.get(path="/{user_id}")
async def get_user_detail(user_id: int):
    user = await User.filter(id=user_id).values(flat=True)
    return GeneralJSONResponse(code=1000, data=user)
