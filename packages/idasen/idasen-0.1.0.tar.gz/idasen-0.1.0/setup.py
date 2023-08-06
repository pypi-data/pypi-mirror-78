# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idasen']

package_data = \
{'': ['*']}

install_requires = \
['bleak>=0.7.1,<0.8.0', 'pyyaml>=5.3.1,<6.0.0', 'voluptuous>=0.11.7,<0.12.0']

entry_points = \
{'console_scripts': ['idasen = idasen.cli:main']}

setup_kwargs = {
    'name': 'idasen',
    'version': '0.1.0',
    'description': 'ikea IDÅSEN desk API and CLI.',
    'long_description': 'idasen\n######\n\n|PyPi Version| |Build Status| |Documentation Status| |Coverage Status| |Black|\n\nThis is a heavily modified fork of `rhyst/idasen-controller`_.\n\nThe IDÅSEN is an electric sitting standing desk with a Linak controller sold by\nikea.\n\nThe position of the desk can controlled by a physical switch on the desk or\nvia bluetooth using an phone app.\n\nThis is a command line interface written in python to control the Idasen via\nbluetooth from a desktop computer.\n\nSet Up\n******\n\nPrerequisites\n=============\n\nThe desk should be connected and paired to the computer.\n\nInstall\n=======\n\n.. code-block:: bash\n\n    python3.8 -m pip install --upgrade idasen\n\n\nDevelopers Install\n==================\n\nDevelopment is done with `poetry`_, a virtual environment manager.\nFirst, `install poetry`_ using their guide.\n\nThen install all the packages using poetry install:\n\n.. code-block:: bash\n\n    poetry install\n\nTo install this as a command avaliable from the system build the package then\ninstall it with pip:\n\n\n.. code-block:: bash\n\n    poetry build\n    python3.8 -m pip install dist/idasen-0.1.0-py3-none-any.whl\n\nConfiguration\n*************\nConfiguration that is not expected to change frequency can be provided via a\nYAML configuraiton file located at ``~/.config/idasen/idasen.yaml``.\n\nYou can use this command to initialize a new configuartion file:\n\n.. code-block:: bash\n\n    idasen init\n\nConfiguartion options:\n\n* ``mac_address`` - The MAC address of the desk. This is required.\n* ``stand_height`` - The standing height from the floor of the desk in meters.\n* ``sit_height`` - The standing height from the floor of the desk in meters.\n\nDevice MAC addresses can be found using ``blueoothctl`` and blueooth adapter\nnames can be found with ``hcitool dev`` on linux.\n\nUsage\n*****\n\nCommand Line\n============\n\nTo print the current desk height:\n\n.. code-block:: bash\n\n    idasen height\n\nTo monitor for changes to height :\n\n.. code-block:: bash\n\n    idasen monitor\n\nAssuming the config file is populated to move the desk to standing position:\n\n.. code-block:: bash\n\n    idasen stand\n\nAssuming the config file is populated to move the desk to sitting position:\n\n.. code-block:: bash\n\n    idasen sit\n\n.. _poetry: https://python-poetry.org/\n.. _install poetry: https://python-poetry.org/docs/#installation\n.. _rhyst/idasen-controller: https://github.com/rhyst/idasen-controller\n\n.. |PyPi Version| image:: https://badge.fury.io/py/idasen.svg\n   :target: https://badge.fury.io/py/idasen\n.. |Build Status| image:: https://github.com/newAM/idasen/workflows/Tests/badge.svg\n   :target: https://github.com/newAM/idasen/actions\n.. |Coverage Status| image:: https://coveralls.io/repos/github/newAM/idasen/badge.svg?branch=master\n   :target: https://coveralls.io/github/newAM/idasen?branch=master\n.. |Documentation Status| image:: https://readthedocs.org/projects/idasen/badge/?version=latest\n   :target: https://idasen.readthedocs.io/en/latest/?badge=latest\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n\t:target: https://github.com/psf/black',
    'author': 'Alex M.',
    'author_email': 'alexmgit@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/newAM/idasen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
