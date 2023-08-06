# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['md_translate']

package_data = \
{'': ['*']}

install_requires = \
['langdetect>=1.0.8,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'translators>=4.7.2,<5.0.0']

entry_points = \
{'console_scripts': ['md-translate = md_translate.app:run']}

setup_kwargs = {
    'name': 'md-translate',
    'version': '2.0.0',
    'description': 'CLI tool to translate markdown files',
    'long_description': '[![codecov](https://codecov.io/gh/ilyachch/md_docs-trans-app/branch/master/graph/badge.svg)](https://codecov.io/gh/ilyachch/md_docs-trans-app)\n# MD Translate\n\nCLI tool to translate `.md` files from English to Russian and back.\n\nCan use Yandex Translation API and Google Cloud translation.\n\n## Installation\n\nInstall project:\n\n```bash\n$ pip install md-translate\n```\n\n## Settings file\n\nYou can store your default settings in `.json` file.\n\nSettings file content example:\n```.json\n{\n  "source_lang": "ru",\n  "target_lang": "en",\n  "service_name": "Google",\n}\n```\n\nIf you set config file, you should specify it with `-c CONFIG_PATH` argument!\n\n## Usage\n\n```bash\n$ md-translate [-h] [-c CONFIG_PATH]\n               [-s {Yandex,Google}] [-S] [-T]\n               [path]\n```\n\nIf you set config file, you can override any of settings by arguments\n\n### Positional arguments:\n* `path` Path to folder to process. If not set, uses current folder\n\n### Optional arguments:\n* `-h, --help`, show this help message and exit\n* `-c CONFIG_PATH, --config_path CONFIG_PATH`, Path to config_file\n* `-s {Yandex,Google,Bing,Deepl}, --service_name {Yandex,Google,Bing,Deepl}`, Translating service\n* `-S SOURCE_LANG, --source_lang SOURCE_LANG`, Source language code\n* `-T TARGET_LANG, --target_lang TARGET_LANG`, Target language code\n\n### Translation services:\nNow used `Yandex`, `Google`, `Bing`, `Deepl`\n\nSome of them can be not working, try it and find the most suitable for you',
    'author': 'Ilya Chichak',
    'author_email': 'ilyachch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ilyachch/md_docs-trans-app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
