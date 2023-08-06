# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['layer_to_layer_pytorch']

package_data = \
{'': ['*']}

install_requires = \
['rich>=6.1.1,<7.0.0',
 'torch>=1.6.0,<2.0.0',
 'tqdm>=4.48.2,<5.0.0',
 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['layer-to-layer-pytorch = '
                     'layer_to_layer_pytorch.__main__:app']}

setup_kwargs = {
    'name': 'layer-to-layer-pytorch',
    'version': '0.1.0',
    'description': 'PyTorch implementation of L2L execution algorithm',
    'long_description': '# layer-to-layer-pytorch\n\n<div align="center">\n\n[![Build status](https://github.com/TezRomacH/layer-to-layer-pytorch/workflows/build/badge.svg?branch=master&event=push)](https://github.com/TezRomacH/layer-to-layer-pytorch/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/layer-to-layer-pytorch.svg)](https://pypi.org/project/layer-to-layer-pytorch/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/TezRomacH/layer-to-layer-pytorch/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/TezRomacH/layer-to-layer-pytorch/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/TezRomacH/layer-to-layer-pytorch/releases)\n[![License](https://img.shields.io/github/license/TezRomacH/layer-to-layer-pytorch)](https://github.com/TezRomacH/layer-to-layer-pytorch/blob/master/LICENSE)\n\nPyTorch implementation of L2L execution algorithm\n</div>\n\n## 🚀 Features [WIP]\n\n## Installation [Not yet ready]\n\n```bash\npip install layer-to-layer-pytorch\n```\n\nor install with `Poetry`\n\n```bash\npoetry add layer-to-layer-pytorch\n```\n\n## 📈 Releases\n\nYou can see the list of available releases on the [GitHub Releases](https://github.com/TezRomacH/layer-to-layer-pytorch/releases) page.\n\nWe follow [Semantic Versions](https://semver.org/) specification.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/TezRomacH/layer-to-layer-pytorch)](https://github.com/TezRomacH/layer-to-layer-pytorch/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/TezRomacH/layer-to-layer-pytorch/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n### This library\n\n```\n@misc{layer-to-layer-pytorch,\n  author = {Roman Tezikov},\n  title = {PyTorch implementation of L2L execution algorithm},\n  year = {2020},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/TezRomacH/layer-to-layer-pytorch}}\n}\n```\n\n### Original paper\n\n```\n@article{Pudipeddi2020TrainingLN,\n  title={Training Large Neural Networks with Constant Memory using a New Execution Algorithm},\n  author={Bharadwaj Pudipeddi and Maral Mesmakhosroshahi and J. Xi and S. Bharadwaj},\n  journal={ArXiv},\n  year={2020},\n  volume={abs/2002.05645}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'Roman Tezikov',
    'author_email': 'tez.romach@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TezRomacH/layer-to-layer-pytorch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
