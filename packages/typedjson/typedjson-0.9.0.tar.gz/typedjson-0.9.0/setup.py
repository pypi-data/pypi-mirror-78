# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typedjson']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7,<4.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6.0,<0.7.0']}

setup_kwargs = {
    'name': 'typedjson',
    'version': '0.9.0',
    'description': 'JSON decoding for Python with type hinting (PEP 484)',
    'long_description': "# typedjson\n\n[![License][license-badge]][license]\n[![Pypi][pypi-badge]][pypi]\n[![CI][ci-badge]][ci]\n\nJSON decoding for Python with type hinting (PEP 484).\n\n\n## Requirements and Restrictions\n\n- Python >= 3.6\n- Use non-generic or parameterized class to decode JSON.\n- Use type hints without forward references.\n\n\n## Features\n\n- Support decoding types as below:\n    - primitive types like `str`, `int`, `float`, `bool` and `None`.\n    - `Union` and `Optional`.\n    - homogeneous and heterogeneous `Tuple` and `List`.\n    - variable-length `Tuple`.\n    - non-generic and parameterized dataclasses.\n- Support API like `json.load` and `json.loads`.\n\n\n## Example\n\n\n```python\nfrom typing import Optional\n\nimport typedjson\nfrom dataclasses import dataclass\n\n\n@dataclass(frozen=True)\nclass NameJson:\n    first: str\n    last: Optional[str]\n\n\n@dataclass(frozen=True)\nclass CatJson:\n    id: str\n    age: int\n    name: Optional[NameJson]\n\n\njson = {\n    'id': 'test-cat',\n    'age': 13,\n    'name': {\n        'first': 'Jiji',\n    },\n}\n\nprint(typedjson.decode(CatJson, json))  # Output: CatJson(id='test-cat', age=13, name=NameJson(first='Jiji', last=None))\n\nprint(typedjson.decode(CatJson, {}))  # Output: DecodingError(TypeMismatch(('id',)))\n```\n\nPlease refer to [test codes](/tests/) for more detail.\n\n\n## Contributions\n\nPlease read [CONTRIBUTING.md](/CONTRIBUTING.md).\n\n\n## TODO\n\n- Prohibit decoding `Set` and `Dict` explicitly.\n- Provide the API document.\n- Explain why typedjson uses undocumented APIs.\n- Explain what typedjson resolves.\n- Improve API to dump like `json.dump` and `json.dumps`.\n    - Provide mypy plugin to check whether the class is encodable as JSON or not with `@typedjson.encodable` decorator.\n- Support type hints with forward reference.\n\n\n[license-badge]: https://img.shields.io/badge/license-MIT-yellowgreen.svg?style=flat-square\n[license]: LICENSE\n[pypi-badge]: https://img.shields.io/pypi/v/typedjson.svg?style=flat-square\n[pypi]: https://pypi.org/project/typedjson/\n[ci-badge]: https://img.shields.io/travis/mitsuse/typedjson-python/master.svg?style=flat-square\n[ci]: https://travis-ci.org/mitsuse/typedjson-python\n[pep-563]: https://www.python.org/dev/peps/pep-0563/\n",
    'author': 'Tomoya Kose',
    'author_email': 'tomoya@mitsuse.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
