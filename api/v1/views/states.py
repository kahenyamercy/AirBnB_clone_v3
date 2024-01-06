#!/usr/bin/python3
"""
Module to define all api routes for State
"""
from api.v1.views import app_views
from flask import jsonify
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
