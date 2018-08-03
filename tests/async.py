from pyShapeshift.async import api
import asyncio


async def main():
    r = await api.get_coins()
    assert r is not None


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
