# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tjax', 'tjax.fixed_point', 'tjax.gradient']

package_data = \
{'': ['*']}

install_requires = \
['chex>=0.0.2,<0.0.3',
 'colorful>=0.5.4,<0.6.0',
 'cooperative_dataclasses>=0.2.0,<0.3.0',
 'jax>=0.1.72,<0.2.0',
 'jaxlib>=0.1.51,<0.2.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.19,<2.0']

setup_kwargs = {
    'name': 'tjax',
    'version': '0.4.3',
    'description': 'Tools for JAX.',
    'long_description': '=============\nTools for JAX\n=============\n\n.. role:: bash(code)\n    :language: bash\n\n.. role:: python(code)\n   :language: python\n\nThis repository implements a variety of tools for the differential programming library\n`JAX <https://github.com/google/jax>`_.  It includes:\n\n- A dataclass decorator that facilitates defining JAX trees, provides convenient text display, and\n  provides a mypy plugin\n\n- A custom VJP decorator that supports both static and non-differentiable arguments\n\n- A random number generator class\n\n- JAX tree registration for `NetworkX <https://networkx.github.io/>`_ graph types\n\n- Testing tools that automatically produce testing code\n\nSee the `documentation <https://neilgirdhar.github.io/tjax/tjax/index.html>`_.\n\nContribution guidelines\n=======================\n\n- Conventions: PEP8.\n\n- How to run tests: :bash:`pytest .`\n\n- How to clean the source:\n\n  - :bash:`isort tjax`\n  - :bash:`pylint tjax`\n  - :bash:`mypy tjax`\n  - :bash:`flake8 tjax`\n',
    'author': 'Neil Girdhar',
    'author_email': 'mistersheik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NeilGirdhar/cmm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
