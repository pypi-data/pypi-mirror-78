# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_minecraft']
install_requires = \
['pytest>=6.0.1,<7.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'pytest11': ['minecraft = pytest_minecraft']}

setup_kwargs = {
    'name': 'pytest-minecraft',
    'version': '0.1.0',
    'description': 'A pytest plugin for running tests against Minecraft releases',
    'long_description': '# pytest-minecraft\n\n[![Build Status](https://travis-ci.com/vberlier/pytest-minecraft.svg?branch=master)](https://travis-ci.com/vberlier/pytest-minecraft)\n[![PyPI](https://img.shields.io/pypi/v/pytest-minecraft.svg)](https://pypi.org/project/pytest-minecraft/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-minecraft.svg)](https://pypi.org/project/pytest-minecraft/)\n\n> A pytest plugin for running tests against Minecraft releases.\n\nThe plugin automatically downloads the latest version of the Minecraft client into the pytest cache. The provided fixtures can also extract the vanilla [resource pack](https://minecraft.gamepedia.com/Resource_Pack) and [data pack](https://minecraft.gamepedia.com/Data_Pack) on demand.\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install pytest-minecraft\n```\n\n## Usage\n\nDownloading the Minecraft client takes a few seconds so the tests that use the fixtures provided by the plugin will be skipped unless explicitly enabled with a command-line flag. The `--minecraft-latest` flag will enable the tests and run them against the latest stable release.\n\n```sh\n$ pytest --minecraft-latest\n```\n\nYou can also use the `--minecraft-snapshot` flag to test against the latest snapshot. Both flags can be specified at the same time to run the tests against both stable and snapshot releases.\n\n```sh\n$ pytest --minecraft-latest --minecraft-snapshot\n```\n\n### Fixtures\n\n- The `minecraft_client_jar` fixture returns the path to the downloaded Minecraft client as a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path) instance.\n\n  ```python\n  def test_with_client(minecraft_client_jar):\n      assert minecraft_client_jar.name == "client.jar"\n\n      with ZipFile(minecraft_client_jar) as client:\n          assert len(client.namelist()) > 10_000\n  ```\n\n- The `minecraft_resource_pack` fixture returns the path to the extracted vanilla resource pack as a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path) instance.\n\n  ```python\n  def test_with_resource_pack(minecraft_resource_pack):\n      assert minecraft_resource_pack.name == "resource_pack"\n      assert (minecraft_resource_pack / "assets" / "minecraft" / "textures").is_dir()\n  ```\n\n- The `minecraft_data_pack` fixture returns the path to the extracted vanilla data pack as a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path) instance.\n\n  ```python\n  def test_with_data_pack(minecraft_data_pack):\n      assert minecraft_data_pack.name == "data_pack"\n      assert (minecraft_data_pack / "data" / "minecraft" / "loot_tables").is_dir()\n  ```\n\n## Contributing\n\nContributions are welcome. This project uses [`poetry`](https://python-poetry.org/).\n\n```sh\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`.\n\n```sh\n$ poetry run pytest\n```\n\nThe code follows the [black](https://github.com/psf/black) code style.\n\n```sh\n$ poetry run black .\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/pytest-minecraft/blob/master/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/pytest-minecraft',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
