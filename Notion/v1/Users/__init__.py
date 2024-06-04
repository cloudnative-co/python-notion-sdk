from datetime import datetime
from enum import Enum
from typing import List, Dict

from ...base import Base
from ...utilities import request_parameter


class Users(Base):

    def list(
        self, start_cursor: str = None, page_size: int = None
    ) -> dict:
        """
        User一覧の取得
        """
        request = request_parameter(locals())
        return self.http_request(**request)

    def get(self, user_id: str) -> dict:
        request = request_parameter(locals())
        return self.http_request(**request)

    def me(self) -> dict:
        request = request_parameter(locals())
        return self.http_request(**request)
