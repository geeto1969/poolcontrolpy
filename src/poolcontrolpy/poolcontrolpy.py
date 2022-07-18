import logging
import json

import aiohttp

from .exceptions import PoolControllerError

_LOGGER = logging.getLogger(__name__)

class Controller:
    def __init__(self, session) -> None:
        self._rh = _RequestsHandler(session)

    async def fetch(self):
        data = await self._rh.get()
        print(data)
        return data

class _RequestsHandler:
    def __init__(self, session: aiohttp.ClientSession):
        self.headers = {"Accept": "application/json"}

        self.session = session

    async def get(self):
        url = "http://10.0.20.13:4200/config/circuits"

        _LOGGER.debug("Sending request to: %s", url)
        try:
            async with self.session.get(
                url, headers=self.headers
            ) as resp:
                if resp.status != 200:
                    _LOGGER.warning("Invalid response from PoolController API: %s", resp.status)
                    raise PoolControllerError(resp.status, await resp.text())

                try:
                    data = await resp.json()
                except aiohttp.ContentTypeError:
                    data = await resp.json(content_type="text/html")
        except aiohttp.ClientConnectorError as e:
            print(repr(e))

        _LOGGER.debug(json.dumps(data))
        return data