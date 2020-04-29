#!/usr/bin/python3
""" show status """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_of_state(state_id):
    """
        Route for handle http methods for requested city by state
        state_id: Is the id of the searched state
    """
    state = storage.get(State, state_id)
    print(state)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    if request.method == 'GET':
        return jsonify(cities)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        kwargs = request.get_json()
        kwargs['state_id'] = state_id
        city = City(**kwargs)
        city.save()
        storage.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def cities_by_id(city_id):
    """
        Route for a city that handle http methods
        city_id: is the id of the searched city
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in request.get_json().items():
            if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, attr, val)
        city.save()
        return jsonify(city.to_dict())
