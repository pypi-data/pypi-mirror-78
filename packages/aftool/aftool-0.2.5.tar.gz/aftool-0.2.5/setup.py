# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aftool']

package_data = \
{'': ['*']}

install_requires = \
['DBUtils>=1.3,<2.0',
 'PyYAML>=5.3.1,<6.0.0',
 'joblib>=0.14.1,<0.15.0',
 'loguru>=0.5.1,<0.6.0',
 'matplotlib>=3.2.0,<4.0.0',
 'numpy>=1.18.0,<2.0.0',
 'pandas>=0.25.3,<0.26.0',
 'pip>=20.0.2,<21.0.0',
 'plotly>=4.9.0,<5.0.0',
 'psutil>=5.6,<6.0',
 'pycryptodome>=3.9.8,<4.0.0',
 'pyecharts>=1.6.2,<2.0.0',
 'pymysql>=0.10.0,<0.11.0',
 'pytest>=5.3.5,<6.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'seaborn>=0.10.0,<0.11.0',
 'snapshot_selenium>=0.0.2,<0.0.3',
 'tqdm>=4.41,<5.0']

setup_kwargs = {
    'name': 'aftool',
    'version': '0.2.5',
    'description': "Asdil Fibrizo's tool",
    'long_description': "# aftool \n[![](https://travis-ci.com/Asdil/aftool.svg?branch=master)](https://travis-ci.com/Asdil/aftool)\n\nAsdil's tool\n",
    'author': 'Asdil Fibrizo',
    'author_email': 'jpl4job@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Asdil/aftool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
