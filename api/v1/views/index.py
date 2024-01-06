#!/usr/bin/python3
"""
Module to define all api routes
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.state import State


@app_views.route('/status', methods=['GET'])
def status():
    """
    Tests whether the api is working
    Returns a JSON dictionary
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Returns the number of each object by type
    """
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)
    stats = {
            "amenities": amenities,
            "cities": cities,
            "places": places,
            "reviews": reviews,
            "states": states,
            "users": users
        }
    return jsonify(stats)
