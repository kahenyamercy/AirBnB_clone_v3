#!/usr/bin/python3
"""
Package views
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
from api.v1.views.index import status, stats
from api.v1.views.states import get_states, get_state
