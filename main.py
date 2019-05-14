# coding: utf-8
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.entities.entity import Session, engine, Base
from src.entities.map import Map, MapSchema
from datetime import datetime

app = Flask(__name__)

# cross origin policy - ok for development, then check if I want to be more restrictive
CORS(app)

# if needed create database schema
# Base.metadata.create_all(engine)


@app.route('/')
def index():
    return jsonify('Welcome to my API'), 200


@app.route('/maps')
def get():
    # fetch from database
    session = Session()
    maps_object = session.query(Map).all()

    # serialize output
    schema = MapSchema(many=True)
    resp = schema.dump(maps_object)

    session.close()
    return jsonify(resp.data), 200


@app.route('/maps/<int:id>', methods=['GET'])
def get_id(id):
    # fetch from database
    session = Session()
    map_object = session.query(Map).get(id)
    if map_object is None:
        return not_found()
    else:
        # serialize output
        schema = MapSchema(many=False)
        resp = schema.dump(map_object)

    session.close()
    return jsonify(resp.data), 200


@app.route('/maps', methods=['POST'])
def post():
    # deserialize input
    json_data = request.get_json()
    map_tdb = MapSchema().load(json_data)

    # create new map
    map_object = Map(title=map_tdb.data['title'], description=map_tdb.data['description'], user="Simon")

    # add & persist to database
    session = Session()
    session.add(map_object)
    session.commit()

    session.close()
    return jsonify(f'{request.url}/{map_object.id}'), 201


@app.route('/maps/<int:id>', methods=['PUT'])
def put(id):
    # deserialize input
    json_data = request.get_json()
    map_tdb = MapSchema().load(json_data)

    # get map to update
    session = Session()
    map_object = session.query(Map).get(id)

    # update & persist to database
    map_object.description = map_tdb.data['description']
    map_object.title = map_tdb.data['title']
    map_object.updated_at = datetime.now()
    session.commit()

    # send it as request response - serialized
    schema = MapSchema(many=False)
    resp = schema.dump(map_object)

    session.close()
    return jsonify(resp.data), 200


@app.route('/maps/delete/<int:id>', methods=['DELETE'])
def delete(id):
    # get map to delete
    session = Session()
    map_object = session.query(Map).get(id)

    # delete & persist to database
    session.delete(map_object)
    session.commit()

    session.close()
    return jsonify('You\'ve just deleted a map successfully'), 204


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run()
