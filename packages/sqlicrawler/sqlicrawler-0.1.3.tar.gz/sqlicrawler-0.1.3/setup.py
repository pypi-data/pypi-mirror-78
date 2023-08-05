# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlicrawler']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiohttp>=3.6.2,<4.0.0',
 'aiohttp_socks>=0.5.3,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'pyppeteer>=0.2.2,<0.3.0',
 'ujson>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['sqlicrawler = sqlicrawler:cli']}

setup_kwargs = {
    'name': 'sqlicrawler',
    'version': '0.1.3',
    'description': 'SQLi Crawler with JavaScript support.',
    'long_description': '# SQLiCrawler\n\n**sqlicrawler** - это утилита, созданная для автоматизации поиска sql-инъекций. Она запускает экземпляр браузера Chromium Headless и посещает ссылки на сайте, выполняя скрипты на JavaScript и отправляя формы. Это моя 100500 реализация сканнера уязвимостей.\n\nС целью ускорения загрузки страниц загрузка стилей и изображений блокируется.\n\n![image](https://user-images.githubusercontent.com/12753171/91443290-cd3a6880-e87b-11ea-8ac1-703880a5ebee.png)\n\nТакой паук "видит" страницу выше:\n\n![image](https://user-images.githubusercontent.com/12753171/91443491-168ab800-e87c-11ea-8faf-1f0da95eb987.png)\n\n## Usage\n\n```zsh\n# install the package into a virtual environment and create an executable in the ~/.local/bin directory\n$ pipx install sqlicrawler\n$ sqlicrawler --help\n```\n\nВ качестве значения флага `-i` используется путь до файла, в котором содержится список ссылок (каждая с новой строки) на сайты для сканирования. С помощью флага `-o` задается имя файла в котором будут храниться результаты сканирования. этот файл имеет формат JSONL. Каждая его строка представляет собой сериализованный в JSON объект. Для парсинга файлов такого типа рекомендуется использовать утилиту **jq**.\n\nЕсли Вы хотите заблокировать нежелательные запросы к определенным сайтам, например, к скриптам, собирающим статистику поситетилей сайта, то нужно создать файл `~/.config/sqlicrawler/blacklist.txt`, содержащий шаблоны запрещенных ссылок. Часть имени, содержащую произвольное количество символов можно заменить на `*`.\n\nСессионная информация браузера лежит в `~/.config/sqlicrawler/chrome_profile`.\n\n## Development\n\n```zsh\n$ poetry run pytest -s tests\n```\n',
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
