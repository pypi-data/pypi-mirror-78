# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flask_threaded_sockets']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'werkzeug>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'flask-threaded-sockets',
    'version': '0.3.1',
    'description': 'Barebones websocket extension for Flask, using Pythonthreading for low-traffic concurrency',
    'long_description': '# Flask-Threaded-Sockets\nBarebones WebSockets for your low-traffic Flask apps.\n\nSimple usage of ``route`` decorator:\n\n```python\nfrom flask import Flask\nfrom flask_threaded_sockets import Sockets, ThreadedWebsocketServer\n\n\napp = Flask(__name__)\nsockets = Sockets(app)\n\n\n@sockets.route(\'/echo\')\ndef echo_socket(ws):\n    while not ws.closed:\n        message = ws.receive()\n        ws.send(message)\n\n\n@app.route(\'/\')\ndef hello():\n    return \'Hello World!\'\n\n\nif __name__ == "__main__":\n    srv = ThreadedWebsocketServer("0.0.0.0", 5000, app)\n    srv.serve_forever()\n```\n\nUsage of `Flask blueprints`:\n\n```python\nfrom flask import Flask, Blueprint\nfrom flask_threaded_sockets import Sockets, ThreadedWebsocketServer\n\n\nhtml = Blueprint(r\'html\', __name__)\nws = Blueprint(r\'ws\', __name__)\n\n\n@html.route(\'/\')\ndef hello():\n    return \'Hello World!\'\n\n@ws.route(\'/echo\')\ndef echo_socket(socket):\n    while not socket.closed:\n        message = socket.receive()\n        socket.send(message)\n\n\napp = Flask(__name__)\nsockets = Sockets(app)\n\napp.register_blueprint(html, url_prefix=r\'/\')\nsockets.register_blueprint(ws, url_prefix=r\'/\')\n\n\nif __name__ == "__main__":\n    srv = ThreadedWebsocketServer("0.0.0.0", 5000, app)\n    srv.serve_forever()\n```\n\nServing WebSockets in Python was really easy, if you used Gevent, AsyncIO, etc. Now it\'s easy if you just want to use a threaded development server.\n\n## Why would you ever want this?\n\n**This should not be used in deployed web apps with lots of requests expected! We developed this library for use in low-traffic IoT devices that benefit from using native Python threads**\n\nAlmost every Python websocket tutorial out there will tell you to use an async library like AsyncIO, Gevent, Tornado etc. For virtually all applications, this is absolutely true. These async libraries allow you to handle a huge number of concurrent requests, even long-running connections like websockets, with minimal overhead.\n\nIn these cases, native threading is heavily discouraged. Most threaded production servers will use a small pool of threads to handle concurrency, and websockets will quickly saturate this pool. Async concurrency libraries get around this by allowing a virtually unlimited number of concurrent requests to be processed.\n\nOne way to use native threads without risking pool saturation would be to spawn a thread *per client*, however it\'s obvious to see why this would be problematic for large public web apps: One thread per client will quickly lead to an infeasible number of native threads, introducing a huge context-switching overhead.\n\nHowever, for small services, such as local WoT devices, this is absolutely fine. If you only expect a small (<50) number of simultaneous connections, native threads are perfectly viable as a concurrency provider. Moreover, unlike most async libraries, you\'re able to easily integrate existing code without having to add `async`/`await` keywords, or monkey-patch libraries. For instrument control, this is ideal. We get the full capabilities of Python threading, and it\'s synchronisation primitives, unmodified use of existing device control code, and no need for monkey-patching.\n\n## Installation\n\nTo install Flask-Sockets, simply:\n\n```pip install flask-threaded-sockets```\n\n## WebSocket interface\n\nThe websocket interface that is passed into your routes is the same as\n[gevent-websocket](https://bitbucket.org/noppo/gevent-websocket).\nThe basic methods are fairly straightforward —\xa0\n``send``, ``receive``, ``send_frame``, and ``close``.\n',
    'author': 'Joel Collins',
    'author_email': 'joel@jtcollins.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/labthings/flask-threaded-sockets',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
