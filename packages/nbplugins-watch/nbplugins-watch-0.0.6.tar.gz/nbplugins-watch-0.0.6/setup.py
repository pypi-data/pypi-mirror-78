# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbplugins_watch']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.5.0,<2.0.0', 'nonebot>=1.6.0,<2.0.0', 'watchgod>=0.6,<0.7']

setup_kwargs = {
    'name': 'nbplugins-watch',
    'version': '0.0.6',
    'description': 'watch and (re)load/remove nonebot plugins from a directory',
    'long_description': '# nonebot-plugins-watch\n![Python3.7 package](https://github.com/ffreemt/nonebot-plugins-watch/workflows/Python3.7%20package/badge.svg) [![codecov](https://codecov.io/gh/ffreemt/nonebot-plugins-watch/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/nonebot-plugins-watch)\n [![PyPI version](https://badge.fury.io/py/nbplugins-watch.svg)](https://badge.fury.io/py/nbplugins-watch)\n\n\n\nhot plug and remove nonebot plugins\n\n### Installation\n\n```pip install nbplugins-watch```\n\nTo validate installation\n```\npython -c "import nbplugins_watch; print(nbplugins_watch.__version__)"\n0.0.6\n```\n\n### Usage\nMake a directory somewhere and place an empty \\_\\_init\\_\\_.py and a plugin file in it.\n\nMonitor the directory in your nonebot runner file, e.g. in  `my_nonebot.py`:\n```python\n\nimport nonebot\nfrom nbplugins_watch import nbplugins_watch\n\nnonebot.load_builtin_plugins()  # optional\nnonebot.load_builtin_plugins("mature-plugin-dir")\n\nplugin_dir_path = r"path_to_plugin_dir"  # absolute or relative path\n\nnbplugins_watch(plugin_dir_path)\n# turn debug on to see what\'s going on\n# nbplugins_watch(plugin_dir_path, debug=True)\n\nnonebot.run()\n\n```\nCreate a file, say fancy_plugin.py if not already there, in the directory above. Edit and test and/or remove the file fancy_plugin.py to your heart\'s content.\n\nNote: <s>if a plugin file contains syntax errors (as opposed to logic errors), you\'ll have to restart nonebot, in other words, nbplugins_watch will cease to work after an uncaught error.</s> nbplugins_watch can recover from syntax errors, in other words, even when a plugin file contains syntax errors (as opposed to logic errors), it just still works.\n\n### Acknowledgments\n\n* Thanks to everyone whose code was used\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/nonebot-plugins-watch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
