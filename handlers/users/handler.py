# -*- coding: utf-8 -*-

"""

manager user information

see more information about how fast api parse path params, query params, body params

you need to define path params first and query params, then define body params as pydantic model

recommend way: define path params use Path, define query params use Query, define body params use model


"""
from fastapi import APIRouter, Query

from handlers.tools import GeneralJSONResponse
from processers.redis.driver import RedisDriver
from processers.postgres.driver import PostgresDriver
from .models import User
from .serialization import UserSerialization
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, func

user_router = APIRouter()


@user_router.get(path="/greeting")
async def greeting():
    return GeneralJSONResponse(code=1000, data="hi, welcome to fastapi boilerplate")


@user_router.get(path="/counter")
async def counter():
    rc = RedisDriver()
    await rc.set("a", 111)
    return GeneralJSONResponse(code=1000, data="hi, write something to redis")


@user_router.get(path="/list")
async def get_user_list(
        page_size: int = Query(10, title="page size", description="how many user in a page", gt=1),
        page_number: int = Query(
            0, title="page number", description="current page of user list", ge=0)
):
    async_session = async_sessionmaker(
        PostgresDriver.alchemy_engine, expire_on_commit=False)
    async with async_session() as session:
        stmt = select(func.count(User.id).label('cnt'))
        result = await session.execute(stmt)

        total = result.scalar_one()
        total_pages = total % page_size
        if page_number >= total_pages:
            page_number = total_pages

        offset = (page_number - 1) * page_size if page_number > 0 else 0
        limit = page_size
        users_ = await session.execute(select(*User.__table__.columns).offset(offset).limit(limit))
        users = [u._asdict() for u in users_.all()]
        return GeneralJSONResponse(code=1000,
                                   data=dict(total_page=total_pages, page_size=page_size, page_number=page_number,
                                             objects=users))


@user_router.post(path="/new")
async def add_new_user(user: UserSerialization):
    """
    create new user
    
    curl -X POST http://127.0.0.1:8000/api/v1/user/new \
    -H 'Content-Type: application/json' \
    -d '{"username":"smile26", "age":10, "mobile":"124", "address": "zj"}'

    :param user:
    :return:
    """
    async_session = async_sessionmaker(
        PostgresDriver.alchemy_engine, expire_on_commit=False)
    async with async_session() as session:
        user_inst = User(**user.dict())
        session.add(user_inst)
        await session.commit()
        return GeneralJSONResponse(code=1000, data=dict(id=user_inst.id, username=user_inst.username))


@user_router.get(path="/{user_id}")
async def get_user_detail(user_id: int):
    async_session = async_sessionmaker(
        PostgresDriver.alchemy_engine, expire_on_commit=False)
    async with async_session() as session:
        user = await session.execute(select(*User.__table__.columns).filter(User.id == user_id))
        users = [u._asdict() for u in user]
        return GeneralJSONResponse(code=1000, data=users)
