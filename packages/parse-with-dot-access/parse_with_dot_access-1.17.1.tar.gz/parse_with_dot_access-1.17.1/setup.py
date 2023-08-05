# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['parse']
setup_kwargs = {
    'name': 'parse-with-dot-access',
    'version': '1.17.1',
    'description': 'a fork of parse with dot access',
    'long_description': '# a fork of parse with dot access\n\nA mirror fork of [parse](https://github.com/r1chardj0n3s/parse) with dot notation access. \n\n## Get Started\n\n```bash\npip install parse_with_dot_access\n```\n\n```python\nfrom parse import parse\n\nresult = parse("{lat}, {long}", "12.21254, 105.15564")\nprint(result) # <Result () {\'lat\': \'12.21254\', \'long\': \'105.15564\'}>\nprint(result["lat"]) # 12.21254 \nprint(result.long) # 105.15564\n```\n\n# For comprehensive documentation please refer to [the readme of upstream repo](https://github.com/r1chardj0n3s/parse).\n\n',
    'author': 'Nutchanon Ninyawee',
    'author_email': 'me@nutchanon.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CircleOnCircles/parse',
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
