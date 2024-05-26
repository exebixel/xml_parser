
from pydantic import BaseModel


class XMLTree(BaseModel):
    """
    XMLTree represents the structure of an XML document.
    """

    tag: str
    text: str = ""
    children: list['XMLTree'] = []
