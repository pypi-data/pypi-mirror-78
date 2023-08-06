# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dependenpy']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0']

extras_require = \
{'tests': ['coverage>=5.0.4,<6.0.0',
           'invoke>=1.4.1,<2.0.0',
           'mypy>=0.770,<0.771',
           'pytest>=4.3,<5.0',
           'pytest-randomly>=3.4.1,<4.0.0',
           'pytest-sugar>=0.9.2,<0.10.0',
           'pytest-xdist>=1.26,<2.0']}

entry_points = \
{'archan': ['dependenpy.InternalDependencies = '
            'dependenpy.plugins:InternalDependencies'],
 'console_scripts': ['dependenpy = dependenpy.cli:main']}

setup_kwargs = {
    'name': 'dependenpy',
    'version': '3.3.0',
    'description': 'Show the inter-dependencies between modules of Python packages.',
    'long_description': '# Dependenpy\n\n[![ci](https://github.com/pawamoy/dependenpy/workflows/ci/badge.svg)](https://github.com/pawamoy/dependenpy/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/dependenpy/)\n[![pypi version](https://img.shields.io/pypi/v/dependenpy.svg)](https://pypi.org/project/dependenpy/)\n\nShow the inter-dependencies between modules of Python packages.\n\n`dependenpy` allows you to build a dependency matrix for a set of Python packages.\nTo do this, it reads and searches the source code for import statements.\n\n![demo](demo.svg)\n\n## Requirements\n\nDependenpy requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.8\n\n# make it available globally\npyenv global system 3.6.8\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install dependenpy\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 dependenpy\n```\n\n## Usage (as a library)\n\n```python\nfrom dependenpy import DSM\n\n# create DSM\ndsm = DSM(\'django\')\n\n# transform as matrix\nmatrix = dsm.as_matrix(depth=2)\n\n# initialize with many packages\ndsm = DSM(\'django\', \'meerkat\', \'appsettings\', \'dependenpy\', \'archan\')\nwith open(\'output\', \'w\') as output:\n    dsm.print(format=\'json\', indent=2, output=output)\n\n# access packages and modules\nmeerkat = dsm[\'meerkat\']  # or dsm.get(\'meerkat\')\nfinder = dsm[\'dependenpy.finder\']  # or even dsm[\'dependenpy\'][\'finder\']\n\n# instances of DSM and Package all have print, as_matrix, etc. methods\nmeerkat.print_matrix(depth=2)\n```\n\nThis package was originally design to work in a Django project.\nThe Django package [django-meerkat](https://github.com/Genida/django-meerkat)\nuses it to display the matrices with Highcharts.\n\n## Usage (command-line)\n\n```\nusage: gen-readme-data.py [-d DEPTH] [-f {csv,json,text}] [-g] [-G] [-h]\n                          [-i INDENT] [-l] [-m] [-o OUTPUT] [-t] [-v]\n                          PACKAGES [PACKAGES ...]\n\nCommand line tool for dependenpy Python package.\n\npositional arguments:\n  PACKAGES              The package list. Can be a comma-separated list. Each\n                        package must be either a valid path or a package in\n                        PYTHONPATH.\n\noptional arguments:\n  -d DEPTH, --depth DEPTH\n                        Specify matrix or graph depth. Default: best guess.\n  -f {csv,json,text}, --format {csv,json,text}\n                        Output format. Default: text.\n  -g, --show-graph      Show the graph (no text format). Default: false.\n  -G, --greedy          Explore subdirectories even if they do not contain an\n                        __init__.py file. Can make execution slower. Default:\n                        false.\n  -h, --help            Show this help message and exit.\n  -i INDENT, --indent INDENT\n                        Specify output indentation. CSV will never be\n                        indented. Text will always have new-lines. JSON can be\n                        minified with a negative value. Default: best guess.\n  -l, --show-dependencies-list\n                        Show the dependencies list. Default: false.\n  -m, --show-matrix     Show the matrix. Default: true unless -g, -l or -t.\n  -o OUTPUT, --output OUTPUT\n                        Output to given file. Default: stdout.\n  -t, --show-treemap    Show the treemap (work in progress). Default: false.\n  -v, --version         Show the current version of the program and exit.\n\n```\n\nExample:\n\n```console\n$ # running dependenpy on itself\n$ dependenpy dependenpy -z=\n\n                Module │ Id │0│1│2│3│4│5│6│7│8│\n ──────────────────────┼────┼─┼─┼─┼─┼─┼─┼─┼─┼─┤\n   dependenpy.__init__ │  0 │ │ │ │4│ │ │ │ │2│\n   dependenpy.__main__ │  1 │ │ │1│ │ │ │ │ │ │\n        dependenpy.cli │  2 │1│ │ │1│ │4│ │ │ │\n        dependenpy.dsm │  3 │ │ │ │ │2│1│3│ │ │\n     dependenpy.finder │  4 │ │ │ │ │ │ │ │ │ │\n    dependenpy.helpers │  5 │ │ │ │ │ │ │ │ │ │\n       dependenpy.node │  6 │ │ │ │ │ │ │ │ │3│\n    dependenpy.plugins │  7 │ │ │ │1│ │1│ │ │ │\n dependenpy.structures │  8 │ │ │ │ │ │1│ │ │ │\n\n```\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pawamoy/dependenpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
