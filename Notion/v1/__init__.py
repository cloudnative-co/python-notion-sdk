from ..base import Base
from .Blocks import Blocks
from .Pages import *
from .Users import *
from .Blocks import *
from .Databases import *


class Client(Base):

    def __getattr__(self, name):
        cls_name = name.capitalize()
        if cls_name not in globals():
            return None

        if not getattr(self, f"__{name}"):
            cls = globals()[cls_name]
            setattr(self, f"__{name}", cls(client=self))
        return getattr(self, f"__{name}")
