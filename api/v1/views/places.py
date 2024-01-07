#!/usr/bin/python3
"""
Module to define all State api routes
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


# Get places of a City
@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """
    Gets a list of all places associated with a certain city
    Return:
        (list): a list of dictionaries
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = []
    city_places = []
    places = storage.all(Place)
    for value in places.values():
        all_places.append(value.to_dict())
    for place in all_places:
        if place['city_id'] == city_id:
            city_places.append(place)
    return jsonify(city_places)


# Get place by id
@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Gets place by id
    Return:
        (dict): a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


# Delete Place Object
@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes place by id
    Args:
        place_id (str): place's id
    Return:
        (dict): an empty dictionary on successful deletion
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


# Create place
@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_city_place(city_id):
    """
    Create a place linked to a certain city

    Return:
        (dict): new place with the status code 201
    """
    # Check is state_id is linked to a state
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    new_place = Place(city_id=city_id, **data)

    # Add city obj to the database
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


# Update place by id
@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Updates place by id
    Args:
        place_id (str): place's id
    Returns:
        (dict): city object with the status code 200
    """
    # Check if place_id is linked to a place
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    # List of attributes that should not be updated
    excluded_attrs = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in excluded_attrs:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
