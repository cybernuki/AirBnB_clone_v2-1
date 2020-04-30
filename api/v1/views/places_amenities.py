#!/usr/bin/python3
""" Show, Delete, Create and Update amenities """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def amenities(place_id):
    """ Endpoint that handle http methods for a amenity

        place_id : is the id of the required place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenities = [place.to_dict() for place in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE', 'POST'])
def amenities_by_place(place_id, amenity_id):
    """ Endpoint that handle http methods for amenities of a place

        place_id: Is the id of the required place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place:
        abort(404)

    if not amenity:
        abort(404)

    if request.method == 'DELETE':
        if amenity_id not in [a.id for a in place.amenities]:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity_id in [a.id for a in place.amenities]:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
