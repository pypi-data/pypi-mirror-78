# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['deep_filter']
setup_kwargs = {
    'name': 'deep-filter',
    'version': '1.0.1',
    'description': 'Removes values from nested dicts and lists',
    'long_description': "# deep-filter\nA simple package that filters out values from dicts/lists, including all dicts/lists nested within it.\n\n## Usage\n```python\nfrom deep_filter import deep_filter\nx = {\n    'nope': 69,\n    'yep': [\n        69,\n        {'maybe': None},\n        99\n    ]\n}\ndef filter_func:\n    return value != 69\nresult = deep_filter(x, filter_func)\nprint(result)\n# {'yep': [{}, 99]}\n```\n\n### deep_filter(dict_or_list, filter_func=default_filter_func)\n- **dict_or_list**: A dictionary or list\n- **filter_func**: An optional callback function. It will take a value as an argument, and return `True` if the value will be kept and `False` if not. If omitted, `None` values will be filtered out.\n\nReturns your dict or list, filtered.\n\n## Dev instructions\n\n### Get started\n\n1. Install Python (Python 3.7 works, probably other versions too)\n2. Install [Poetry](https://poetry.eustace.io). Poetry is used to manage dependencies, the virtual environment and publishing to PyPI\n3. Run `poetry install` to install Python package dependencies\n\nI recommend running `poetry config virtualenvs.in-project true`, which makes Poetry store your Python virtual environment inside the project folder. Additionally, it lets VSCode's Python extension detect the virtual environment if you set the `python.pythonPath` setting to `${workspaceFolder}/.venv/bin/python` in your settings.\n\n### Running\n\nTo test if things work, you can run the following command to open the Python REPL. Then you can write Python, such as the usage examples:\n\n```\npoetry run python\n```\n\n### Releasing a new version\n\n1. Consider updating the lockfile by running `poetry update`, then check if thing still work\n2. Bump the version number:\n    ```\n    poetry version <version>\n    ```\n3. Update `CHANGELOG.md`\n4. Build:\n    ```\n    poetry build\n    ```\n5. Commit and create git tag\n6. Create GitHub release with release notes and attach the build files\n7. Publish to PyPi:\n    ```\n    poetry publish\n    ```\n",
    'author': 'kasper.space',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/probablykasper/deep-filter',
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
