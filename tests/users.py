# -*- coding: utf-8 -*-

"""

user test cases

"""

from . import client


def test_get_all_users():
    resp = client.get("/api/v1/user/list")
    assert resp.status_code == 200, "http error"
