from enum import Enum
from pydantic import BaseModel

class XSDElementTypeAttribute(Enum):
    STRING = "xs:string"
    INTEGER = "xs:integer"
    DECIMAL = "xs:decimal"
    BOLLEAN = "xs:boolean"
    DATE = "xs:date"
    TIME = "xs:time"

    COMPLEX_TYPE = "xs:complexType"
    SEQUENCE = "xs:sequence"

class XSDAttribute(BaseModel):
    name: str
    type: XSDElementTypeAttribute

class XSDTree(BaseModel):
    name: str
    type: XSDElementTypeAttribute | None = None
    attributes: list[XSDAttribute] = []
    children: list["XSDTree"] = []
