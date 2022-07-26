import aiohttp

from poolcontrolpy.poolcontrolpy import Controller


routes = aiohttp.web.RouteTableDef()


@routes.get('/config')
async def config(request):
    """Returns good config resource stored in 'tests/config_good.json'"""
    with open('tests/config_good.json', 'r') as openfile:
        respbody = openfile.read()
    return aiohttp.web.Response(body=respbody, content_type="application/json")


async def test_checkconnect_connected(aiohttp_server):
    """Test successful connection to controller
    """
    # Setup test server
    app = aiohttp.web.Application()
    app.add_routes(routes)
    server = await aiohttp_server(app)

    # Confirm checkconnect returns true
    async with aiohttp.ClientSession() as client:
        controller = Controller(client, server.host, server.port)
        try:
            resp = await controller.checkconnect()
        except Exception: # pylint: disable=broad-except
            assert False, 'Raised unexpected Exception'
        else:
            assert resp, 'Returned False on good config'

async def test_checkconnect_failed(aiohttp_server):
    """Test failed connection to controller
    """
    # Setup test server
    app = aiohttp.web.Application()
    app.add_routes(routes)
    server = await aiohttp_server(app)

    # Confirm checkconnect returns false
    async with aiohttp.ClientSession() as client:
        controller = Controller(client, server.host, server.port + 1)
        try:
            resp = await controller.checkconnect()
        except Exception: # pylint: disable=broad-except
            assert False, 'Raised unexpected Exception'
        else:
            assert not resp, 'Returned True on bad config'
