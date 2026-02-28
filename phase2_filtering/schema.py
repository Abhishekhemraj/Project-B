from enum import Enum
from pydantic import BaseModel, Field

class LengthClass(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"

class LamenessLevel(str, Enum):
    WITTY = "witty"
    AVERAGE = "average"
    CRINGE = "cringe"

class JokeRequest(BaseModel):
    length_class: LengthClass
    lameness_level: LamenessLevel

class JokeResponse(BaseModel):
    text: str
    length_class: LengthClass
    lameness_level: LamenessLevel


