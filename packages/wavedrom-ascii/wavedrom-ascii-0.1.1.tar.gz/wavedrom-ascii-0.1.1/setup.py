# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wavedrom_ascii']

package_data = \
{'': ['*']}

install_requires = \
['json5>=0.9.5,<0.10.0']

setup_kwargs = {
    'name': 'wavedrom-ascii',
    'version': '0.1.1',
    'description': 'Wavedrom waves and registers for the terminal',
    'long_description': '# Wavedrom ASCII\n\nAn ASCII (actually Unicode) representation of [Wavedrom](https://github.com/wavedrom/wavedrom) waves and bitfields.\n\n## Comparison\n\nExample Wavedrom JSON:\n``` json\n{\n  "signal": [\n    {\n      "name": "clk",\n      "wave": "p......"\n    },\n    {\n      "name": "bus",\n      "wave": "x.34.5x",\n      "data": "head body tail"\n    },\n    {\n      "name": "wire",\n      "wave": "0.1..0."\n    }\n  ]\n}\n```\n\nWavedrom image:\n\n<img src="https://svg.wavedrom.com/{signal:[{name:\'clk\',wave:\'p......\'},{name:\'bus\',wave:\'x.34.5x\',data:\'head body tail\'},{name:\'wire\',wave:\'0.1..0.\'}]}"/>\n\nASCII representation:\n```\n        ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐    \n  clk   ┘    └────┘    └────┘    └────┘    └────┘    └────┘    └────┘    └────\n        ────────────────────╥─────────╥───────────────────╥─────────╥─────────\n  bus   XXXXXXXXXXXXXXXXXXXX║ head    ║ body              ║ tail    ║XXXXXXXXX\n        ────────────────────╨─────────╨───────────────────╨─────────╨─────────\n                            ┌─────────────────────────────┐                   \n  wire  ────────────────────┘                             └───────────────────\n```\n\n\nThe Bitfield example from Wavedrom:\n\n![reg vl](https://svg.wavedrom.com/github/wavedrom/wavedrom/master/test/reg-vl.json5)\n\nWill be rendered as:\n\n```\n31  2928  262524      2019      1514  1211       7 6           0\n┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐\n│ nf  │ mop │v│  lumop  │   rs1   │width│   vd    │0 0 0 0 1 1 1│\n└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘\n```\n',
    'author': 'zegervdv',
    'author_email': 'zegervdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zegervdv/wavedrom-ascii',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
