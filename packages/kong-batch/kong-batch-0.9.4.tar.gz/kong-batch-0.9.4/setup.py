# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kong', 'kong.drivers', 'kong.model']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'coloredlogs>=14.0,<15.0',
 'halo>=0.0.29,<0.0.31',
 'humanfriendly>=8.2,<9.0',
 'jinja2>=2.11.2,<3.0.0',
 'notifiers>=1.2.1,<2.0.0',
 'peewee>=3.13.3,<4.0.0',
 'psutil>=5.7.2,<6.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'pytz>=2020.1,<2021.0',
 'pyyaml>=5.3.1,<6.0.0',
 'schema>=0.7.2,<0.8.0',
 'sh>=1.13.1,<2.0.0',
 'tqdm>=4.48.0,<5.0.0']

extras_require = \
{'ipython': ['ipython>=7.16.1,<8.0.0']}

entry_points = \
{'console_scripts': ['kong = kong.cli:main']}

setup_kwargs = {
    'name': 'kong-batch',
    'version': '0.9.4',
    'description': 'Batch job submission and management tool',
    'long_description': "# Kong ![CI](https://github.com/paulgessinger/kong/workflows/CI/badge.svg) [![codecov](https://codecov.io/gh/paulgessinger/kong/branch/master/graph/badge.svg)](https://codecov.io/gh/paulgessinger/kong) [![pypi](https://img.shields.io/pypi/v/kong-batch)](https://pypi.org/project/kong-batch/) [![docs](https://readthedocs.org/projects/kong-batch/badge/?version=latest)](https://kong-batch.readthedocs.io)\n[Documentation](https://kong-batch.readthedocs.io)\n\n\n\n## What does this do?\nSuppose you use a batch cluster somewhere to run parallel workloads. Normally\nyou'd write dedicated submission code for each type of system and use the\nrelevant shell commands to monitor job progress. How do you keep track\nof what happened to jobs? How do you even keep track of which job did what?\n\nWith kong, you can organize your jobs into *folders* (not actual folders on disk),\nhowever you feel like it. Kong can keep track of job statuses and reports\nthem to you in a clean and organized view. You can manage your jobs \nin kong, kill them, resubmit them, remove them. Kong also normalizes things\nlike where the your job can find scratch space, where to put log files\nand where to put output files. This is done by a set of environment variables\navailable in every job, regardless of backend (called *driver*):\n\nvariable name       | value\n--------------------|------\nKONG_JOB_ID         | Kong-specific job ID (not the batch system one)\nKONG_JOB_OUTPUT_DIR | Where to put output files\nKONG_JOB_LOG_DIR    | Where log files go\nKONG_JOB_NPROC      | How many core your job can use\nKONG_JOB_SCRATCHDIR | scratch dir for the job\n\nYou can write job scripts that are mostly agnostic to which driver is\nused to execute the job. Some things remain specific to your environment,\nespecially things that are implemented on top of the actual batch system. This\nincludes things like licenses, queue names, and any other specific configuration.\nKong allows you to provide arguments like this either via configuration, or on\na job by job basis.\n\n## Interface\n\n### REPL\n\nKong provides a command line like program. If you run\n\n[![asciicast](https://asciinema.org/a/hnBQ7S4GQQj2uGI42kbOQyHw4.svg)](https://asciinema.org/a/hnBQ7S4GQQj2uGI42kbOQyHw4)\n\n\n",
    'author': 'Paul Gessinger',
    'author_email': 'hello@paulgessinger.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paulgessinger/kong/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
