from datetime import datetime

from typing import List
from meetbot.core.DataBase import DataBase


class Profile:
    def __init__(self, db: DataBase, user_id: str):
        self._db = db
        d = self._db.execute("SELECT * FROM profiles WHERE user_id = ?", user_id).fetchall()[0]

        self.user_id = user_id
        self.name: str = d["name"]
        self.gender: str = d["gender"]
        self.description: str = d["description"]
        self.age: int = d["age"]
        self.country: str = d["country"]
        self.other: List[str] = [] if d["other"] is '' else [x for x in d["other"].split(";;")]
        self.creation_date: datetime = d["creation_date"]
        self.active: bool = bool(d["active"])
        self.last_meet: datetime = d["last_meet"]
        self.color = d["color"]


PROFILE_COLUMS = {'name': 40, 'gender': 15, 'description': 255, 'country': 50, 'other': 500, 'age': 3, 'color': 6}
