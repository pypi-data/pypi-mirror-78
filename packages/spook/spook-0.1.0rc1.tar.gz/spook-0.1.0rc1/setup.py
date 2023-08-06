# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spook']

package_data = \
{'': ['*']}

install_requires = \
['django>=1.11.0',
 'djangorestframework>=3.11.0,<4.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'spook',
    'version': '0.1.0rc1',
    'description': 'Django Rest Framework library to interconnect external APIs',
    'long_description': "# Django Spook\n\nLibrary to interconnect multiple external HTTP APIs as Http Services\n\n## Installation\n\n```bash\npip install spook\n```\n\n## Usage\n\nDeclare your internal model\n\n```python\nclass MyModel(models.Model):\n    name = models.CharField(max_length=16)\n    age = models.IntegerField(default=0)\n```\n\nDeclare a serializer class for your external service\n\n```python\nfrom rest_framework import serializers\n\nclass MyModelSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = MyModel\n        fields = ('name', 'age', )\n```\n\nDeclare a Http Service class\n\n```python\nfrom spook.services import HttpService\n\nclass MyService(HttpService):\n    model = MyModel\n    serializer_class = MyModelSerializer\n    api_url = 'https://my.external/api'\n```\n\nAnd you can instance MyService class and use the methods\n\n```python\nservice = MyService()\n\nresponse = service.list()\ndata = response.data_set.data\nservice.get_queryset(data=data)\n```\n",
    'author': 'Pablo Moreno',
    'author_email': 'pablomoreno.inf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
