import logging
import json

import aiohttp

from .exceptions import HostError, ResourceError, ResourceTypeError

_LOGGER = logging.getLogger(__name__)


class Controller:
    def __init__(self, session, host, port) -> None:
        self._rh = _RequestsHandler(session, host, port)

    async def fetch(self, resource: str):
        data = await self._rh.get(resource)
        print(data)
        return data


class _RequestsHandler:
    def __init__(self, session: aiohttp.ClientSession, host: str, port):
        self.headers = {"Accept": "application/json"}
        self.scheme = "http"

        self.session = session
        self.host = host
        self.port = port

    async def get(self, resource: str):
        """Method to get resource from Pool Controller API

        Parameters
        ----------
        resource : str
            Resource to get with leading '/'

        Returns
        -------
        JSON Object
            Object representing resource

        Raises
        ------
        ResourceTypeError
            Error raised when ContentType is not application/json
        HostError
            Error raised when Host refuses connection
        ResourceError
            Error raised when Resource return status code >= 400
        """
        data = []
        url = f"{self.scheme}://{self.host}:{self.port}{resource}"

        try:
            async with self.session.get(
                url,
                headers=self.headers,
                raise_for_status=True
            ) as resp:
                try:
                    data = await resp.json()
                except aiohttp.ContentTypeError as error:
                    _LOGGER.debug(repr(error))
                    raise ResourceTypeError(error.request_info.url) from error
                else:
                    _LOGGER.debug(json.dumps(data))
                    return data
        except aiohttp.ClientConnectorError as error:
            _LOGGER.warning(
                "Connection to PoolController failed: %s://%s:%s",
                self.scheme,
                self.host,
                self.port)
            _LOGGER.debug(repr(error))
            raise HostError(error.host, error.port) from error
        except aiohttp.ClientResponseError as error:
            _LOGGER.warning("Received unexpected response for resource: %s", resource)
            _LOGGER.debug(repr(error))
            raise ResourceError(error.status, error.request_info.url) from error
        else:
            _LOGGER.debug(
                "Connected to PoolController: %s://%s:%s",
                self.scheme,
                self.host,
                self.port)
