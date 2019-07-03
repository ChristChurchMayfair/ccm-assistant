from typing import Dict, Any
from enum import Enum, auto

AlexaResponse = Dict[str, Any]


class Service(Enum):
    morning = auto()
    evening = auto()
