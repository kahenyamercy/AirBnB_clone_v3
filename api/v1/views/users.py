#!/usr/bin/python3
"""
Module to define all api routes for User
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.amenity import Amenity


# Get users
@app_views.route('/users', methods=['GET'])
def get_users():
    """
    Gets all users
    Return:
        (list): a list of dictionaries
    """
    serialized_users = []
    users  = storage.all(User)
    for value in users.values():
        serialized_users.append(value.to_dict())
    return jsonify(serialized_users)


# Get users by id
@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Gets user by id
    Return:
        (dict): a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


# Delete User Object
@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes users
    Args:
        user_id (str): user's id
    Return:
        (dict): an empty dictionary on successful deletion
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


# Create User
@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Create user

    Return:
        (dict): new user with the status code 201
    """
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400

    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400

    new_user = User(**data)

    # Add user obj to the database
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


# Update user
@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user by id
    Args:
        user_id (str): unique identifier for each user
    Returns:
        (dict): updated user object with the status code 200
    """
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    # Check if amenity_id is valid
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    excluded_attributes = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in excluded_attributes:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
