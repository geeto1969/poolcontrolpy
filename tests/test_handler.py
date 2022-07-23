import aiohttp

import pytest

from poolcontrolpy import poolcontrolpy
from poolcontrolpy.exceptions import *

routes = aiohttp.web.RouteTableDef()

@routes.get('/')
async def base(request):
    return aiohttp.web.Response(status=404)

@routes.get('/config/circuit/1')
async def circuit1(request):
    data = '{"id":1,"freeze":true,"type":1,"isActive":true,"eggTimer":60,"showInFeatures":false,"name":"Spa","nameId":72,"dontStop":false,"master":0}'
    return aiohttp.web.Response(body=data, content_type="application/json")

@routes.get('/config/circuit/2')
async def circuit2(request):
    data = 'Hello, world!'
    return aiohttp.web.Response(body=data, content_type="text/html")

async def test_host_connected(aiohttp_server):
    """Test successful connection to host
    """
    # Setup test server
    app = aiohttp.web.Application()
    app.add_routes(routes)
    server = await aiohttp_server(app)

    # Make request and confirm no exceptions
    async with aiohttp.ClientSession() as client:
        reqhandler = poolcontrolpy._RequestsHandler(client, server.host, server.port)
        try:
            resp = await reqhandler.get("/config/circuit/1")
        except Exception:
            assert False, 'Raised unexpected Exception'
        else:
            assert True

async def test_host_rejection(aiohttp_server):
    """Test exception handling of scenario where host does not respond or refuses connection
    """
    # Setup test server
    app = aiohttp.web.Application()
    app.add_routes(routes)
    server = await aiohttp_server(app)

    # Make request to incorrect port and confirm no connection exception
    async with aiohttp.ClientSession() as client:
        reqhandler = poolcontrolpy._RequestsHandler(client, server.host, server.port + 1)
        try:
            resp = await reqhandler.get("/config/circuit/1")
        except HostError:
            assert True, 'Raised expected HostError'
        except Exception:
            assert False, 'Failed to raise expected HostError'
        else:
            assert False, 'Bad Test: Connection not rejected'

async def test_resource_missing(aiohttp_server):
    """Test exception handling of scenario where the target resource is missing
    """
    # Setup test server without routes
    app = aiohttp.web.Application()
    server = await aiohttp_server(app)

    # Make request and validate successful connection but missing resource
    async with aiohttp.ClientSession() as client:
        reqhandler = poolcontrolpy._RequestsHandler(client, server.host, server.port)
        try:
            resp = await reqhandler.get("/config/circuit/1")
        except HostError:
            assert False, 'Bad Test: Connection rejected'
        except ResourceError:
            assert True, 'Raised expected ResourceError'
        except Exception:
            assert False, 'Raised unexpected Exception'
        else:
            assert False, 'Failed to raise any Exception'

async def test_resource_bad_type(aiohttp_server):
    """Test exception handling of scenario where the target resource is wrong type
    """
    # Setup test server
    app = aiohttp.web.Application()
    app.add_routes(routes)
    server = await aiohttp_server(app)

    # Make request and validate successful connection but wrong resource type
    async with aiohttp.ClientSession() as client:
        reqhandler = poolcontrolpy._RequestsHandler(client, server.host, server.port)
        try:
            resp = await reqhandler.get("/config/circuit/2")
        except HostError:
            assert False, 'Bad Test: Connection rejected'
        except ResourceError:
            assert False, 'Bad Test: Resource missing'
        except ResourceTypeError:
            assert True, 'Raised expected ContentTypeError'
        except Exception:
            assert False, 'Raised unexpected Exception'
        else:
            assert False, 'Failed to raise any Exception'
