"""
pyShapeshift library is a wrapper for shapeshift.io REST
API

Includes sync and async libraries.
"""
from .shapeshift_api import ShapeshiftAPI
from . import sync
# from . import async


api = sync.api
