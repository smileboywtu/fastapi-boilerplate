# -*- coding: utf-8 -*-

"""
dev develop tools
"""


import typer

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('./.envs/.production/.fastapi'),verbose=True)
load_dotenv(Path('./.envs/.production/.postgres'),verbose=True)

## user import here
import config
import asyncio
import uvicorn
from operator import attrgetter
from handlers.application import app_instance
from init_postgres_schema import init_postgres_orm_model

app = typer.Typer()

@app.command(help='开启测试web 服务器')
def runserver():
    uvicorn.run("handlers.application:app_instance",reload=True)

@app.command(help='初始化 ORM')
def initorm(name:str=None):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_postgres_orm_model())
    
@app.command(help='执行预置的 SQL')
def runsql(sql_name:str):
    from processers.postgres_process import pg_client
    async def run_sql_by_name(sql_name):
        await pg_client.execute_sql(sql_name)
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_sql_by_name(sql_name))
    print('execute sql done:')
    print(attrgetter(sql_name)(pg_client.query).sql)

@app.command(help='列举预置的 SQL')
def listsql():
    from processers.postgres_process import pg_client
    print("all available aiosql: ", list(pg_client.query.available_queries))
    
@app.command(help='查询预置 SQL 明细内容')
def showsql(sql_name:str):
    from processers.postgres_process import pg_client
    if sql_name not in list(pg_client.query.available_queries):
        print('sql name: {0} not find, all available sql names: {1}'.format(
            sql_name,list(pg_client.query.available_queries)
        ))
    else:
        print(attrgetter(sql_name)(pg_client.query).sql)
    
@app.command(help='ORM 功能测试')
def sqlalchemy():
    from processers.postgres_process import pg_client
    from sqlalchemy.ext.asyncio import async_sessionmaker
    from sqlalchemy import select,func
    from handlers.users.models import User
    async_session = async_sessionmaker(
    pg_client.alchemy_engine, expire_on_commit=False)
    
    async def _query():
        async with async_session() as session:
            stmt = select(func.count(User.id).label('cnt'))
            # print(stmt)
            result = await session.execute(stmt)
            print(result.scalar_one())
            
            users = await session.execute(select(*User.__table__.columns).offset(0).limit(10))
            print([u._asdict() for u in users.all()])
            print(users.all())
            # await session.commit()
            
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_query())
    

if __name__ == '__main__':
    app()