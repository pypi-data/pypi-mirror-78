# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['karmabot', 'karmabot.commands', 'karmabot.db']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.17,<2.0.0',
 'feedparser==5.2.1',
 'humanize>=2.4.0,<3.0.0',
 'importlib-metadata>=1.6.1,<2.0.0',
 'psycopg2>=2.8.5,<3.0.0',
 'pyjokes>=0.6.0,<0.7.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'slackclient==1.3.1']

entry_points = \
{'console_scripts': ['karmabot = karmabot.main:main']}

setup_kwargs = {
    'name': 'karmabot',
    'version': '1.1',
    'description': 'A bot for Slack',
    'long_description': '# PyBites Karmabot - A Python based Slack Chatbot\n\n[![Tests](https://github.com/pogross/karmabot/workflows/Tests/badge.svg)](https://github.com/pogross/karmabot/actions?workflow=Tests) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![BCH compliance](https://bettercodehub.com/edge/badge/pybites/karmabot?branch=master)](https://bettercodehub.com/) [![codecov](https://codecov.io/gh/pogross/karmabot/branch/hypermodern-karmabot/graph/badge.svg)](https://codecov.io/gh/pogross/karmabot)\n\n**A Python based Slack Chatbot for Community interaction**\n\n## Features\n\nKarmabot\'s main features is the management of Karma within the slack community server. You can give karma, reduce karma, check your current karma points and manage your karma related username.\n\n![karma example](https://www.pogross.de/uploads/karmabot.png)\n\nhttps://www.youtube.com/watch?v=Yx9qYl6lmzM&amp;t=2s\n\nAdditional commands / features are:\n\n- Jokes powered by [PyJokes](https://github.com/pyjokes/pyjokes)\n- Overview on top channels of the slack server\n- Random Python tip, quote or nugget from CodeChalleng.es\n- Browse and search python documentation, "pydoc help"\n\n## Installation\n\n`pip install karmabot`\n\n## Basic Usage\n\nAfter installing you can start karmabot by using the command\n\n```bash\nkarmabot\n```\n\nHowever, you need to supply some settings prior to this.\n\n### Settings\n\nBy default we will look for a `.karmabot` file in the directory you used the `karmabot` command. The file should supply the following information.\n\n```env\nKARMABOT_SLACK_USER=\nKARMABOT_SLACK_TOKEN=\nKARMABOT_SLACK_INVITE_USER_TOKEN=\nKARMABOT_DATABASE_URL=\nKARMABOT_GENERAL_CHANNEL=\nKARMABOT_ADMINS=\n```\n\n- KARMABOT_SLACK_USER\n  The [bot\'s slack user id](https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace).\n\n- KARMABOT_SLACK_TOKEN\n  The [auth toke](https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace) for your bot\n\n- KARMABOT_SLACK_INVITE_USER_TOKEN\n  An invite token to invite the bot to new channels. Bots cannot autojoin channels, but we implemented an invite procedure for this.\n\n- KARMABOT_DATABASE_URL\n  The database url which should be compatible with SqlAlchemy. For the provided docker file use postgres://user42:pw42@localhost:5432/karmabot\n\n- KARMABOT_GENERAL_CHANNEL\n  The channel id of your main channel slack\n\n- KARMABOT_ADMINS\n  The [slack user ids](https://api.slack.com/methods/users.identity) of the users that should have admin command access separated by commas.\n\nIf you do not want to use a file you have to provide environment variables with the above names. If no file is present we default to environment variables.\n\n## Development pattern for contributors\n\nWe use [poetry](https://github.com/python-poetry/poetry) and `pyproject.toml` for managing packages, dependencies and some settings.\n\n### Setup virtual environment for development\n\nYou should follow the [instructions](https://github.com/python-poetry/poetry) to get poetry up and running for your system. We recommend to use a UNIX-based development system (Linux, Mac, WSL). After setting up poetry you can use `poetry install` within the project folder to install all dependencies.\n\nThe poetry virtual environment should be available in the the project folder as `.venv` folder as specified in `poetry.toml`. This helps with `.venv` detection in IDEs.\n\n### Testing and linting\n\nFor testing you need to install [nox](https://nox.thea.codes/en/stable/) separately from the project venv created by poetry. For testing just use the `nox` command within the project folder. You can run all the nox sessions separately if need, e.g.,\n\n- only linting `nox -rs lint`\n- only testing `nox -rs test`\n\nFor different sessions see the `nox.py` file. Please make sure all tests and checks pass before opening pull requests!\n\n### [pre-commit](https://pre-commit.com/)\n\nTo ensure consistency you can use pre-commit. `pip install pre-commit` and after cloning the karmabot repo run `pre-commit install` within the project folder.\n\nThis will enable pre-commit hooks for checking before every commit.\n',
    'author': 'PyBites',
    'author_email': 'info@pybit.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PyBites-Open-Source/karmabot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
