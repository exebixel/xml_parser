from enum import Enum
from pydantic import BaseModel

class XSDElementTypeAttribute(Enum):
    DATE = "xs:date"
    TIME = "xs:time"
    STRING = "xs:string"
    INTEGER = "xs:integer"
    DECIMAL = "xs:decimal"
    BOLLEAN = "xs:boolean"

    COMPLEX_TYPE = "xs:complexType"
    SEQUENCE = "xs:sequence"

class XSDAttribute(BaseModel):
    name: str
    type: XSDElementTypeAttribute

class XSDTree(BaseModel):
    name: str
    children: list["XSDTree"] = []
    attributes: list[XSDAttribute] = []
    type: XSDElementTypeAttribute | None = None
