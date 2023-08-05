# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hoa', 'hoa.ast', 'hoa.helpers', 'hoa.tools']

package_data = \
{'': ['*'], 'hoa': ['grammars/*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'lark-parser>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['pyhoafparser = hoa.tools.pyhoafparser:main']}

setup_kwargs = {
    'name': 'hoa-utils',
    'version': '0.1.0',
    'description': 'Utilities for the HOA format.',
    'long_description': '<h1 align="center">\n  <b>HOA utils</b>\n</h1>\n\n<p align="center">\n  <a href="https://pypi.org/project/hoa-utils">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/hoa-utils">\n  </a>\n  <a href="https://pypi.org/project/hoa-utils">\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/hoa-utils" />\n  </a>\n  <a href="">\n    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/hoa-utils" />\n  </a>\n  <a href="">\n    <img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/hoa-utils" />\n  </a>\n  <a href="">\n    <img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/hoa-utils" />\n  </a>\n  <a href="https://github.com/whitemech/hoa-utils/blob/master/LICENSE">\n    <img alt="GitHub" src="https://img.shields.io/github/license/whitemech/hoa-utils" />\n  </a>\n</p>\n<p align="center">\n  <a href="">\n    <img alt="test" src="https://github.com/whitemech/hoa-utils/workflows/test/badge.svg">\n  </a>\n  <a href="">\n    <img alt="lint" src="https://github.com/whitemech/hoa-utils/workflows/lint/badge.svg">\n  </a>\n  <a href="">\n    <img alt="docs" src="https://github.com/whitemech/hoa-utils/workflows/docs/badge.svg">\n  </a>\n  <a href="https://codecov.io/gh/whitemech/hoa-utils">\n    <img src="https://codecov.io/gh/whitemech/hoa-utils/branch/master/graph/badge.svg" />\n  </a>\n</p>\n<p align="center">\n  <a href="https://img.shields.io/badge/flake8-checked-blueviolet">\n    <img alt="" src="https://img.shields.io/badge/flake8-checked-blueviolet">\n  </a>\n  <a href="https://img.shields.io/badge/mypy-checked-blue">\n    <img alt="" src="https://img.shields.io/badge/mypy-checked-blue">\n  </a>\n  <a href="https://img.shields.io/badge/isort-checked-yellow">\n    <img alt="" src="https://img.shields.io/badge/isort-checked-yellow">\n  </a>\n  <a href="https://img.shields.io/badge/code%20style-black-black">\n    <img alt="black" src="https://img.shields.io/badge/code%20style-black-black" />\n  </a>\n  <a href="https://www.mkdocs.org/">\n    <img alt="" src="https://img.shields.io/badge/docs-mkdocs-9cf">\n  </a>\n</p>\n\nUtilities for the HOA format.\n\n## Install\n\nThe best way is to install the package from PyPI:\n```\npip install hoa-utils\n```\n\nAlternatively, you can install it from source (master branch):\n```\npip install git+https://github.com/whitemech/hoa-utils.git\n```\n\n## What you\'ll find\n\n- APIs to create and manipulate HOA objects\n- CLI tools to about the HOA format.\n\nThe implementation may not be very stable at the moment.\n\nCurrently, the only supported CLI tool is:\n- `pyhoafparser`: parse and validate a file in HOA format. \n\n\n## Development\n\nIf you want to contribute, here\'s how to set up your development environment.\n\n- Install [Poetry](https://python-poetry.org/)\n- Clone the repository: `git clone https://github.com/whitemech/hoa-utils.git && cd hoa-utils`\n- Install the dependencies: `poetry install`\n\n## Tests\n\nTo run tests: `tox`\n\nTo run only the code tests: `tox -e py3.7`\n\nTo run only the code style checks:\n - `tox -e black-check`\n - `tox -e isort-check`\n - `tox -e flake8`\n \n In `tox.ini` you can find all the test environment supported.\n\n## Docs\n\nTo build the docs: `mkdocs build`\n\nTo view documentation in a browser: `mkdocs serve`\nand then go to [http://localhost:8000](http://localhost:8000)\n\n## Authors\n\n- [Marco Favorito](https://marcofavorito.github.io/)\n- [Francesco Fuggitti](https://francescofuggitti.github.io/)\n\n## License\n\n`hoa-utils` is released under the MIT License.\n\nCopyright 2020 WhiteMech\n',
    'author': 'Marco Favorito',
    'author_email': 'marco.favorito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://whitemech.github.io/hoa-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
