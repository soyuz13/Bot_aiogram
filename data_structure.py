from pydantic import BaseModel
from pydantic.typing import Optional, List


class Subgroup(BaseModel):
    id: Optional[int]
    caption: Optional[str]
    caption_translit: Optional[str]
    url_path: Optional[str]


class Group(BaseModel):
    id: Optional[int]
    caption: Optional[str]
    caption_translit: Optional[str]
    url_path: Optional[str]
    subgroups: Optional[List[Subgroup]]
