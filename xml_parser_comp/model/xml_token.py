from enum import Enum
from pydantic import BaseModel, ConfigDict


class TagType(Enum):
    Tag = "Tag"
    Text = "Text"


class XMLToken(BaseModel):
    type: TagType
    is_opening_tag: bool
    is_closing_tag: bool
    tag_name: str | None = None
    text: str | None = None

    model_config = ConfigDict(use_enum_values=True)
