from pydantic import BaseModel
from pydantic.typing import Optional, List


class Subgroup(BaseModel):
    caption: Optional[str]
    caption_translit: Optional[str]
    url_path: Optional[str]
    id: Optional[int]


class Group(BaseModel):
    caption: Optional[str]
    caption_translit: Optional[str]
    url_path: Optional[str]
    subgroups: Optional[List[Subgroup]]
    id: Optional[int]

# print(Group.__fields__.keys())