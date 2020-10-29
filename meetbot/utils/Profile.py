from typing import Dict, Any, Union
from datetime import datetime

from discord import Embed, User

from meetbot.core.DataBase import DataBase


class Profile:
    def __init__(self, d: Dict[str, Any]):
        """d = les données de la bdd"""
        self.user_id: int = int(d["user_id"])
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

    def __str__(self):
        return f"(ID: {self.user_id}) {self.name}, {self.gender} of {self.age} years old, from {self.country}."

    async def get_user(self, bot) -> User:
        return await bot.fetch_user(self.user_id)

    @staticmethod
    def get_prop(prop) -> Union[int, str]:
        if type(prop) is str:
            return prop if prop is not '' else 'Not provided'
        else:
            return prop if prop is not 0 else 'Not provided'

    async def to_embed(self, bot):
        user = await self.get_user(bot)
        em = Embed(color=self.color)
        em.set_author(name='Informations about: ' + user.name, icon_url=user.avatar_url)
        em.add_field(name='Name:', value=Profile.get_prop(self.name))
        em.add_field(name='Gender:', value=Profile.get_prop(self.gender))
        em.add_field(name='Age:', value=str(Profile.get_prop(self.age)))
        em.add_field(name='Description:', value=Profile.get_prop(self.description))
        em.add_field(name='Country:', value=Profile.get_prop(self.country))
        em.add_field(name='Profile creation date:', value=str(self.creation_date))
        em.add_field(name='Last meet command:', value=str(self.creation_date))
        em.add_field(name='Other:', value=Profile.get_prop(self.other))
        return em.set_footer(text='User id: ' + str(self.user_id))

    @staticmethod
    def from_db(db: DataBase, user_id: int):
        return Profile(db.execute("SELECT * FROM profiles WHERE user_id = ?", str(user_id)).fetchall()[0])


PROFILE_COLUMS = {'name': 40, 'gender': 15, 'description': 255, 'country': 50, 'other': 500, 'age': 3, 'color': 6}
