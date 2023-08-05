# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diffusor']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'diff-match-patch>=20200713,<20200714',
 'logzero>=1.5.0,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['diffusor = diffusor.diffusor:cli']}

setup_kwargs = {
    'name': 'diffusor',
    'version': '1.1.0',
    'description': "A pure-python diffing utility using Google's diff-match-patch.",
    'long_description': "# Diffusor\n[![CircleCI](https://circleci.com/gh/kobaltcore/diffusor.svg?style=svg)](https://circleci.com/gh/kobaltcore/diffusor)\n[![Downloads](https://pepy.tech/badge/diffusor)](https://pepy.tech/project/diffusor)\n\nA pure-python diffing utility using Google's [diff-match-patch](https://github.com/google/diff-match-patch).\n\nThis is a utility script for a very specific purpose, namely easy generation and application of diffs for Python-centric projects, programmatically from within Python.\n\nThis tool serves exactly two functions:\n1. Create diffs between two versions of the same file\n2. Apply diffs to a file\n\nIt works on a per-file basis.\n\nIf you don't have a specific use case for this, you're probably better off using Git diffs and the ubiquitous Linux `patch` tool. Diffusor exists specifically for easing the patch-apply workflow within Python programs, nothing more, nothing less.\n\n## Installation\nDiffusor can be installed via pip:\n```bash\n$ pip install diffusor\n```\n\nPlease note that Diffusor requires Python 3 and will not provide backwards compatibility for Python 2 for the foreseeable future.\n\n## Usage\nTo create a diff:\n```bash\ndiffusor diff <source_file> <modified_file> -n <target_file>\n```\n\nTo apply a diff:\n```bash\ndiffusor apply <patch_file> -t <target_file>\n```\n\n### Command Line Interface\n```\nUsage: diffusor.py [OPTIONS] COMMAND [ARGS]...\n\n  A pure-python diffing utility using Google's diff-match-patch.\n\n  This tool serves exactly two functions:\n  1. Create diffs between two versions of the same file\n  2. Apply diffs to a file\n\n  Commands can be abbreviated by the shortest unique string.\n\n  For example:\n      diff -> d\n      apply -> a\n\n  Examples of full commands:\n      diffusor diff <source_file> <modified_file> -n <target_file>\n      diffusor apply <patch_file> -t <target_file>\n\nOptions:\n  -d, --debug / -nd, --no-debug  Print debug information or only regular\n                                 output\n\n  --help                         Show this message and exit.\n\nCommands:\n  apply\n  diff\n```\n",
    'author': 'CobaltCore',
    'author_email': 'cobaltcore@yandex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kobaltcore/diffusor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
