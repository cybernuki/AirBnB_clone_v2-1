#!/usr/bin/python3
""" Show, Delete, Create and Update amenities """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def reviews(review_id):
    """ Endpoint that handle http methods for a review

        review_id : is the id of the required review
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        info = request.get_json()

        if not info:
            abort(400, "Not a JSON")
        for attr, value in info.items():
            if attr not in ['id', 'user_id', 'place_id',
                            'created_at', 'updated_at']:
                setattr(review, attr, value)
        review.save()
        storage.save()
        return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def reviews_by_place(place_id):
    """ Endpoint that handle http methods for reviews of a place

        place_id: Is the id of the required place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        info = request.get_json()
        if not info:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in info:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if not storage.get(User, info['user_id']):
            abort(404)
        if 'text' not in info:
            return make_response(jsonify({'error': 'Missing text'}), 400)

        info['place_id'] = place_id
        review = Review(**info)
        review.save()
        storage.save()
        return jsonify(review.to_dict()), 201
