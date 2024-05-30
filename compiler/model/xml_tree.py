
from pydantic import BaseModel


class XMLTree(BaseModel):
    tag: str
    text: str = ""
    children: list['XMLTree'] = []
    attributes: dict[str, str] = {}
