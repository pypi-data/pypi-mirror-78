# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kivysome']

package_data = \
{'': ['*']}

install_requires = \
['lastversion==1.2.0',
 'mutapath>=0.16.0,<0.17.0',
 'remotezip>=0.9.2,<0.10.0',
 'semver>=2.10.2,<3.0.0',
 'urllib3>=1.25.7,<2.0.0']

setup_kwargs = {
    'name': 'kivysome',
    'version': '0.2.1',
    'description': 'Font Awesome 5 Icons for Kivy',
    'long_description': '# kivysome\n\n[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/matfax/kivysome/build/master?style=for-the-badge)](https://github.com/matfax/kivysome/actions)\n[![Codecov](https://img.shields.io/codecov/c/github/matfax/kivysome?style=for-the-badge)](https://codecov.io/gh/matfax/kivysome)\n[![Dependabot Status](https://img.shields.io/badge/dependabot-enabled-blue?style=for-the-badge&logo=dependabot&color=0366d6)](https://github.com/matfax/kivysome/network/updates)\n[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/kivysome?style=for-the-badge)](https://libraries.io/pypi/kivysome)\n[![CodeFactor](https://www.codefactor.io/repository/github/matfax/kivysome/badge?style=for-the-badge)](https://www.codefactor.io/repository/github/matfax/kivysome)\n[![security: bandit](https://img.shields.io/badge/security-bandit-purple.svg?style=for-the-badge)](https://github.com/PyCQA/bandit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kivysome?style=for-the-badge)](https://pypi.org/project/kivysome/)\n[![PyPI](https://img.shields.io/pypi/v/kivysome?color=%2339A7A6&style=for-the-badge)](https://pypi.org/project/kivysome/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/kivysome?color=ff69b4&style=for-the-badge)](https://pypistats.org/packages/kivysome)\n[![GitHub License](https://img.shields.io/github/license/matfax/kivysome.svg?style=for-the-badge)](https://github.com/matfax/kivysome/blob/master/LICENSE)\n[![GitHub last commit](https://img.shields.io/github/last-commit/matfax/kivysome?color=9cf&style=for-the-badge)](https://github.com/matfax/kivysome/commits/master)\n\nFont Awesome 5 Icons for Kivy\n\n## Usage\n\n### Enable it\n\n#### Using a version\n\nThis will only work for free versions of Font Awesome.\n\n```python\nimport kivysome \nkivysome.enable(kivysome.LATEST, group=kivysome.FontGroup.REGULAR)\n```\n\n#### Using a kit\n\nThis might be extended to commercial versions of Font Awesome on demand.\n\n##### 1. Generate your kit\n\nGo to [Font Awesome](https://fontawesome.com/kits) and generate your kit there.\nThe specified version is respected.\nFor the moment, only free licenses are supported. \n\n##### 2. Enable it\n\nIn your main.py register your font:\n\n```python\nimport kivysome \nkivysome.enable("https://kit.fontawesome.com/{YOURCODE}.js", group=kivysome.FontGroup.SOLID)\n```\n\n### 3. Use it\n\nIn your `.kv` file or string, reference the short Font Awesome (i.e., without `fa-` prefix) as you can copy them from their website.\n\n```yaml\n#: import icon kivysome.icon\nButton:\n    markup: True # Always turn markup on\n    text: "%s Comment" % icon(\'comment\', 24)\n```\n\n## Caching\n\nKivysome will cache the files in the font folder and not redownload them from GitHub.\nIf a kit is given, however, the kit version will have to be fetched from Font Awesome on every execution.\nIf `kivysome.LATEST` is given, the latest version will also have to be determined from GitHub\'s servers.\nFont packs will only be downloaded if new versions are published, then.\nTo completely avoid regular server access, a pinned version will have to be given.\nThe initial download can also be circumvented by downloading it a single time on the developer\'s machine and publishing\nthe downloaded `fonts` folder with the project. The folder should then contain a `.css`, `.fontd`, and a `.ttf` file\nmatching the pinned Font Awesome version and font group.\n\nCheck the `examples` folder for more insight.\n',
    'author': 'matfax',
    'author_email': 'matthias.fax@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matfax/kivysome',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
