import urllib.error
import json


class APIException(urllib.error.HTTPError):
    code = ""
    reason = ""
    type = ""
    error = ""
    desc = ""

    def __init__(self, e: urllib.error.HTTPError = None):
        body = e.read().decode("utf-8")
        try:
            body = json.loads(body)
        except json.decoder.JSONDecodeError:
            return
        self.reason = e.reason
        self.code = e.code
        if "errors" in body:
            self.desc = body["errors"][0]["messages"][0]
            self.type = body["errors"][0]["type"]
        if e.code == 401:
            if "error" in body:
                self.type = "Autholization Error"
                self.error = body.get("error", "")
                self.desc = body.get("error_description", "")
            else:
                self.desc = body.get("message", "")
        return

    def __str__(self):
        return json.dumps({
            "code": self.code,
            "reason": self.reason,
            "message": self.desc,
            "type": self.type
        }, ensure_ascii=False)

    def __iter__(self):
        ret = {
            "code": self.code,
            "reason": self.reason,
            "message": self.desc,
            "type": self.type
        }
        for key, val in ret.items():
            yield (key, val)
