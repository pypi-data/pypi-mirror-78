# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['nb_clean']
install_requires = \
['nbformat>=4.4']

entry_points = \
{'console_scripts': ['nb-clean = nb_clean:main']}

setup_kwargs = {
    'name': 'nb-clean',
    'version': '1.6.0',
    'description': 'Clean Jupyter notebooks for versioning',
    'long_description': '# nb-clean\n\n`nb-clean` cleans Jupyter notebooks of cell execution counts, metadata, outputs,\nand (optionally) empty cells, preparing them for committing to version control.\nIt provides a Git filter to automatically clean notebooks before they are\nstaged, and can also be used as a standalone tool outside Git or with other\nversion control systems. It can determine if a notebook is clean or not, which\ncan be used as a check in your continuous integration pipelines.\n\n## Installation\n\nTo install the latest release from [PyPI], use [pip]:\n\n```bash\npython3 -m pip install nb-clean\n```\n\nAlternately, in Python projects using [Poetry] or [Pipenv] for dependency\nmanagement, add `nb-clean` as a development dependency with\n`poetry add --dev nb-clean` or `pipenv install --dev nb-clean`. `nb-clean`\nrequires Python 3.6 or later.\n\n## Usage\n\n### Cleaning\n\nTo install a filter in an existing Git repository to automatically clean\nnotebooks before they are staged, run the following from the working tree:\n\n```bash\nnb-clean configure-git\n```\n\nThis will configure a filter to remove cell execution counts, metadata, and\noutputs. To also remove empty cells, use:\n\n```bash\nnb-clean configure-git --remove-empty\n```\n\nTo preserve cell metadata, such as that required by tools such as [papermill],\nuse:\n\n```bash\nnb-clean configure-git --preserve-metadata\n```\n\n`nb-clean` will configure a filter in the Git repository in which it is run, and\nwill not mutate your global or system Git configuration. To remove the filter,\nrun:\n\n```bash\nnb-clean unconfigure-git\n```\n\nAside from usage from a filter in a Git repository, you can also clean up a\nJupyter notebook manually with:\n\n```bash\nnb-clean clean -i original.ipynb -o cleaned.ipynb\n```\n\nor by passing the notebook contents on stdin:\n\n```bash\nnb-clean clean < original.ipynb > cleaned.ipynb\n```\n\nTo also remove empty cells, add the `--remove--empty` flag. To preserve cell\nmetadata, add the `--preserve-metadata` flag.\n\n### Checking\n\nYou can check if a notebook is clean with:\n\n```bash\nnb-clean check -i notebook.ipynb\n```\n\nor by passing the notebook contents on stdin:\n\n```bash\nnb-clean check < notebook.ipynb\n```\n\nTo also check for empty cells, add the `--remove--empty` flag. To ignore cell\nmetadata, add the `--preserve-metadata` flag.\n\n`nb-clean` will exit with status code 0 if the notebook is clean, and status\ncode 1 if it is not. `nb-clean` will also print details of cell execution\ncounts, metadata, outputs, and empty cells it finds.\n\n## Copyright\n\nCopyright © 2017-2020 [Scott Stevenson].\n\n`nb-clean` is distributed under the terms of the [ISC licence].\n\n[isc licence]: https://opensource.org/licenses/ISC\n[papermill]: https://papermill.readthedocs.io/\n[pip]: https://pip.pypa.io/\n[pipenv]: https://pipenv.readthedocs.io/\n[poetry]: https://python-poetry.org/\n[pypi]: https://pypi.org/project/nb-clean/\n[scott stevenson]: https://scott.stevenson.io\n',
    'author': 'Scott Stevenson',
    'author_email': 'scott@stevenson.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/srstevenson/nb-clean',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
