#!/usr/bin/python3
"""
Module to define all api routes for State
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


# Get cities of a State
@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    """
    Gets the list of all City objects of a State
    Return:
        (list): a list of dictionaries
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = []
    states_cities = []
    cities = storage.all(City)
    for value in cities.values():
        all_cities.append(value.to_dict())
    for city in all_cities:
        if city['state_id'] == state_id:
            states_cities.append(city)
    return jsonify(states_cities)


# Get City object
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """
    Gets City object
    Return:
        (dict): a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


# Delete City Object
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes  a City object
    Args:
        city_id (str): city's id
    Return:
        (dict): an empty dictionary on successful deletion
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


# Create City
@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city_state(state_id):
    """
    Create a City of State

    Return:
        (dict): new city with the status code 201
    """
    # Check is state_id is linked to a state
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_city = City(state_id=state_id, name=data['name'])

    # Add city obj to the database
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


# Update State
@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Updates a City item
    Args:
        state_id (str): city's id
    Returns:
        (dict): city object with the status code 200
    """
    # Check if city_id is linked to a city
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    # List of attributes that should not be updated
    excluded_attrs = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in excluded_attrs:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
