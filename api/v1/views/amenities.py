#!/usr/bin/python3
"""
Module to define all api routes for Amenity
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


# Get amenities
@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """
    Gets all amenities
    Return:
        (list): a list of dictionaries
    """
    serialized_amenities = []
    amenities  = storage.all(Amenity)
    for value in amenities.values():
        serialized_amenities.append(value.to_dict())
    return jsonify(serialized_amenities)


# Get amenity by id
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Gets amenity item
    Return:
        (dict): a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


# Delete Amenity Object
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes Amenity  object
    Args:
        amenity_id (str): amenity's id
    Return:
        (dict): an empty dictionary on successful deletion
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


# Create Amenity 
@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """
    Create an Amenity item

    Return:
        (dict): new amenity with the status code 201
    """
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(name=data['name'])

    # Add amenity obj to the database
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


# Update Amenity
@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an Amenity item
    Args:
        amenity_id (str): amenity's id
    Returns:
        (dict): amenity object with the status code 200
    """
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    # Check if amenity_id is valid
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    # List of attributes not to be updated
    excluded_attrs = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in excluded_attrs:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
