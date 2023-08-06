# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['signald']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=18.2,<19.0']

setup_kwargs = {
    'name': 'pysignald',
    'version': '0.0.8',
    'description': 'A library that allows communication via the Signal IM service using the signald daemon.',
    'long_description': 'pysignald\n=======\n\n[![PyPI](https://img.shields.io/pypi/v/pysignald.svg)](https://pypi.org/project/pysignald/)\n[![pipeline status](https://gitlab.com/stavros/pysignald/badges/master/pipeline.svg)](https://gitlab.com/stavros/pysignald/commits/master)\n\npysignald is a Python client for the excellent [signald](https://git.callpipe.com/finn/signald) project, which in turn\nis a command-line client for the Signal messaging service.\n\npysignald allows you to programmatically send and receive messages to Signal.\n\nInstallation\n------------\n\nYou can install pysignald with pip:\n\n```\n$ pip install pysignald\n```\n\n\nRunning\n-------\n\nJust make sure you have signald installed. Here\'s an example of how to use pysignald:\n\n\n```python\nfrom signald import Signal\n\ns = Signal("+1234567890")\n\n# If you haven\'t registered/verified signald, do that first:\ns.register(voice=False)\ns.verify("sms code")\n\ns.send_message("+1098765432", "Hello there!")\n\nfor message in s.receive_messages():\n    print(message)\n```\n\nYou can also use the chat decorator interface:\n\n```python\nfrom signald import Signal\n\ns = Signal("+1234567890")\n\n@s.chat_handler("hello there", order=10)  # This is case-insensitive.\ndef hello_there(message, match):\n    # Returning `False` as the first argument will cause matching to continue\n    # after this handler runs.\n    stop = False\n    reply = "Hello there!"\n    return stop, reply\n\n\n# Matching is case-insensitive. The `order` argument signifies when\n# the handler will try to match (default is 100), and functions get sorted\n# by order of declaration secondly.\n@s.chat_handler("hello", order=10)\ndef hello(message, match):\n    # This will match on "hello there" as well because of the "stop" return code in\n    # the function above. Both replies will be sent.\n    return "Hello!"\n\n\n@s.chat_handler(re.compile("my name is (.*)"))  # This is case-sensitive.\ndef name(message, match):\n    return "Hello %s." % match.group(1)\n\n\n@s.chat_handler("")\ndef catch_all(message, match):\n    # This will only be sent if nothing else matches, because matching\n    # stops by default on the first function that matches.\n    return "I don\'t know what you said."\n\ns.run_chat()\n```\n\nVarious\n-------\n\npysignald also supports different socket paths:\n\n```python\ns = Signal("+1234567890", socket_path="/var/some/other/socket.sock")\n```\n\nIt supports TCP sockets too, if you run a proxy. For example, you can proxy signald\'s UNIX socket over TCP with socat:\n\n```bash\n$ socat -d -d TCP4-LISTEN:15432,fork UNIX-CONNECT:/var/run/signald/signald.sock\n```\n\nThen in pysignald:\n\n```python\ns = Signal("+1234567890", socket_path=("your.serveri.ip", 15432))\n```\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/stavros/pysignald/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
