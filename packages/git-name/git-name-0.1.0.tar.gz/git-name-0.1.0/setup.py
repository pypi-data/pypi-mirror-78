# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_name', 'git_name.git_name']

package_data = \
{'': ['*']}

install_requires = \
['inflect>=4.1.0,<5.0.0']

entry_points = \
{'console_scripts': ['git-name = git_name.cli:main']}

setup_kwargs = {
    'name': 'git-name',
    'version': '0.1.0',
    'description': 'a cli and python package for naming hashes',
    'long_description': '# git-name\n\na git extension and python package for turning hashes into memorable names\n\n# install\n\nfrom pypi\n\n`pip install git-name`\n\nor from github master\n\n`pip install git+https://github.com/CircArgs/git-name.git`\n\n# Usage\n\n## shell\n\n```shell\nCircArgs $ git name -h\nusage: git name [-h] [-f] [-l LENGTH] word_or_hash\n\nconvert hashes to memorable names\n\npositional arguments:\n  word_or_hash\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -f, --from            `from hash` flag used to denote argument is a hash.\n  -l LENGTH, --length LENGTH\n                        `hash length` (default=7) truncate the input output hash to this length\n\nCircArgs $ git name efa8f31\nten occupied nuts\n\nCircArgs $ git name -f "ten occupied nuts"\nefa8f31\n\nCircArgs $ git name -f "five fat frogs"\na42cd68\n\n# use names with git instead of hashes\nCircArgs $ git checkout $(git name -f "five fat frogs")\n```\n\n## python\n\n```python\nfrom git_name import NameGenerator\n\nnum=142152565\n\nng=NameGenerator()\n\nname=ng.generate_name(num)\n\nprint(name)\n# \'eight upward buttons\'\n\nname_num=ng.generate_num(name)\nprint(name_num)\n#142152565\n\nprint(num==name_num)\n#True\n\nprint(ng.generate_hash_from_name(name, 7))\n#8791375\n\nprint(ng.generate_name_from_hash(8791375, 7)\n#\'eight upward buttons\'\n\n\n```\n',
    'author': 'CircArgs',
    'author_email': 'quebecname@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CircArgs/git-name',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
