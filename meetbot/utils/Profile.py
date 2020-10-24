from typing import Dict, Any
from datetime import datetime

from meetbot.core.DataBase import DataBase


class Profile:
    def __init__(self, d: Dict[str, Any]):
        """d = les données de la bdd"""
        self.user_id: int = d["user_id"]
        self.name: str = d["name"]
        self.gender: str = d["gender"]
        self.description: str = d["description"]
        self.age: int = d["age"]
        self.country: str = d["country"]
        self.other: str = d["other"]
        self.creation_date: datetime = d["creation_date"]
        self.active: bool = bool(d["active"])
        self.last_meet: datetime = d["last_meet"]
        self.color: int = d["color"]

    @staticmethod
    def from_db(db: DataBase, user_id: int):
        return Profile(db.execute("SELECT * FROM profiles WHERE user_id = ?", str(user_id)).fetchall()[0])


PROFILE_COLUMS = {'name': 40, 'gender': 15, 'description': 255, 'country': 50, 'other': 500, 'age': 3, 'color': 6}
