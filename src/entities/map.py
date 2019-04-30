# coding=utf-8

from sqlalchemy import Column, String

from src.entities.entity import Entity, Base


class Map(Entity, Base):
    __tablename__ = 'maps'

    title = Column(String(16))
    description = Column(String(16))

    def __init__(self, title, description, created_by):
        Entity.__init__(self, created_by)
        self.title = title
        self.description = description

