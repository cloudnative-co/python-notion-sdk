from datetime import datetime
from enum import Enum
from typing import List, Dict

from ...base import Base
from ...utilities import request_parameter
from ...utilities import uuid_format


class Pages(Base):

    def get(self, page_id: str, filter_properties: str = None) -> dict:
        page_id = uuid_format(page_id)
        request = request_parameter(locals())
        return self.http_request(**request)

    def create(
        self, database_id: str,
        properties: dict[str, list],
        children: list[dict] = None,
        icon: dict[str, str] = None,
        cover: dict[str, str | dict[str, str]] = None
    ) -> dict:
        database_id = uuid_format(database_id)
        request = request_parameter(locals())
        return self.http_request(**request)
