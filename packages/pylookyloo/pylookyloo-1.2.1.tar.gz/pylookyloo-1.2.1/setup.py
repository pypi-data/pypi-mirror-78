# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylookyloo']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['lookyloo = pylookyloo:main']}

setup_kwargs = {
    'name': 'pylookyloo',
    'version': '1.2.1',
    'description': 'Python CLI and module for Lookyloo',
    'long_description': "# PyLookyloo\n\nThis is the client API for [Lookyloo](https://github.com/Lookyloo/lookyloo).\n\n## Installation\n\n```bash\npip install pylookyloo\n```\n\n## Usage\n\n* You can use the lookyloo command to enqueue an URL.\n\n```bash\nusage: lookyloo [-h] [--url URL] --query QUERY\n\nEnqueue a URL on Lookyloo.\n\noptional arguments:\n  -h, --help     show this help message and exit\n  --url URL      URL of the instance (defaults to https://lookyloo.circl.lu/,\n                 the public instance).\n  --query QUERY  URL to enqueue.\n  --listing      Should the report be publicly listed.\n  --redirects    Get redirects for a given capture.\n\nThe response is the permanent URL where you can see the result of the capture.\n```\n\n* Or as a library\n\n```python\n\nfrom pylookyloo import Lookyloo\n\nlookyloo = Lookyloo('https://url.of.lookyloo.instance')\nif lookyloo.is_up:  # to make sure it is up and reachable\n\tpermaurl = lookyloo.enqueue('http://url.to.lookup')\n\n```\nYou can add the following paramaters to the enqueue fuction:\n```\n    quiet      Return only the uuid\n    listing    Should the report be publicly listed.\n    user_agent Set your own user agent\n    Depth      Set the analysis depth. Can not be more than in config\n```\nTo retrieve the redirects (json)\n```python\n    redirect = lookyloo.get_redirects(uuid)\n```\nTo retrieve the cookies (json)\n```python\n    cookies = lookyloo.get_cookies(uuid)\n```\nTo retrieve the screenshot (raw)\n```python\n    screen = lookyloo.get_screenshot(uuid)\n```\nTo retrieve the html (raw)\n```python\n    html = lookyloo.get_html(uuid)\n```\nTo retrieve the complete capture(raw)\n```python\n    capture = lookyloo.get_complete_capture(uuid)\n```\n",
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lookyloo/PyLookyloo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
