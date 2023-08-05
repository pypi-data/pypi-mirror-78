# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioddd']

package_data = \
{'': ['*']}

install_requires = \
['uuid>=1.30,<2.0']

setup_kwargs = {
    'name': 'aioddd',
    'version': '1.1.0',
    'description': 'Async Python DDD utilities library.',
    'long_description': "# Async Python DDD utilities library\n\naioddd is an async Python DDD utilities library.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install aiocli.\n\n```bash\npip install aioddd\n```\n\n## Usage\n\n```python\nfrom asyncio import get_event_loop\nfrom typing import Type\nfrom aioddd import NotFoundError, \\\n    Command, CommandHandler, SimpleCommandBus, \\\n    Query, QueryHandler, OptionalResponse, SimpleQueryBus\n\n_products = []\n\nclass StoreProductCommand(Command):\n    def __init__(self, ref: str):\n        self.ref = ref\n\nclass StoreProductCommandHandler(CommandHandler):\n    def subscribed_to(self) -> Type[Command]:\n        return StoreProductCommand\n\n    async def handle(self, command: StoreProductCommand) -> None:\n        _products.append(command.ref)\n\nclass ProductNotFoundError(NotFoundError):\n    _code = 'product_not_found'\n    _title = 'Product not found'\n\nclass FindProductQuery(Query):\n    def __init__(self, ref: str):\n        self.ref = ref\n\nclass FindProductQueryHandler(QueryHandler):\n    def subscribed_to(self) -> Type[Query]:\n        return FindProductQuery\n\n    async def handle(self, query: FindProductQuery) -> OptionalResponse:\n        if query.ref != '123':\n            raise ProductNotFoundError.create(detail={'ref': query.ref})\n        return {'ref': query.ref}\n\nasync def main() -> None:\n    commands_bus = SimpleCommandBus([StoreProductCommandHandler()])\n    await commands_bus.dispatch(StoreProductCommand('123'))\n    query_bus = SimpleQueryBus([FindProductQueryHandler()])\n    response = await query_bus.ask(FindProductQuery('123'))\n    print(response)\n\n\nif __name__ == '__main__':\n    get_event_loop().run_until_complete(main())\n```\n\n## Requirements\n\n- Python >= 3.6\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://github.com/ticdenis/python-aioddd/blob/master/LICENSE)\n",
    'author': 'ticdenis',
    'author_email': 'denisnavarroalcaide@outlook.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ticdenis/python-aioddd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
