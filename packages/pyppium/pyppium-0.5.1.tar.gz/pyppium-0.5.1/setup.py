# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyppium', 'pyppium.utils']

package_data = \
{'': ['*']}

install_requires = \
['Appium-Python-Client==1.0.2',
 'PyYAML==5.3.1',
 'httpx==0.14.3',
 'loguru==0.5.1']

setup_kwargs = {
    'name': 'pyppium',
    'version': '0.5.1',
    'description': 'Pyppium is a wrapper of Appium-Python-Client for cross mobile testing.',
    'long_description': '# Pyppium\n\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![codecov](https://codecov.io/gh/leomenezessz/pyppium/branch/master/graph/badge.svg)](https://codecov.io/gh/leomenezessz/pyppium)\n[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/leomenezessz/pyppium/blob/master/LICENSE)\n![GitHub Pages Deploy](https://github.com/leomenezessz/pyppium/workflows/GitHub%20Pages%20Deploy/badge.svg?branch=master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\nPyppium is an Appium-Python-Client wrapper for cross mobile testing. It helps you to save your time by reducing complexity, increasing efficiency \nand also avoiding these boring and repetitive work problems. Assists you to focus on what really matters, like your business rules, and provides an\nenvironment to start creating your application\'s screens and your test scenarios as fast as possible.\n\n## Installation\n\n```\n\n$ pip install pyppium\n\n```\n\n## Basic Usage\n\nThe following code will give you the necessary to create a simple flow that searches for components on your application screen and perform an action.\nOthers components are supported based on the Appium usage, so feel free to explore and setup your own custom actions.\n\n```python\n\nfrom pyppium.fetcher import fetch, iOS, Android\n\n\nclass ScreenOne:\n    _button_sign_in = fetch(iOS("id", "buttonSignIn"), Android("id", "button"))\n    _input_username = fetch(iOS("id", "inputUserName"), Android("id", "username"))\n    _input_password = fetch(iOS("id", "InputPassword"), Android("id", "pass"))\n\n    def login(self, username, password):\n        self._input_username.send_keys(username)\n        self._input_password.send_keys(password)\n        self._button_sign_in.click()\n\n    \n```\n\nAfter that, you can use the class above (ScreenOne) to create an specific scenario. \nNote that you need to start Pyppium Driver.\n\n```python\n\nfrom pyppium.driver import PyppiumDriver\nfrom tests.e2e.screens.screen import LoginScreen, WelcomeScreen\n\n\ndef test_android_basic_behaviours():\n    username = "Lully"\n    password = "123456789"\n\n    caps_android ={\n            "platformName": "Android",\n            "automationName": "uiautomator2",\n            "deviceName": "Android Emulator",\n            "appPackage": "com.example.dummy",\n            "appActivity": "MainActivity",\n            "newCommandTimeout": 0,\n    }\n\n\n    PyppiumDriver(caps_android)\n\n    LoginScreen().login(username, password)\n\n    assert username in WelcomeScreen().label_welcome_message()\n\n    PyppiumDriver.quit()\n```\n\n## Documentation\n\n- https://leomenezessz.github.io/pyppium/\n\n## Tests\n\nRun all unity tests.\n\n```\n\n$ tox\n\n``` \n\n## Special Thanks\n \n Pyppium count on many packages for trying to deliver a good framework. And of course, these packages are amazing!\n \n - [Appium-Python-Client](https://pypi.org/project/Appium-Python-Client/)\n - [PyYAML](https://pypi.org/project/PyYAML/)\n - [Pytest](https://pypi.org/project/pytest/)\n - [Assertpy](https://pypi.org/project/assertpy/)\n - [Black](https://pypi.org/project/black/)\n - [Pytest-mock](https://pypi.org/project/pytest-mock/)\n - [Pytest-cov](https://pypi.org/project/pytest-cov/)\n - [Codecov](https://pypi.org/project/codecov/)\n - [Mkdocs](https://pypi.org/project/mkdocs/)\n - [Tox](https://pypi.org/project/tox/) \n - [Mkdocs-material](https://squidfunk.github.io/mkdocs-material/) \n\n## License\n\n The MIT License (MIT)\n Copyright (c) 2020 Leonardo Menezes\n\n Permission is hereby granted, free of charge, to any person obtaining a copy\n of this software and associated documentation files (the "Software"), to deal\n in the Software without restriction, including without limitation the rights\n to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n copies of the Software, and to permit persons to whom the Software is\n furnished to do so, subject to the following conditions:\n\n The above copyright notice and this permission notice shall be included in all\n copies or substantial portions of the Software.\n\n THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\n EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\n MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\n IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,\n DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\n OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE\n OR OTHER DEALINGS IN THE SOFTWARE.\n \n <br/>',
    'author': 'Leonardo Menezes',
    'author_email': 'leonardosmenezes.ssz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leomenezessz/pyppium',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
