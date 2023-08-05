# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['argsearch']
install_requires = \
['numpy>=1.19.1,<2.0.0']

entry_points = \
{'console_scripts': ['argsearch = argsearch:main']}

setup_kwargs = {
    'name': 'argsearch',
    'version': '0.1.1',
    'description': 'Run a command many times with different combinations of its inputs.',
    'long_description': '# argsearch\n`argsearch` is a simple and composable tool for running the same command many times with different combinations of arguments.\nIt aims to make random search and grid search easy for things like hyperparameter tuning and setting simulation parameters, while only requiring that your program accepts command line arguments in some form.\n\n## Example\n```\n$ argsearch \'echo {a} {b}\' grid 3 --a 0.0 1.5 --b X Y\n[\n{"args": {"a": "0.0", "b": "X"}, "command": "echo 0.0 X", "stdout": "0.0 X\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "0.0", "b": "Y"}, "command": "echo 0.0 Y", "stdout": "0.0 Y\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "0.75", "b": "X"}, "command": "echo 0.75 X", "stdout": "0.75 X\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "0.75", "b": "Y"}, "command": "echo 0.75 Y", "stdout": "0.75 Y\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "1.5", "b": "X"}, "command": "echo 1.5 X", "stdout": "1.5 X\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "1.5", "b": "Y"}, "command": "echo 1.5 Y", "stdout": "1.5 Y\\n", "stderr": "", "returncode": 0}\n]\n```\n\n## Installation\n\n```\npip install argsearch\n```\n\n## Usage\n\n`argsearch` takes 4 kinds of arguments:\n - A **command string** with **templates** designated by bracketed names (e.g. `\'python my_script.py --flag {value}\'`.\n - A **search strategy** (*random* or *grid*).\n -  A number N defining the **search extent** (for random search, the number of trials to make; for grid search, the number of intervals to divide each range into).\n -  A **range** for each template in the command string (e.g. `--value 1 100`).\n\nThen, `argsearch` runs the command string several times, each time replacing the templates with values from their associated ranges.\n\n### Ranges\n3 kinds of ranges are supported:\n - Float ranges are specified by a minimum and maximum floating-point value (e.g. `--value 0.0 1.0`).\n - Integer ranges are specified by a minimum and maximum integer (e.g. `--value 1 100`). Integer ranges are guaranteed to only yield integer values.\n - Categorical ranges are specified by a list of non-numeric categories, or more than two numbers (e.g. `--value A B C`, `--value 2 4 8 16`). Categorical ranges only draw values from the listed categories, and are not divided up during a grid search.\n\nNote that values are sampled uniformly, so if you think of your range as log-uniform this sampling behavior may not work well.\n\n### Output\n\nThe output is JSON, which can be wrangled with [jq](https://github.com/stedolan/jq) or other tools, or dumped to a file. The run is a list of mappings, one per command call, each of which has the following keys:\n - `args`: a mapping of argument names to values.\n - `command`: the command string with substitutions applied.\n - `stdout`: a string containing the command\'s stdout.\n - `stderr`: a string containing the command\'s stderr.\n - `returncode`: an integer return code for the command.\n',
    'author': 'Aidan Swope',
    'author_email': 'aidanswope@gmail.com',
    'maintainer': 'Aidan Swope',
    'maintainer_email': 'aidanswope@gmail.com',
    'url': 'https://github.com/maxwells-daemons/argsearch',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
