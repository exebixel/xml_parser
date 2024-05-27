from enum import Enum
from pydantic import BaseModel

class XSDElementTypeAttribute(Enum):
    STRING = "xs:string"
    INTEGER = "xs:integer"
    COMPLEX_TYPE = "xs:complexType"
    SEQUENCE = "xs:sequence"


class XSDTree(BaseModel):
    name: str
    type: XSDElementTypeAttribute | None = None
    children: list["XSDTree"] = []
