from pydantic import BaseModel

class XSDTree(BaseModel):
    tag: str
    type: str | None = None
    children: list["XSDTree"] = []

