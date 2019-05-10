# coding: utf-8

from flask import Flask, jsonify, request
from flask_cors import CORS
from src.entities.entity import Session, engine, Base
from src.entities.map import Map, MapSchema

app = Flask(__name__)

# CORS policy - ok for development, then check if I want to be more restrictive
CORS(app)

# if needed create database schema
Base.metadata.create_all(engine)


@app.route('/')
def index():
    return jsonify('Hello world')


@app.route('/maps')
def get_maps():
    # fetch from database
    session = Session()
    maps_object = session.query(Map).all()

    # serialize output
    schema = MapSchema(many=True)
    maps = schema.dump(maps_object)

    session.close()
    return jsonify(maps.data), 200


@app.route('/maps', methods=['POST'])
def add_maps():
    # deserialize input
    json_data = request.get_json()
    input = MapSchema().load(json_data)

    # create new map
    map = Map(title=input.data['title'], description=input.data['description'], created_by="HTTP postrequest")

    # persist to database
    session = Session()
    session.add(map)
    session.commit()
    session.close()

    return jsonify('Congrats ! You\'ve just created a new map!'), 201


if __name__ == "__main__":
    app.run()
