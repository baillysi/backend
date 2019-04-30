# coding=utf-8

from src.entities.entity import Session, engine, Base
from src.entities.map import Map


# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
maps = session.query(Map).all()

if len(maps) == 0:
    # create and persist dummy exam
    new_map = Map("title", "oui", "created_by")
    session.add(new_map)
    session.commit()
    session.close()

    # reload exams
    maps = session.query(Map).all()

# show existing exams
print('### Maps:')
for map in maps:
    print(f'({map.id}) {map.title} - {map.description}')

