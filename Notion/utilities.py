import base64
import datetime
import importlib
import inspect
import io
import json
import re


def uuid_format(value: str) -> str:
    rgx = r"([a-z0-9]{8})([a-z0-9]{4})([a-z0-9]{4})([a-z0-9]{4})([a-z0-9]{12})"
    m = re.findall(rgx, value)
    if m:
        value = "-".join(list(m[0]))
    return value


def normalization(args):
    result = {}
    for ky, value in args.items():
        if ky == "self":
            continue
        if value is None:
            value = "null"

        elif isinstance(value, str):
            value = value.replace('"', '\\"')
            value = '"{}"'.format(value)
        elif isinstance(value, datetime.datetime):
            value = value.strftime("%Y-%m-%d")
            value = f'"{value}"'
        elif isinstance(args[ky], dict):
            value = json.dumps(value)
        elif isinstance(args[ky], list):
            value = json.dumps(value)
        elif isinstance(value, bool):
            value = "true" if value else "false"
        elif isinstance(value, bytes):
            value = base64.b64encode(value)
            value = '"{}"'.format(value)
        result[ky] = value
    return result


def remove_none(params: dict):
    result = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, dict):
            v = remove_none(v)
            if v is None:
                continue
        elif isinstance(v, list):
            tmp_lst = []
            for v1 in v:
                if isinstance(v1, dict):
                    v1 = remove_none(v1)
                    if v1 is None:
                        continue
                tmp_lst.append(v1)
            if len(tmp_lst) == 0:
                continue
            v = tmp_lst
        result[k] = v
    if len(result) == 0:
        return None
    return result


def request_parameter(args: dict):
    map_path = args["self"].__module__.split(".")[:3]
    map_path.append("maps")
    map_path = ".".join(map_path)
    mdl_map = importlib.import_module(map_path)
    parameter_maps = mdl_map.Maps
    m_name = inspect.stack()[1].function
    req_map = parameter_maps.get(m_name, None)
    if req_map is None:
        return None

    method = req_map["method"]
    url = req_map.get("url", None)

    if url:
        url = url.format(**args)
    path = req_map.get("path", None)
    if path:
        path = path.format(**args)

    params = normalization(args)
    query = None
    payload = None
    if "query" in req_map:
        query = req_map["query"]
        query = query.format(**params)
        try:
            query = json.loads(query, strict=False)
        except json.decoder.JSONDecodeError as e:
            start = e.pos - 10
            start = 0 if start <= 0 else start
            end = e.pos + 10
            end = len(query) if len(query) >= end else end
            raise e
        query = remove_none(query)
    if "payload" in req_map:
        payload = req_map["payload"]
        payload = payload.format(**params)
        try:
            payload = json.loads(payload, strict=False)
        except json.decoder.JSONDecodeError as e:
            start = e.pos - 10
            start = 0 if start <= 0 else start
            end = e.pos + 10
            end = len(payload) if len(payload) >= end else end
            raise e
        payload = remove_none(payload)
    result = {
        "method": method,
        "url": url,
        "path": path,
        "query": query,
        "payload": payload
    }
    return result
