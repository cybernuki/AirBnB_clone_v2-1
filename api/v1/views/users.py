#!/usr/bin/python3
""" Show, Delete, Create and Update amenities """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    """ Endpoint that retrieves all users
        or post a new one
    """
    if request.method == 'GET':
        users = storage.all(User)
        users_info = [user.to_dict() for user in users.values()]
        return jsonify(users_info)

    if request.method == 'POST':
            info = request.get_json()
            if not info:
                abort(400, 'Not a JSON')
            if 'email' not in info:
                abort(400, 'Missing email')
            if 'password' not in info:
                abort(400, 'Missing password')
            user = User(**info)
            storage.new(user)
            storage.save()
            return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def users_params(user_id):
    """ Endpoint that retrieves, delete or update
        a user by id

        user_id: Is the id of the required user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        info = request.get_json()
        if not info:
            abort(400, "Not a JSON")

        for attr, val in info.items():
            if attr not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, attr, val)
        user.save()
        storage.save()
        return jsonify(user.to_dict())
