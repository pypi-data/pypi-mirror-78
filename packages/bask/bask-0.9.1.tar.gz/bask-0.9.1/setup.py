# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bask']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1.2,<8.0.0',
 'arviz>=0.9.0,<0.10.0',
 'emcee>=3.0.2,<4.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'scikit-learn>=0.22,<0.23',
 'scikit-optimize>=0.7.4,<0.8.0',
 'scipy>=1.5.2,<2.0.0',
 'tqdm>=4.48.2,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=3.1.2,<4.0.0',
          'numpydoc>=1.1.0,<2.0.0',
          'nbsphinx>=0.7.1,<0.8.0',
          'nbsphinx-link>=1.3.0,<2.0.0']}

entry_points = \
{'console_scripts': ['bask = bask.cli:main']}

setup_kwargs = {
    'name': 'bask',
    'version': '0.9.1',
    'description': 'A fully Bayesian implementation of sequential model-based optimization',
    'long_description': '\n\n\n.. image:: https://github.com/kiudee/bayes-skopt/raw/master/docs/images/header.png\n   :width: 800 px\n   :alt: Bayes-skopt header\n   :align: center\n\n===========\nBayes-skopt\n===========\n\n.. image:: https://mybinder.org/badge_logo.svg\n        :target: https://mybinder.org/v2/gh/kiudee/bayes-skopt/master?filepath=examples\n\n.. image:: https://img.shields.io/pypi/v/bask.svg\n        :target: https://pypi.python.org/pypi/bask\n\n.. image:: https://img.shields.io/travis/kiudee/bayes-skopt.svg\n        :target: https://travis-ci.org/kiudee/bayes-skopt\n\n.. image:: https://readthedocs.org/projects/bayes-skopt/badge/?version=latest\n        :target: https://bayes-skopt.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\nA fully Bayesian implementation of sequential model-based optimization\n\n\n* Free software: Apache Software License 2.0\n* Documentation: https://bayes-skopt.readthedocs.io.\n* Built on top of the excellent `Scikit-Optimize (skopt) <https://github.com/scikit-optimize/scikit-optimize>`__.\n\n\nFeatures\n--------\n\n- A **fully Bayesian** variant of the ``GaussianProcessRegressor``.\n- State of the art information-theoretic acquisition functions, such as the\n  `Max-value entropy search <https://arxiv.org/abs/1703.01968>`__ or\n  `Predictive variance reduction search <https://bayesopt.github.io/papers/2017/13.pdf>`__, for even faster\n  convergence in simple regret.\n- Familiar `Optimizer` interface known from Scikit-Optimize.\n\nInstallation\n------------\n\nTo install the latest stable release it is best to install the version on PyPI::\n\n   pip install bask\n\nThe latest development version of Bayes-skopt can be installed from Github as follows::\n\n   pip install git+https://github.com/kiudee/bayes-skopt\n\nAnother option is to clone the repository and install Bayes-skopt using::\n\n   poetry install\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Karlson Pfannschmidt',
    'author_email': 'kiudee@mail.upb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kiudee/bayes-skopt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
