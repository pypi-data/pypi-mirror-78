# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fn_station']

package_data = \
{'': ['*'],
 'fn_station': ['static/fn_station/*',
                'static/fn_station/fontawesome/*',
                'static/fn_station/fontawesome/css/*',
                'static/fn_station/fontawesome/js/*',
                'static/fn_station/fontawesome/less/*',
                'static/fn_station/fontawesome/metadata/*',
                'static/fn_station/fontawesome/scss/*',
                'static/fn_station/fontawesome/sprites/*',
                'static/fn_station/fontawesome/svgs/brands/*',
                'static/fn_station/fontawesome/svgs/regular/*',
                'static/fn_station/fontawesome/svgs/solid/*',
                'static/fn_station/fontawesome/webfonts/*',
                'templates/fn_station/*']}

install_requires = \
['flask-scss>=0.5,<0.6',
 'fn_graph_studio',
 'instant_api',
 'psycopg2>=2.8.4,<3.0.0',
 'sqlalchemy>=1.3.13,<2.0.0']

setup_kwargs = {
    'name': 'fn-station',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'James Saunders',
    'author_email': 'james@businessoptics.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
