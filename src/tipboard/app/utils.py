# -*- coding: utf-8 -*-
from datetime import datetime
from src.tipboard.app.properties import API_KEY, DEBUG


def getTimeStr():
    return datetime.now().strftime("%Hh%M")


def checkAccessToken(method='GET', request=None, unsecured=False):
    """ Check if API_TOKEN is correct. Who cares about api version ?"""
    key = "NO_KEY_FOUND"
    if unsecured:
        return True
    try:
        if method == 'GET' or method == 'POST' or method == 'DELETE' and \
                request.GET.get('API_KEY', 'NO_API_KEY_FOUND') == API_KEY:  # TODO: check if it's work with delete:
            return True
    except Exception:
        pass
    print(f"{getTimeStr()} (-) Access Token error: {key}")
    return False
