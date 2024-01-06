#!/usr/bin/python3
"""
Module to define all api routes for State
"""
from api.v1.views import app_views
from flask import jsonify, abort
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
    print(state)
    storage.delete(state)
    return jsonify({}), 200
