# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykhipu']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'six>=1.15.0,<2.0.0']

extras_require = \
{':python_version < "3.9"': ['importlib_metadata>=1.7.0,<2.0.0'],
 ':python_version >= "2.7" and python_version < "2.8"': ['mock==3.0.5']}

setup_kwargs = {
    'name': 'pykhipu',
    'version': '0.1.7',
    'description': 'Wrapper for the Khipu payment service API v2.0',
    'long_description': "# PyKhipu\n\nPaquete de Python para el API 2.0 del servicio de pagos Khipu\n\n🇬🇧 Python wrapper for the Khipu payment service API v2.0\n\n![PyPI](https://img.shields.io/pypi/v/pykhipu)\n\n## Sobre Khipu\n\n> [Khipu](https://cl.khipu.com/page/introduccion) permite a las personas y empresas, pagar y cobrar electrónicamente usando sus propias cuentas corrientes o cuentas vista del banco, de manera fácil, rápida y segura. \n\n## Instalación\n\n```bash\npip install pykhipu\n```\n\n## Uso\n\nIguala al API de Khipu en llamadas, ideal para portar código o en casos en que se busque más control sobre los resultados.\n\n```python\nfrom pykhipu.client import Client\n\nclient = Client(receiver_id='1234', secret='abcd')\npayment = client.payments.post('test', 'USD', 100)\nprint(payment.payment_url)\n```\n",
    'author': 'Pablo Albornoz',
    'author_email': 'pablo.albornoz.n@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/fixmycode/pykhipu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
