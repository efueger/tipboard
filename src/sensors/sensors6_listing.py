# -*- coding: utf-8 -*-
import datetime, json, requests, time
from src.tipboard.app.properties import TIPBOARD_URL
from src.sensors.utils import getTimeStr, end, sendBVColor

NAME_OF_SENSORS = "listing"
TILE_TEMPLATE = "listing"
TILE_ID = "listing_ex"

def executeScriptToGetData():
    """ Simulate some actions for text tile exemple"""
    return {
        "items":
            ["Leader: 5",
             "Product Owner: 0",
             "Scrum Master: 3",
             "Developer: 0"]
        }


def sendDataToTipboard(data=None, tile_template=None, tile_id="", isTest=False):
    configTile = {
        "tile": tile_template, #tile_template name
        "key": tile_id, #tile_template name
        "data": json.dumps(data)
    }
    if not isTest:
        res = requests.post(TIPBOARD_URL + "/push", data=configTile)
        print(f"{res} -> {tile_id}: {res.text}", flush=True)

def sonde6(isTest):
    start_time = time.time()
    data = executeScriptToGetData()
    sendDataToTipboard(data, tile_template=TILE_TEMPLATE, tile_id=TILE_ID, isTest=isTest)
    end(title=f"sensors6 -> {TILE_ID}", start_time=start_time)