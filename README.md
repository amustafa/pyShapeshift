# pyShapeshift

A python library for working with Shapeshift.io
Includes both sync libraries using [requests](http://docs.python-requests.org/en/master/) and async library using [aiohttp](https://aiohttp.readthedocs.io/en/stable/)

To see API behavior, see official [ShapeShift API Reference](https://info.shapeshift.io/)

## Sync vs. Async

The api is exactly the same between the two options, the only difference is how you import them.

* Sync Import is done `from pyShapshift import api` or `from pyShapshift.sync import api` 
* Async Import is done `from pyShapshift.async import api`


## Installation

`pip install git+https://github.com/amusatfa/pyShapeshift.git`


## How to Use

### Sync using requests

    from pyShapeshift import api

    print('Available Coins: ', api.get_coins())

### Async Using aiohttp

    import asyncio
    from pyShapeshift.async import api


    async def main():
        print('Available Coins: ', await api.get_coins())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())







