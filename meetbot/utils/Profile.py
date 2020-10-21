from typing import List, Optional


class Profile:
    def __init__(self, user_id: str, name: str, gender: str, description='', age=None, flag=None, other=None):
        self.user_id = user_id
        self.name: str = name
        self.gender: str = gender
        self.description: str = description
        self.age: int = age
        self.flag: str = flag
        self.other: Optional[List[str]] = None if other is None else [x for x in other.split(";;")]
