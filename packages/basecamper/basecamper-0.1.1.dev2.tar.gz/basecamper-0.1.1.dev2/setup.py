# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basecamper',
 'basecamper.grain',
 'basecamper.loss',
 'basecamper.metrics',
 'basecamper.runner']

package_data = \
{'': ['*']}

install_requires = \
['MedPy==0.4.0',
 'numpy==1.18.1',
 'polyaxon==1.1.7post4',
 'sphinx_rtd_theme>=0.4.3,<0.5.0',
 'torch==1.6.0']

setup_kwargs = {
    'name': 'basecamper',
    'version': '0.1.1.dev2',
    'description': 'Training utility library and config manager for Granular Machine Vision research',
    'long_description': '===================\nGranular Basecamper\n===================\n\n\nUtility package for satellite machine learning training\n\n\n* Free software: MIT license\n* Documentation: docs.granular.ai/basecamper.\n\n\nFeatures\n--------\n\n* Polyaxon auto-param capture\n* Configuration enforcement and management for translation into Dione environment\n* Precomposed loss functions and metrics\n\n\nTODO\n----\n\n* Shift build logic from cloudbuild to github actions\n\n\nBuild Details\n-------------\n\n* packages are managed using poetry\n* packages poetry maintains pyproject.toml\n* PRs and commits to `develop` branch trigger a google cloudbuild (image: cloudbuild.yaml, docs: cloudbuild_docs.yaml)\n* Dockerfile builds image by exporting poetry dependencies as tmp_requirements.txt and installing them\n',
    'author': 'Sagar Verma',
    'author_email': 'sagar@granular.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/granularai/basecamper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
