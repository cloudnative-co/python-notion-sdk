# -*- coding: utf-8 -*-
# import module snippets
import http.cookiejar
import json
import urllib.request
import urllib.parse

from .exception import APIException


class Base(object):

    schema: str = "https"
    endpoint: str = "api.notion.com"
    client: urllib.request.OpenerDirector = None
    cookie: http.cookiejar.CookieJar = None
    headers: dict = dict()

    def __init__(
        self,
        access_token: str = None,
        version: str = None,
        client: object = None,
    ):
        if client is not None:
            self.client = client.client
            self.cookie = client.cookie
            self.headers = client.headers
            return
        self.cookie = http.cookiejar.CookieJar()
        self.client = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie)
        )
        urllib.request.install_opener(self.client)
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Notion-Version": version
        }

    def http_request(
        self,
        method: str, path: str = None, headers: dict = {},
        query: dict = None, payload: dict = None, url: str = None,
        files: dict = None, is_read: bool = True, with_header: bool = False,
        auth_method: str = None, auth_params: dict = {}, charset: str = "utf-8"
    ):
        if url is None:
            url = f"{self.schema}://{self.endpoint}/{path}"
        if query is None:
            query = dict()
        if "?" in url:
            q = url.split("?")
            if query is None:
                query = dict()
            for q1 in q[1].split("&"):
                q1 = q1.split("=")
                query[q1[0]] = q1[1]
        if len(query) > 0:
            url = "{}?{}".format(url, urllib.parse.urlencode(query))

        parsed_url = urllib.parse.urlparse(url)
        resource = "{}://{}".format(parsed_url.scheme, parsed_url.netloc)

        args = {
            "url": url,
            "method": method.upper()
        }
        ctype = headers.get('Content-Type', None)
        if ctype == "multipart/form-data":
            ctype, payload = self.encode_multipart(payload, files, charset)
            headers["Content-Type"] = ctype
            args["data"] = payload
        elif ctype == "application/octet-stream":
            args["data"] = payload
        elif ctype == "application/x-www-form-urlencoded":
            args["data"] = urllib.parse.urlencode(payload).encode()
        elif payload is not None:

            try:
                payload = json.dumps(payload).encode('utf-8')
                headers["Content-Type"] = "application/json; charset=UTF-8"
            except TypeError as e:
                try:
                    payload = urllib.parse.urlencode(payload).encode()
                except Exception as e:
                    pass
            args["data"] = payload
        else:
            payload = b""
        args["headers"] = dict(self.headers, **headers)
        req = urllib.request.Request(**args)
        try:
            with self.client.open(req) as res:
                head = dict(res.info())
                if is_read:
                    body = res.read()
                    try:
                        body = body.decode("utf-8")
                    except UnicodeDecodeError:
                        if with_header:
                            return body, head
                        return body
                    try:
                        body = json.loads(body)
                        if with_header:
                            return body, head
                        return body
                    except Exception as e:
                        if with_header:
                            return body, head
                        return body
                return res
        except urllib.error.HTTPError as e:
            raise APIException(e)
