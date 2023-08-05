# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olliepy',
 'olliepy.utils',
 'reports-templates',
 'reports-templates.regression-error-analysis-report']

package_data = \
{'': ['*'],
 'reports-templates.regression-error-analysis-report': ['css/*',
                                                        'fonts/*',
                                                        'img/*',
                                                        'js/*']}

install_requires = \
['flask>=1.1.0',
 'ipython>=7.0.0',
 'numpy>=1.17.0',
 'pandas>=0.25.0',
 'pycrypto>=2.6.1',
 'scikit-learn>=0.22',
 'scipy>=1.3.0']

setup_kwargs = {
    'name': 'olliepy',
    'version': '0.1.14',
    'description': 'An interactive reporting tool written in python for machine learning experiments that generates interactive reports written in VueJS.',
    'long_description': None,
    'author': 'ahmed.mohamed',
    'author_email': 'hanoush87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
