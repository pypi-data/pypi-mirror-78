# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxmler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyxmler',
    'version': '0.3.0',
    'description': 'Converts a Python dictionary into a valid XML string',
    'long_description': '[![Build Status](https://travis-ci.org/rtician/pyxmler.svg?branch=master)](https://travis-ci.org/rtician/pyxmler)\n\n# What am I\n\nPy-xmler is a python package for converting python dictionaries into valid XML. Most XML conversion utilities out there don\'t seem to provide any namespace support, which was my main reason for creating this package. Inspiration was drawn from the current most popular dictionary to  XML conversion utility [dicttoxml](https://github.com/quandyfactory/dicttoxml).\n\n# Details\n\nPy-xmler has a very specific api that it abides by and, for now, doesn\'t have very good error handling. Getting namespace support with python dictionaries is not easy so there may be some quirks.\n\nTo be used with this package your dictionary must be formatted in the following way:\n\n```python\nfrom pyxmler import dict2xml\n\nmyDict = {\n\t"RootTag": {\n\t\t"@ns": "soapenv",\n\t\t"@attrs": {\n\t\t\t"xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/"\n\t\t},\n\t\t"childTag": {\n\t\t\t"@attrs": {\n\t\t\t\t"someAttribute": "colors are nice"\n\t\t\t},\n\t\t\t"grandchild": "This is a text tag"\n\t\t}\n\t}\n}\n\nprint(dict2xml(myDict, pretty=True))\n```\n\nWhich will return the following XML:\n\n```xml\n<soapenv:RootTag xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">\n\t<childTag someAttribute="colors are nice">\n\t\t<grandchild>This is a text tag</grandchild>\n\t</childTag>\n</soapenv:RootTag>\n```\n\nAs you can see if a key is given a string rather than a dictionary it becomes a text tag.\n\n# API\n\n### Options\n\n#### @ns\n\nThe namespace option. Adds the supplied namespace to the element.\n\n**Example:**\n\nPython input:\n```python\nmyDict = {\n\t"RootTag": {\n\t\t"@ns": "soapenv"\n\t}\n}\n```\n\nPretty XML Output:\n```xml\n<soapenv:RootTag />\n```\n\n#### @attrs\n\nThe attributes option takes a dictionary of attributes. The key for each becomes the attribute itself, while the value becomes the attribute\'s value.\n\n**Example:**\n\nPython input:\n```python\nmyDict = {\n\t"RootTag": {\n\t\t"@ns": "soapenv",\n\t\t"@attrs": {\n\t\t\t"xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/"\n\t\t}\n\t}\n}\n```\n\nPretty XML Output:\n```xml\n<soapenv:RootTag xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" />\n```\n\n#### @name\n\nChanges the name of the tag.\n\n*Example:*\n\nPython input:\n```python\nmyDict = {\n\t"RootTag": {\n\t\t"@ns": "soapenv",\n\t\t"@attrs": {\n\t\t\t"xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/"\n\t\t},\n\t\t"@name": "SomethingElse"\n\t}\n}\n```\n\nPretty XML Output:\n```xml\n<soapenv:SomethingElse xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" />\n```\n\n#### @value\n\nAllows you to give the tag a string value rather than having nested tags.\n\n**Example:**\n\nPython input:\n```python\nmyDict = {\n\t"RootTag": {\n\t\t"@ns": "soapenv",\n\t\t"@attrs": {\n\t\t\t"xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/"\n\t\t},\n\t\t"@value": "Namespace test",\n\t\t"@name": "SomethingElse"\n\t}\n}\n```\n\nPretty XML Output:\n```xml\n<soapenv:SomethingElse xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">Namespace test</soapenv:SomethingElse>\n```\n\n### Tags\n\nTags are defined by using a key value for the dictionary that does not start with a `@`. For now no syntax checking is being done on tag names, so use this wisely.\n\nThe value of the dictionary key can be either a dictionary or a string. If a dictionary is used you can define a namespace, attributes, name, and value for the tag. If a string is supplied you can only have a basic tag with text content.\n\n**Example:**\n\n```python\n# The following two tags are exactly the same,\n# but defined in a different way\n\nmyDict = {\n\t"SomeTag": {\n\t\t"@value": "Some value"\n\t},\n\t"SomeTag": "Some value"\n}\n```\n\n# Installation\n\nPyxmler is [published to PyPi](https://pypi.org/project/pyxmler/), so installing it is as easy as:\n\n```shell\npip install pyxmler\n```\n',
    'author': 'Ramiro Tician',
    'author_email': 'ramirotician@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rtician/pyxmler',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
