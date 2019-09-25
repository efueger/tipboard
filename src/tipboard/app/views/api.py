# -*- coding: utf-8 -*-
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.http import HttpResponseServerError, Http404
from src.tipboard.app.applicationconfig import getRedisPrefix, getIsoTime
from src.tipboard.app.properties import PROJECT_NAME, LAYOUT_CONFIG, REDIS_DB, LOG, DEBUG
from src.tipboard.app.cache import getCache
from src.tipboard.app.utils import getTimeStr, checkAccessToken

cache = getCache()
redis = cache.redis


def get_tile(request, tile_key, unsecured=False):
    if not checkAccessToken(method="GET", request=request, unsecured=unsecured):
        return HttpResponse("API KEY incorrect", status=401)
    if redis.exists(tile_key):
        return HttpResponse(redis.get(tile_key))
    else:
        return HttpResponseBadRequest(f"{tile_key} key does not exist.")


def delete_tile(request, tile_key, unsecured=False):
    if not checkAccessToken(method="DELETE", request=request, unsecured=unsecured):
        return HttpResponse("API KEY incorrect", status=401)
    if redis.exists(tile_key):
        redis.delete(tile_key)
        return HttpResponse("Tile's data deleted.")
    else:
        return HttpResponseBadRequest(f"{tile_key} key does not exist.")


def tile(request, tile_key, unsecured=False):  # TODO: "it's better to ask forgiveness than permission" ;)
    """ Handles reading and deleting of tile's data """
    if request.method == "GET":
        return get_tile(request, tile_key, unsecured)
    elif request.method == "DELETE":
        return delete_tile(request, tile_key, unsecured)
    raise Http404


def push_tile(tile_id, data, tile_template):
    tilePrefix = getRedisPrefix(tile_id)
    if not redis.exists(tilePrefix):
        if LOG:
            print(f"{getTimeStr()}: (+) {tile_id} not found in cache, creating tile {tile_template}", flush=True)
        if cache.createTile(tile_id=tile_id, value=data, tile_template=tile_template):
            return HttpResponse(f"{tile_id} data created successfully.")
        else:
            return HttpResponse(f"Internal Error {tile_id} was not created")
    cachedTile = json.loads(redis.get(tilePrefix))
    cachedTile['data'] = json.loads(data)
    cachedTile['modified'] = getIsoTime()
    cachedTile['tile_template'] = tile_template
    cache.set(tilePrefix, json.dumps(cachedTile))
    return HttpResponse(f"{tile_id} data updated successfully.")


def push(request, unsecured=False):
    """ Update the content of a tile(widget) """
    if request.method == "POST":
        if not checkAccessToken(method="POST", request=request, unsecured=unsecured):
            return HttpResponse("API KEY incorrect", status=401)
        tile_id = request.POST.get("key", None)
        data = request.POST.get("data", None)
        tile_template = request.POST.get("tile", None)
        if not tile_id or not data or not tile_template:
            return HttpResponseBadRequest(f"Missing data")
        return push_tile(tile_id, data, tile_template)
    raise Http404


def update_tile_meta(request, tilePrefix, tile_key):
    cachedTile = json.loads(redis.get(tilePrefix))
    options = json.loads(request.body.decode("utf-8"))
    try:
        for metaItem in options.keys():
            cachedTile['meta'][metaItem] = options[metaItem]
    except Exception as e:
        return HttpResponseBadRequest(f"Invalid Json data: {e}")
    cache.set(tilePrefix, json.dumps(cachedTile))
    return HttpResponse(f"{tile_key} data updated successfully.")


def meta(request, tile_key, unsecured=False):
    """ Update the meta(config) of a tile(widget) """
    if request.method == "POST":
        if not checkAccessToken(method="POST", request=request, unsecured=unsecured):
            return HttpResponse("API KEY incorrect", status=401)
        tilePrefix = getRedisPrefix(tile_key)
        if not redis.exists(tilePrefix):
            return HttpResponseBadRequest(f"{tile_key} is not present in cache")
        return update_tile_meta(request, tilePrefix, tile_key)
    raise Http404


def isThereMetaUpdate(request, tile_id):
    try:
        request.POST.get("value", None)
        httpResponse = meta(request, tile_id)
        if httpResponse.status_code != 200:
            return httpResponse
    except Exception as e:
        if LOG:
            print(f"{getTimeStr()} (-) No meta value for update tile {tile_id}: {e}", flush=True)
        return HttpResponseBadRequest(f"{tile_id} data updated successfully.")
    return HttpResponse(f"{tile_id} data updated successfully.")


def update(request, unsecured=False):  # TODO: "it's better to ask forgiveness than permission" ;)
    """ Update the meta(config) AND the content of a tile(widget) """
    if request.method == "POST":
        if not checkAccessToken(method="POST", request=request, unsecured=unsecured):
            return HttpResponse("API KEY incorrect", status=401)
        tile_id = request.POST.get("key", None)
        data = request.POST.get("data", None)  # Test if var is present
        if data is None:
            print("No data")
        httpResponse = push(request)
        if httpResponse.status_code != 200:
            return httpResponse
        isThereMetaUpdate(request, tile_id)
    raise Http404


def projectInfo(request):
    if request.method == "GET":
        response = {
            'tipboard_version': "v0.1",
            'project_name': PROJECT_NAME,
            'project_layout_config': LAYOUT_CONFIG,
            'redis_db': REDIS_DB,
        }
        return JsonResponse(response)
    raise Http404


# Unsecured part
""" This allow previous user to use their old script without migration in a insecure way :) """


def tile_unsecured(request, tile_key):
    if not DEBUG:
        raise Http404
    else:
        return tile(request=request, tile_key=tile_key, unsecured=True)


def push_unsecured(request):
    if not DEBUG:
        raise Http404
    else:
        return push(request=request, unsecured=True)


def meta_unsecured(request, tile_key):
    if not DEBUG:
        raise Http404
    else:
        return meta(request=request, tile_key=tile_key, unsecured=True)


def update_unsecured(request):
    if not DEBUG:
        raise Http404
    else:
        return update(request=request, unsecured=True)
