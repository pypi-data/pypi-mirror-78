from dataclasses import dataclass
from moodlepy import MoodleObject


@dataclass
class Category(MoodleObject):
    id: int
    name: str
    description: str
    descriptionformat: int
    parent: int
    sortorder: int
    coursecount: int
    depth: int
    path: str
