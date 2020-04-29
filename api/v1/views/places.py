#!/usr/bin/python3
""" show status """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_of_city(city_id):
    """
        Route for handle http methods for requested place by city
        city_id: Is the id of the searched city
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    info_city = []
    for info in city.places:
        info_city.append(info.to_dict())
    if request.method == 'GET':
        return jsonify(info_city)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if "user_id" not in data:
            abort(400, 'Missing user_id')
        if storage.get(User, data["user_id"]) is None:
            abort(404)
        if "name" not in data:
            abort(400, 'Missing name')

        data['city_id'] = city_id
        new_place = Place(**data)
        new_place.save()
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
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
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        info = request.get_json()
        if not info:
            abort(400, "Not a JSON")
        dont = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
        for key, value in info.items():
            if key in dont:
                pass
            else:
                setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
