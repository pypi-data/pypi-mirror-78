from typing import *
import aiohttp
import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr

from ..types import Updatable, oauth_refresh


# noinspection PyAttributeOutsideInit
class Osu(Updatable):
    __tablename__ = "osu"

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def user(self):
        return relationship("User", backref=backref("osu"))

    @declared_attr
    def access_token(self):
        return Column(String, nullable=False)

    @declared_attr
    def refresh_token(self):
        return Column(String, nullable=False)

    @declared_attr
    def expiration_date(self):
        return Column(DateTime, nullable=False)

    @declared_attr
    def osu_id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def username(self):
        return Column(String, nullable=False)

    @declared_attr
    def avatar_url(self):
        return Column(String)

    @declared_attr
    def standard_pp(self):
        return Column(Float)

    @declared_attr
    def taiko_pp(self):
        return Column(Float)

    @declared_attr
    def catch_pp(self):
        return Column(Float)

    @declared_attr
    def mania_pp(self):
        return Column(Float)

    async def refresh(self, *, client_id, client_secret):
        j = await oauth_refresh(url="https://osu.ppy.sh/oauth/token",
                                client_id=client_id,
                                client_secret=client_secret,
                                refresh_code=self.refresh_token)
        self.access_token = j["access_token"]
        self.refresh_token = j.get("refresh_token") or self.refresh_token
        self.expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=j["expires_in"])

    async def refresh_if_expired(self, *, client_id, client_secret):
        if datetime.datetime.now() >= self.expiration_date:
            await self.refresh(client_id=client_id, client_secret=client_secret)

    def json(self) -> dict:
        return {
            "osu_id": self.osu_id,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "standard": {
                "pp": self.standard_pp,
            },
            "taiko": {
                "pp": self.taiko_pp,
            },
            "catch": {
                "pp": self.catch_pp,
            },
            "mania": {
                "pp": self.mania_pp,
            },
        }
