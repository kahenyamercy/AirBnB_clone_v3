#!/usr/bin/python3
"""
Module to define all api routes
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    """
    Tests whether the api is working
    Returns a JSON dictionary
    """
    return jsonify({"status": "OK"})
