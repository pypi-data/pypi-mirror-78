# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faust_avro', 'faust_avro.parsers']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0',
 'fastavro>=0.22.5,<0.23.0',
 'faust>=1.10,<2.0',
 'funcy>=1.13,<2.0',
 'typing-inspect>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'faust-avro',
    'version': '0.4.1',
    'description': 'Avro codec and schema registry support for Faust',
    'long_description': '[![Maintainability](https://api.codeclimate.com/v1/badges/13676d472164ce8b3699/maintainability)](https://codeclimate.com/github/masterysystems/faust-avro/maintainability)\n\n[![Test Coverage](https://api.codeclimate.com/v1/badges/13676d472164ce8b3699/test_coverage)](https://codeclimate.com/github/masterysystems/faust-avro/test_coverage)\n\n# Faust Avro\n\nAvro codec and schema registry support for Faust.\n\n## Getting Started\n\n### First Time Setup\n\n* Get [asdf](https://asdf-vm.com/#/core-manage-asdf-vm?id=install-asdf-vm)\n* Install python: `asdf install python`\n* Get [poetry](https://poetry.eustace.io/docs/)\n  * `curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python`\n  * As with any code asking you to do this from the internet, you should really first download get-poetry.py and inspect it to make sure it doesn\'t do anything bad, then run the copy you inspected.\n  * Or you can just `pip install poetry` to stick it inside the main python install by asdf. If you switch python versions and get errors about reshimming poetry, that version of python doesn\'t have poetry installed.\n\n### Install needed packages\n\n`poetry install`\n\n### Activate environment\n\nMost directions here assume you have the poetry-created virtualenv active. Some form of `source .venv/bin/activate` (or `source .venv/bin/activate.(csh|fish)`) should activate the environment for you, or you can configure your shell to auto-activate, eg:\n\n```\n$ cat ~/.config/fish/functions/cd.fish\n#!/bin/env fish\n\nfunction cd -d "change directory, and activate virtualenvs, if available"\n    # first and foremost, change directory\n    builtin cd $argv\n\n    # find a parent git directory\n    if git rev-parse --show-toplevel >/dev/null ^/dev/null\n        set gitdir (realpath (git rev-parse --show-toplevel))\n    else\n        set gitdir ""\n    end\n\n    # if that directory contains a virtualenv in a ".venv" directory, activate it\n    if test \\( -z "$VIRTUAL_ENV" -o "$VIRTUAL_ENV" != "$gitdir/.venv" \\) -a -f "$gitdir/.venv/bin/activate.fish"\n        source $gitdir/.venv/bin/activate.fish\n    end\n\n    # deactivate an active virtualenv if not int a git directory with an ".venv"\n    if test -n "$VIRTUAL_ENV" -a "$VIRTUAL_ENV" != "$gitdir/.venv"\n        deactivate\n    end\nend\n```\n\n### Add pre-commit hooks\n\nInstall git pre-commit hooks via `pre-commit install`. These will auto-run black and isort to ensure your code is pretty no matter what editor you use. This must be done inside an activated environment.\n\n### Running tests\n\n`pytest`\n',
    'author': 'Mastery Systems LLC',
    'author_email': 'oss@mastery.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/masterysystems/faust-avro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
