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
    'version': '0.1.15',
    'description': '**OlliePy** is a python package which can help the data scientists in evaluating and analysing their machine learning experiments by utilising the power and structure of modern web applications. The data scientist only needs to provide the data and any required information and OlliePy will generate the rest.',
    'long_description': '\n![OlliePy logo](./sphinxSource/source/_static/imgs/logo.png)\n# OlliePy - An alternative approach for evaluating ML models\n> **OlliePy** is a python package which can help the data scientists in\n> evaluating and analysing their machine learning experiments by\n> utilising the power and structure of modern web applications. \n> The data scientist only needs to provide the data and any required \n> information and OlliePy will generate the rest.\n\n### <br/>Get started by following the [**OlliePy** guide](https://ahmed-mohamed-sn.github.io/olliePy/)\n\n### <br/>Error analysis report for regression demo\n![OlliePy demo](./sphinxSource/source/_static/imgs/error-analysis-regression-demo.gif)\n',
    'author': 'ahmed.mohamed',
    'author_email': 'hanoush87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ahmed-mohamed-sn/olliePy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
