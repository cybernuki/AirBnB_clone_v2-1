#!/usr/bin/python3
""" show status """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route('cities/<city_id>/places', methods=['GET', 'POST'])
def places_of_city(city_id):
    """
        Route for handle http methods for requested place by city
        city_id: Is the id of the searched city
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [city.to_dict() for city in city.places]

    if request.method == 'GET':
        return jsonify(places)
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        kwargs = request.get_json()
        kwargs['city_id'] = city_id
        city = City(**kwargs)
        storage.new(city)
        storage.save()
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_by_id(place_id):
    """
        Route for a city that handle http methods
        place_id: is the id of the searched place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in request.get_json().items():
            if attr not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, attr, val)
        place.save()
        storage.save()
        return jsonify(place.to_dict()), 200
