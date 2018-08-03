"""
Async Shapeshift API

Uses the asyncio library and aiohttp to create an awaitable API.
"""
from .shapeshift_api import ShapeshiftAPI
from . import request_fns

api = ShapeshiftAPI(request_fns._async_get_request,
                    request_fns._async_post_request)
