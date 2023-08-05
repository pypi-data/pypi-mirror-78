# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unionstation', 'unionstation.core']

package_data = \
{'': ['*']}

install_requires = \
['absl-py==0.10.0',
 'betterproto[compiler]>=2.0.0b1,<3.0.0',
 'boto3>=1.14.44,<2.0.0',
 'opencv-python==4.2.0.34',
 'pandas>=1.1.1,<2.0.0',
 'protobuf>=3.13.0,<4.0.0',
 'pyarrow>=1.0.0,<2.0.0',
 'pycocotools>=2.0.1,<3.0.0',
 'pyspark>=3.0.0,<4.0.0',
 's3fs>=0.4.2,<0.5.0',
 'tabulate>=0.8.7,<0.9.0',
 'tqdm>=4.48.2,<5.0.0',
 'urllib3>=1.25.10,<2.0.0']

setup_kwargs = {
    'name': 'unionstation',
    'version': '0.1.0',
    'description': 'Big ML/DL dataset processing station',
    'long_description': None,
    'author': 'H-AI',
    'author_email': 'dongjian413@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
