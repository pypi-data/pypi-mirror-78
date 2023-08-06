# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emoji']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'lxml>=4.5.1,<5.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['emoji-search = emoji.main:main']}

setup_kwargs = {
    'name': 'emoji-search',
    'version': '1.1.0',
    'description': 'The #1 Python tool for miscellaneous emoji info',
    'long_description': '# `emoji-search`\n\n\n[![](https://img.shields.io/pypi/v/emoji-search.svg?style=flat)](https://pypi.org/pypi/emoji-search/)\n[![](https://img.shields.io/pypi/dw/emoji-search.svg?style=flat)](https://pypi.org/pypi/emoji-search/)\n[![](https://img.shields.io/pypi/pyversions/emoji-search.svg?style=flat)](https://pypi.org/pypi/emoji-search/)\n[![](https://img.shields.io/pypi/format/emoji-search.svg?style=flat)](https://pypi.org/pypi/emoji-search/)\n[![](https://img.shields.io/pypi/l/emoji-search.svg?style=flat)](https://github.com/dawsonbooth/emoji-search/blob/master/LICENSE)\n\n\n*The #1 Python tool for miscellaneous emoji info*\n\n\n## Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npip install emoji-search\n```\n\n## Usage\n\nThe following is an example usage of the package:\n\n```python\nfrom random import choice\nfrom emoji import Emoji, categories, search, category\n\ndef random_emoji() -> Emoji:\n    return search(choice(category(choice(categories))))\n\nprint(random_emoji())\n```\n```txt\n\xf0\x9f\xa4\xaf\n```\nYou can also run the tool from the command-line:\n\n```txt\nusage: console.py [-h] [--search SEARCH | --category CATEGORY | --categories | --palette]\n\nSearch for emoji information\n\noptional arguments:\n  -h, --help           show this help message and exit\n  --search SEARCH      Emoji to search for\n  --category CATEGORY  Category to get list of emojis\n  --categories         Get list of emoji categories\n  --palette            Get JSON object of all categories and their emojis\n```\n\n```bash\nemoji-search --search \'\xf0\x9f\x8e\x88\' > balloon.json\n```\nThen check out all the information!\n\n```json\n{\n  "symbol": "\xf0\x9f\x8e\x88",\n  "description": "A balloon on a string, as decorates a birthday party. Generally depicted in red, though WhatsApp\xe2\x80\x99s is pink and Google\xe2\x80\x99s orangish-red.\\nCommonly used to convey congratulations and celebration, especially when wishing someone\xc2\xa0a happy birthday.\\nMicrosoft and Samsung\'s balloons were previously blue;\xc2\xa0SoftBank\'s\xc2\xa0was shown floating in the sky.\\n\\nBalloon was approved as part of Unicode 6.0 in 2010\\nand added to Emoji 1.0 in 2015.\\n",\n  "name": "Balloon",\n  "aliases": ["Party", "Red Balloon"],\n  "apple_name": "Balloon",\n  "unicode_name": "",\n  "vendors": {\n    "Apple": [\n      "iOS 13.3",\n      "iOS 10.2",\n      "iOS 8.3",\n      "iOS 6.0",\n      "iOS 5.1",\n      "iOS 4.0",\n      "iPhone OS 2.2"\n    ],\n    "Google": [\n      "Android 10.0 March 2020 Feature Drop",\n      "Android 8.0",\n      "Android 7.0",\n      "Android 5.0",\n      "Android 4.4",\n      "Android 4.3"\n    ],\n    "Microsoft": [\n      "Windows 10 May 2019 Update",\n      "Windows 10 Anniversary Update",\n      "Windows 10",\n      "Windows 8.1",\n      "Windows 8.0"\n    ],\n    "Samsung": [\n      "One UI 1.5",\n      "One UI 1.0",\n      "Experience 9.0",\n      "Experience 8.0",\n      "TouchWiz 7.1",\n      "TouchWiz 7.0",\n      "TouchWiz Nature UX 2"\n    ],\n    "WhatsApp": ["2.19.352", "2.17"],\n    "Twitter": ["Twemoji 13.0", "Twemoji 1.0"],\n    "Facebook": ["4.0", "3.0", "2.0", "1.0"],\n    "JoyPixels": [\n      "6.0",\n      "5.5",\n      "5.0",\n      "4.5",\n      "4.0",\n      "3.1",\n      "3.0",\n      "2.2",\n      "2.0",\n      "1.0"\n    ],\n    "OpenMoji": ["12.3", "1.0"],\n    "emojidex": ["1.0.34", "1.0.33", "1.0.19", "1.0.14"],\n    "Messenger": ["1.0"],\n    "LG": ["G5", "G3"],\n    "HTC": ["Sense 7"],\n    "Mozilla": ["Firefox OS 2.5"],\n    "SoftBank": ["2014", "2008", "2006", "2004", "2001", "2000"],\n    "Docomo": ["2013"],\n    "au by KDDI": ["Type F", "Type D-3", "Type D-2", "Type D-1"]\n  }\n}\n```\nFeel free to [check out the docs](https://dawsonbooth.github.io/emoji-search/) for more information.\n\n## License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/emoji-search',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
