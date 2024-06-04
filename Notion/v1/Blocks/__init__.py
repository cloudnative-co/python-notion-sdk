from datetime import datetime
from enum import Enum
from typing import List, Dict

from ...base import Base
from ...utilities import request_parameter
from ...utilities import uuid_format


class Blocks(Base):

    def get(self, block_id: str) -> dict:
        block_id = uuid_format(block_id)
        request = request_parameter(locals())
        return self.http_request(**request)

    def children(
        self, block_id: str, start_cursor: str = None, page_size: int = None
    ) -> dict:
        block_id = uuid_format(block_id)
        request = request_parameter(locals())
        return self.http_request(**request)

    def append(
        self, block_id: str, children: list[dict], after: str = None
    ) -> dict:
        block_id = uuid_format(block_id)
        request = request_parameter(locals())
        return self.http_request(**request)
