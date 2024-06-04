# -*- coding: utf-8 -*-
# import module snippets
from .base import Base
from .v1 import Client as v1


class Client(Base):
    __v1: v1 = None

    @property
    def v1(self):
        if self.__v1 is None:
            self.__v1 = v1(client=self)
        return self.__v1
