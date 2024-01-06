#!/usr/bin/python3
"""
Main Entry point for the RESTFUL API
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Teardown context
    """
    storage.close()


# 404 error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    api_host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    api_port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=api_host, port=api_port)
