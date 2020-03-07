# -*- coding: utf-8 -*-

"""

manager user information


"""

from handlers.application import app_instance


@app_instance.route(path="/api/v1/user/list", methods=["GET"])
async def get_user_list():
    pass


@app_instance.route(path="/api/v1/user/add", methods=["POST"])
async def add_new_user():
    pass


@app_instance.route(path="/api/v1/user/{userid}", methods=["GET"])
async def get_user_detail():
    pass
