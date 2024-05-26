from pydantic import BaseModel


class XSDToken(BaseModel):
    name: str
    attributes: dict
    is_opening_tag: bool
    is_closing_tag: bool