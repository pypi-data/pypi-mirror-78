# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mrsr']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.15.4,<2.0.0']

setup_kwargs = {
    'name': 'mrsr',
    'version': '0.1.0',
    'description': '',
    'long_description': '# mrsr\n\n![GitHub](https://img.shields.io/github/license/omadson/mrsr.svg)\n[![PyPI](https://img.shields.io/pypi/v/mrsr.svg)](http://pypi.org/project/mrsr/)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/w/omadson/mrsr.svg)](https://github.com/omadson/mrsr/pulse)\n[![GitHub last commit](https://img.shields.io/github/last-commit/omadson/mrsr.svg)](https://github.com/omadson/mrsr/commit/master)\n[![Downloads](https://pepy.tech/badge/mrsr)](https://pepy.tech/project/mrsr)\n\n\n`mrsr` is a Python module implementing the [Multiresponse Sparse Regression algorithm][1] clustering algorithm.\n\n## instalation\nthe `mrsr` package is available in [PyPI](https://pypi.org/project/mrsr/). to install, simply type the following command:\n```\npip install mrsr\n```\n\n## how to cite mrsr package\nif you use `mrsr` package in your paper, please cite it in your publication.\n```\n@misc{mrsr,\n    author       = "Madson Luiz Dantas Dias",\n    year         = "2019",\n    title        = "mrsr: a Python module implementing the Multiresponse Sparse Regression algorithm.",\n    url          = "https://github.com/omadson/mrsr",\n    institution  = "Federal University of Cear\\\'{a}, Department of Computer Science" \n}\n```\n\n## contributing\n\nthis project is open for contributions. here are some of the ways for you to contribute:\n - bug reports/fix\n - features requests\n - use-case demonstrations\n\nto make a contribution, just fork this repository, push the changes in your fork, open up an issue, and make a pull request!\n\n## contributors\n - [Madson Dias](https://github.com/omadson)\n\n[1]: https://doi.org/10.1109/IJCNN.2006.246933\n[2]: http://scikit-learn.org/\n',
    'author': 'Madson Dias',
    'author_email': 'madsonddias@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/omadson/mrsr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
