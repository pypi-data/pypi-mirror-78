# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mangoapi', 'pytaku', 'pytaku.database', 'pytaku.database.migrations']

package_data = \
{'': ['*'],
 'pytaku': ['static/*',
            'static/feathericons/*',
            'static/js/*',
            'static/js/routes/*',
            'static/vendored/*',
            'templates/*']}

install_requires = \
['argon2-cffi>=20.1.0,<21.0.0',
 'flask>=1.1.2,<2.0.0',
 'goodconf>=1.0.0,<2.0.0',
 'gunicorn>=20.0.4,<21.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['pytaku = pytaku:serve',
                     'pytaku-dev = pytaku:dev',
                     'pytaku-generate-config = pytaku:generate_config',
                     'pytaku-migrate = pytaku:migrate',
                     'pytaku-scheduler = pytaku:scheduler']}

setup_kwargs = {
    'name': 'pytaku',
    'version': '0.3.13',
    'description': 'Self-hostable web-based manga reader',
    'long_description': None,
    'author': 'Bùi Thành Nhân',
    'author_email': 'hi@imnhan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
