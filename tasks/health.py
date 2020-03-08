# -*- coding: utf-8 -*-

"""

application health check task

"""

import asyncio
import socket
import time


async def check_socket(host, port):
    """
    check if socket is ok

    :param host:
    :param port:
    :return:
    """
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(b'hello')
        await writer.drain()
        writer.close()
        return 0, ''
    except Exception as e:
        return -1, str(e)


def simple_check_socket(host, port, timeout=3, verbose=False):
    """
    Check if socket is open and detect socket error if need

    :param host:
    :param port:
    :param timeout:
    :return:
    """
    try:
        ip = socket.gethostbyname(host)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.send(b"0")
        sock.recv(1)
    except socket.timeout:
        errcode, errmsg = 1, "Socket Connect Timeout"
    except socket.error as e:
        errcode, errmsg = e.errno, e.strerror
    else:
        errcode, errmsg = 0, None
    finally:
        logmsg = (
            "{ts} | "
            "{errtype} | "
            "{host}:{ip}:{port} | "
            "{errcode} | "
            "{errmsg}"
        ).format(
            ts=int(time.time()),
            errtype="SOCKET",
            host=host,
            ip=ip,
            port=port,
            errcode=errcode,
            errmsg=errmsg or ""
        )
        if verbose:
            print(logmsg)
        return errcode, errmsg, logmsg


async def check_redis(host, port):
    return await check_socket(host, port)


async def check_postgres(host, port):
    return await check_socket(host, port)
