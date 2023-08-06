# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['myrabbit',
 'myrabbit.commands',
 'myrabbit.contrib',
 'myrabbit.contrib.opentelemetry',
 'myrabbit.core',
 'myrabbit.core.consumer',
 'myrabbit.core.converter',
 'myrabbit.core.publisher',
 'myrabbit.core.serializer',
 'myrabbit.events',
 'myrabbit.events.listen_event_strategy',
 'myrabbit.service',
 'myrabbit.utils']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'orjson>=3.0.0,<4.0.0',
 'pika>=1.1,<2.0',
 'pydantic>=1.4,<2.0',
 'wrapt>=1.12.1,<2.0.0']

extras_require = \
{'telemetry': ['opentelemetry-sdk>=0.12b0,<0.13',
               'opentelemetry-instrumentation>=0.12b0,<0.13']}

setup_kwargs = {
    'name': 'myrabbit',
    'version': '0.1.12',
    'description': 'Python library for microservice messaging via RabbitMq',
    'long_description': None,
    'author': 'asyncee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
