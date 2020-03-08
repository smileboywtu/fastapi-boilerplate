# -*- coding: utf-8 -*-

"""


common tools for all handlers


"""
import uuid

from fastapi.responses import UJSONResponse

status_codes = {
    1000: "success",
    2000: "database error",
    3000: "params error",
    4000: "internal error"
}


class GeneralJSONResponse(UJSONResponse):
    __slots__ = []

    def __init__(self, code, data, detail=""):
        body_data = {
            "code": code,
            "message": status_codes[code],
            "data": data,
            "detail": detail
        }
        super(GeneralJSONResponse, self).__init__(status_code=200, content=body_data)


def generate_request_id_by_uuid():
    """
    generate uuid for request id

    :param request:
    :return:
    """
    return uuid.uuid4().hex


def generate_instegram_request_id():
    pass
