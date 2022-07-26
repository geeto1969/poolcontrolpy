# poolcontrolpy

Package for accessing nodejs-poolController for use with a planned Home Assistant integration.

## Installation

```bash
$ pip install poolcontrolpy
```

## Usage

This example uses 'asyncio.run' so it cannot be called when another asyncio event loop is running in the same thread.

```python
import asyncio
import aiohttp

from poolcontrolpy.poolcontrolpy import Controller


async def get():

    async with aiohttp.ClientSession() as client:
        controller = Controller(client, "10.0.20.13", 4200)
        return await controller._rh.get("/config")

config = asyncio.run(get())
print(config['circuits'][1])
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`poolcontrolpy` was created by Kevin Robinson. It is licensed under the terms of the MIT license.

## Credits

`poolcontrolpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
