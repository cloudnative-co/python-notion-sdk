from datetime import datetime
from enum import Enum
from typing import List, Dict

from ...base import Base
from ...utilities import request_parameter
from ...utilities import uuid_format


class Databases(Base):

    def get(self, database_id: str) -> dict:
        database_id = uuid_format(database_id)
        request = request_parameter(locals())
        return self.http_request(**request)

    def filter(self, database_id: str, filter: dict) -> dict:
        database_id = uuid_format(database_id)
        request = request_parameter(locals())
        return self.http_request(**request)
