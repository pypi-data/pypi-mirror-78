# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gql']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core>=3,<4']

setup_kwargs = {
    'name': 'python-gql',
    'version': '0.1.2',
    'description': 'Python schema-first GraphQL library based on GraphQL-core',
    'long_description': '# python-gql\n\nPython schema-first GraphQL library based on GraphQL-core.\n\n\n## Requirements\n\nPython 3.7+\n\n## Installation\n\n`pip install python-gql`\n\n## Getting start\n\n```python\nimport graphql\nfrom gql import gql, make_schema, query, mutate\n\ntype_defs = gql("""\ntype Query {\n    hello(name: String!): String!\n}\n\ntype Post {\n    author: String!\n    comment: String!\n}\ntype Mutation {\n    addPost(author: String, comment: String): Post!\n}\n""")\n\n\n@query\ndef hello(parent, info, name: str) -> str:\n    return name\n\n\n@mutate\ndef add_post(parent, info, author: str = None, comment: str = None) -> dict:\n    return {\'author\': author, \'comment\': comment}\n\n\nschema = make_schema(type_defs)\n\nq = """\nquery {\n    hello(name: "graphql")\n}\n"""\nresult = graphql.graphql_sync(schema, q)\nprint(result.data)\n\n# result: {\'hello\': \'graphql\'}\n\nq = """\nmutation {\n    addPost(author: "syfun", comment: "This is a good library.") {\n        author\n        comment\n    }\n}\n"""\nresult = graphql.graphql_sync(schema, q)\nprint(result.data)\n\n# result: {\'addPost\': {\'author\': \'syfun\', \'comment\': \'This is a good library.\'}}\n```\n\n## Build schema\n\nThis library is `schema-first`, so you must build a schema explicitly.\n\nHere, we have two methods to build a schema, by `a type definitions` or `a schema file`.\n\n```python\nfrom gql import gql, make_schema\n\ntype_defs = gql("""\ntype Query {\n    hello(name: String!): String!\n}\n""")\n\nschema = make_schema(type_defs)\n```\n\n> `gql` function will check your type definitions syntax.\n\n```python\nfrom gql import make_schema_from_file\n\nschema = make_schema_from_file(\'./schema.graphql\')\n```\n\n## Resolver decorators\n\n> In Python, `decorator` is my favorite function, it save my life!\n\nWe can use `query`, `mutation`, `subscribe` to bind functions to GraphQL resolvers.\n\n```python\n@query\ndef hello(parent, info, name: str) -> str:\n    return name\n```\n\nThese decorators will auto convert the snake function to camel one.\n\n```python\n# add_port => addPost\n@mutate\ndef add_post(parent, info, author: str = None, comment: str = None) -> dict:\n    return {\'author\': author, \'comment\': comment}\n```\n\nWhen the funcation name different from the resolver name, you can give a name argument to these decorators.\n\n```python\n@query(\'hello\')\ndef hello_function(parent, info, name: str) -> str:\n    return name\n```\n\nAbout `subscribe`, please see [gql-subscriptions](gql-subscriptions).\n\n## Enum type decorator\n\nUse `enum_type` decorator with a python Enum class.\n\n```python\nfrom enum import Enum\n\nfrom gql import enum_type\n\n\n@enum_type\nclass Gender(Enum):\n    MALE = 1\n    FEMALE = 2\n```\n\n## Custom Scalar\n\nUse `scalar_type` decorator with a python class.\n\n```python\nfrom gql import scalar_type\n\n\n@scalar_type\nclass JSONString:\n    description = "The `JSONString` represents a json string."\n\n    @staticmethod\n    def serialize(value: Any) -> str:\n        return json.dumps(value)\n\n    @staticmethod\n    def parse_value(value: Any) -> dict:\n        if not isinstance(value, str):\n            raise TypeError(f\'JSONString cannot represent non string value: {inspect(value)}\')\n        return json.loads(value)\n\n    @staticmethod\n    def parse_literal(ast, _variables=None):\n        if isinstance(ast, StringValueNode):\n            return json.loads(ast.value)\n\n        return INVALID\n\n```\n\n\n## Apollo Federation\n\n[Example](https://github.com/syfun/starlette-graphql/tree/master/examples/federation)\n\n[Apollo Federation](https://www.apollographql.com/docs/apollo-server/federation/introduction/)\n\nThanks to [Ariadne](https://ariadnegraphql.org/docs/apollo-federation)\n\n\n## Framework support\n\n- [Starlette GraphQL](https://github.com/syfun/starlette-graphql)\n- [Django GraphQL](https://github.com/syfun/django-graphql)\n',
    'author': 'ysun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/syfun/python-gql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
