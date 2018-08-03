"""
Request Functions

Request function use in the shapeshift api to allow the class
to either be async or sync.
"""
import aiohttp
import requests


def _sync_get_request(url):
    """
    Takes the url and returns the json synchronously.

    :url: (str) url to get
    """
    response = requests.get(url)
    return response.json()


def _sync_post_request(url, payload):
    """
    Takes the url, posts, and returns the json synchronously.

    :url: (str) url to get
    :payload: (dict) data to send in post
    """
    response = requests.post(url, data=payload)
    return response.json()


async def _async_get_request(url):
    """
    Takes the url and returns the json asynchronously.

    :url: (str) url to get
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def _async_post_request(url, payload):
    """
    Takes the url, posts, and returns the json asynchronously.

    :url: (str) url to get
    :payload: (dict) data to send in post
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            return await response.json()
