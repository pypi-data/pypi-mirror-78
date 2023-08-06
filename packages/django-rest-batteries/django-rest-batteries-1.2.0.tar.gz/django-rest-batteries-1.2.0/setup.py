# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rest_batteries']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.8,<4.0.0', 'djangorestframework>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': 'django-rest-batteries',
    'version': '1.2.0',
    'description': 'Build clean APIs with DRF faster',
    'long_description': '[![Build Status](https://travis-ci.org/defineimpossible/django-rest-batteries.svg?branch=master)](https://travis-ci.org/github/defineimpossible/django-rest-batteries)\n[![Coverage](https://codecov.io/gh/defineimpossible/django-rest-batteries/branch/master/graph/badge.svg)](https://codecov.io/gh/defineimpossible/django-rest-batteries)\n\n# Django REST Framework Batteries\n\nBuild clean APIs with DRF faster.\n\n# Overview\n\nHere\'s a quick overview of what the library has at the moment:\n\n- Action-based serializers for ViewSets\n- Two serializers per request/response cycle for ViewSets and GenericAPIViews\n- Action-based permissions for ViewSets\n- Single format for all errors\n\n# Requirements\n\n- Python ≥ 3.6\n- Django (2.2, 3.0)\n- Django REST Framework (3.9, 3.10, 3.11)\n\n# Installation\n\n```bash\n$ pip install django-rest-batteries\n```\n\n# Usage\n\n## Action-based serializers for ViewSets\n\nEach action can have a separate serializer:\n\n```python\nfrom rest_batteries.mixins import RetrieveModelMixin, ListModelMixin\nfrom rest_batteries.viewsets import GenericViewSet\n...\n\nclass OrderViewSet(RetrieveModelMixin,\n                   ListModelMixin,\n                   GenericViewSet):\n    response_action_serializer_classes = {\n        \'retrieve\': OrderSerializer,\n        \'list\': OrderListSerializer,\n    }\n```\n\n## Two serializers per request/response cycle\n\nWe found that more often than not we need a separate serializer for handling request payload and a separate serializer for generating response data.\n\nHow to achieve it in ViewSet:\n\n```python\nfrom rest_batteries.mixins import CreateModelMixin, ListModelMixin\nfrom rest_batteries.viewsets import GenericViewSet\n...\n\nclass OrderViewSet(CreateModelMixin,\n                   ListModelMixin,\n                   GenericViewSet):\n    request_action_serializer_classes = {\n        \'create\': OrderCreateSerializer,\n    }\n    response_action_serializer_classes = {\n        \'create\': OrderResponseSerializer,\n        \'list\': OrderResponseSerializer,\n        \'cancel\': OrderResponseSerializer,\n    }\n```\n\nHow to achieve it in GenericAPIView:\n\n```python\nfrom rest_batteries.generics import CreateAPIView\n...\n\n\nclass OrderCreateView(CreateAPIView):\n    request_serializer_class = OrderCreateSerializer\n    response_serializer_class = OrderResponseSerializer\n```\n\n## Action-based permissions for ViewSets\n\nEach action can have a separate set of permissions:\n\n```python\nfrom rest_batteries.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin\nfrom rest_batteries.viewsets import GenericViewSet\nfrom rest_framework.permissions import AllowAny, IsAuthenticated\n...\n\nclass OrderViewSet(CreateModelMixin,\n                   UpdateModelMixin,\n                   ListModelMixin,\n                   GenericViewSet):\n    action_permission_classes = {\n        \'create\': IsAuthenticated,\n        \'update\': [IsAuthenticated, IsOrderOwner],\n        \'list\': AllowAny,\n    }\n```\n\n## Single format for all errors\n\nWe believe that having a single format for all errors is good practice. This will make the process of displaying and handling errors much simpler for clients that use your APIs.\n\nAny error always will be a JSON object with a message, code (identifier of the error), and field if the error is specific to a particular field. How your response could look like:\n\n```python\n{\n    "errors": [\n        {\n            "message": "Delete or cancel all reservations first.",\n            "code": "invalid"\n        },\n        {\n            "message": "Ensure this field has no more than 21 characters.",\n            "code": "max_length",\n            "field": "address.work_phone"\n        },\n        {\n            "message": "This email already exists",\n            "code": "unique",\n            "field": "login_email"\n        }\n    ]\n}\n```\n\nYou will not have a single format out-of-the-box after installation. You need to add an exception handler to your DRF settings:\n\n```python\nREST_FRAMEWORK = {\n    ...\n    \'EXCEPTION_HANDLER\': \'rest_batteries.exception_handlers.errors_formatter_exception_handler\',\n}\n```\n\n# Credits\n\n- [Django-Styleguide by HackSoftware](https://github.com/HackSoftware/Django-Styleguide) - inspiration\n',
    'author': 'Define Impossible',
    'author_email': 'hi@defineimpossible.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/defineimpossible/django-rest-batteries',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
