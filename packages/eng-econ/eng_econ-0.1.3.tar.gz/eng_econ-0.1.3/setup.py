# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eng_econ']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eng-econ',
    'version': '0.1.3',
    'description': 'This package provides some of the basic functions of engineering economics',
    'long_description': '\n# engineering-economics-basics\n\n## Overview\n\nThis package provides some of the basic functions of engineering economics\n\nYou can find it at: [https://pypi.org/project/eng-econ/](https://pypi.org/project/eng-econ/)\n\n## Install\n\n```\npip install eng_econ\n```\n\n## Usage\n\n```\n# Using uniform_gradient_present_worth_factor as an example\nfrom eng_econ.factors import uniform_gradient_present_worth_factor\nuniform_gradient_present_worth_factor(0.01, 20)\n```\n\n## Documents\n\nSee [https://songyu-wang.github.io/engineering-economics-basics/docs/eng_econ/index.html](https://songyu-wang.github.io/engineering-economics-basics/docs/eng_econ/index.html)\n\n## Test Coverage\n\nsee [https://songyu-wang.github.io/engineering-economics-basics/htmlcov/index.html](https://songyu-wang.github.io/engineering-economics-basics/htmlcov/index.html)\n\n### Reference\n\nNational Council of Examiners for Engineering and Surveying(NCEES). FE Reference Handbook, 9.5 Edition, (ISBN 978-1-932613-67-4).\n',
    'author': 'Songyu-Wang',
    'author_email': 'wangsongyuf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://songyu-wang.github.io/engineering-economics-basics/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
