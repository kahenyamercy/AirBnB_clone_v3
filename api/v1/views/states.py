#!/usr/bin/python3
"""
Module to define all api routes for State
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """
    Gets the list of all State objects
    Return:
        (list): a list of dictionaries
    """
    serialized_states = []
    states = storage.all(State)
    for value in states.values():
        serialized_states.append(value.to_dict())
    return jsonify(serialized_states)


# Get State object
@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """
    Gets State object
    Return:
        (dict): a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


# Delete State Object
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes  a State object
    Args:
        state_id (str): states id
    Return:
        (dict): an empty dictionary on successful deletion
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


# Create State
@app_views.route('/states', methods=['POST'])
def create_state():
    """
    Create a State item

    Return:
        (dict): new state with the status code 201
    """
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(name=data['name'])

    # Add state obj to the database
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


# Update State
@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """
    Updates a State item
    Args:
        state_id (str): state's id
    Returns:
        (dict): state object with the status code 200
    """
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    # List of attributes not to be updated
    excluded_attrs = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in excluded_attrs:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
