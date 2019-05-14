# coding=utf-8

from sqlalchemy import Column, String
from src.entities.entity import Entity, Base
from marshmallow import Schema, fields


class Map(Entity, Base):
    __tablename__ = 'maps'

    title = Column(String(16))
    description = Column(String(16))

    def __init__(self, title, description, user):
        Entity.__init__(self, user)
        self.title = title
        self.description = description


class MapSchema(Schema):
    id = fields.Number()
    title = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
