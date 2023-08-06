# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mesmer',
 'mesmer.extern',
 'mesmer.tests',
 'mesmer.utils',
 'mesmer.utils.tests']

package_data = \
{'': ['*'], 'mesmer': ['data/*']}

install_requires = \
['astropy>=4.0.1,<5.0.0',
 'h5py>=2.10.0,<3.0.0',
 'jax==0.1.74',
 'jaxlib==0.1.52',
 'matplotlib>=3.0.0,<4.0.0',
 'numpy>=1.17,<2.0',
 'pyyaml>=5.3.1,<6.0.0',
 'tox-pyenv>=1.1.0,<2.0.0']

extras_require = \
{'docs': ['sphinx>=3.1.2,<4.0.0',
          'sphinx-astropy>=1.3,<2.0',
          'sphinx-argparse>=0.2.5,<0.3.0',
          'nbsphinx>=0.7.1,<0.8.0',
          'sphinx-math-dollar>=1.1.1,<2.0.0',
          'pandoc>=1.0.2,<2.0.0',
          'recommonmark>=0.6.0,<0.7.0'],
 'test': ['pytest-astropy>=0.8.0,<0.9.0', 'pytest>=5,<6']}

setup_kwargs = {
    'name': 'mesmer',
    'version': '0.0.4.dev0',
    'description': 'mesmer sees through foregrounds',
    'long_description': '[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)\n[![mesmer-master Actions Status](https://github.com/bthorne93/mesmer/workflows/mesmer-master/badge.svg)](https://github.com/bthorne93/mesmer/actions)\n\n# mesmer\n\nPackage to calculate the log probability of foregrounds.\n\n## Description\n\nGiven a dataset $\\mathbf{d}$, this package calculates, and samples from, the maximum \nlikelihood set of foreground parameters, $P(\\mathbf{\\theta}}\\mathbf{d})$.\n\nThis approach has been used in these papers:\n\n1. [Simulated forecasts for primordial B-mode searches in ground-based experiments](https://arxiv.org/abs/1608.00551)\n2. [The Simons Observatory: Science goals and forecasts](https://arxiv.org/abs/1808.07445)\n3. [Removal of Galactic foregrounds for the Simons Observatory primordial gravitational wave search](https://arxiv.org/abs/1905.08888)\n\n## Useage\n\n[An example note book](examples/example.ipynb) is in the `notebooks` folder.\n\nTo add SEDs, edit [the SED functions file](mesmer/seds.py). The likelihood is defined in [the likelihood file](mesmer/likelihood.py).\n\n# License\n\nThis project is Copyright (c) Ben Thorne and licensed under\nthe terms of the BSD 3-Clause license. This package is based upon\nthe [Astropy package template](https://github.com/astropy/package-template)\nwhich is licensed under the BSD 3-clause license. See the licenses folder for\nmore information.\n',
    'author': 'Ben Thorne',
    'author_email': 'bn.thorne@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bthorne93/mesmer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
