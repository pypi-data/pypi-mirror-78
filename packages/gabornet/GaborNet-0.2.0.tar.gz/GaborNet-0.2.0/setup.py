# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['GaborNet', 'GaborNet.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'torch>=1.6.0,<2.0.0', 'torchvision>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'gabornet',
    'version': '0.2.0',
    'description': 'Meet Gabor Layer',
    'long_description': '# GaborNet\n\n[![PyPI-Status][pypi-image]][pypi-url]\n[![Build Status][travis-badge]][travis-url]\n[![LICENSE][license-image]][license-url]\n[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/iKintosh/GaborNet/?ref=repository-badge)\n\n## Installation\n\nGaborNet can be installed via pip from Python 3.7 and above:\n\n```bash\npip install GaborNet\n```\n\n## Getting started\n\n```python\nimport torch\nimport torch.nn as nn\nfrom torch.nn import functional as F\nfrom GaborNet import GaborConv2d\n\ndevice = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")\n\n\nclass GaborNN(nn.Module):\n    def __init__(self):\n        super(GaborNN, self).__init__()\n        self.g0 = GaborConv2d(in_channels=1, out_channels=96, kernel_size=(11, 11))\n        self.c1 = nn.Conv2d(96, 384, (3,3))\n        self.fc1 = nn.Linear(384*3*3, 64)\n        self.fc2 = nn.Linear(64, 2)\n\n    def forward(self, x):\n        x = F.leaky_relu(self.g0(x))\n        x = nn.MaxPool2d()(x)\n        x = F.leaky_relu(self.c1(x))\n        x = nn.MaxPool2d()(x)\n        x = x.view(-1, 384*3*3)\n        x = F.leaky_relu(self.fc1(x))\n        x = self.fc2(x)\n        return x\n\nnet = GaborNN().to(device)\n\n```\n\nOriginal research paper (preprint): https://arxiv.org/abs/1904.13204\n\nThis research on deep convolutional neural networks proposes a modified\narchitecture that focuses on improving convergence and reducing training\ncomplexity. The filters in the first layer of network are constrained to fit the\nGabor function. The parameters of Gabor functions are learnable and updated by\nstandard backpropagation techniques. The proposed architecture was tested on\nseveral datasets and outperformed the common convolutional networks\n\n## Citation\n\nPlease use this bibtex if you want to cite this repository in your publications:\n\n    @misc{gabornet,\n        author = {Alekseev, Andrey},\n        title = {GaborNet: Gabor filters with learnable parameters in deep convolutional\n                   neural networks},\n        year = {2019},\n        publisher = {GitHub},\n        journal = {GitHub repository},\n        howpublished = {\\url{https://github.com/iKintosh/GaborNet}},\n    }\n\n[travis-url]: https://travis-ci.com/iKintosh/GaborNet\n[travis-badge]: https://travis-ci.com/iKintosh/GaborNet.svg?branch=master\n[pypi-image]: https://img.shields.io/pypi/v/gabornet.svg\n[pypi-url]: https://pypi.org/project/gabornet\n[license-image]: https://img.shields.io/badge/License-MIT-yellow.svg\n[license-url]: https://pypi.org/project/gabornet\n',
    'author': 'an.alekseev',
    'author_email': 'alekseev.as@phystech.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iKintosh/GaborNet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
