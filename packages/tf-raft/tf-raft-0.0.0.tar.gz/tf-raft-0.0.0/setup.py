# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tf_raft', 'tf_raft.datasets', 'tf_raft.layers', 'tf_raft.losses']

package_data = \
{'': ['*']}

install_requires = \
['albumentations>=0.4.6,<0.5.0',
 'tensorflow-addons>=0.11.1,<0.12.0',
 'tensorflow>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'tf-raft',
    'version': '0.0.0',
    'description': 'RAFT (Recurrent All Pairs Field Transforms for Optical Flow) implementation via tf.keras',
    'long_description': None,
    'author': 'Daigo Hirooka',
    'author_email': 'daigo.hirooka@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
