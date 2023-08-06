# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indexpy',
 'indexpy.http',
 'indexpy.openapi',
 'indexpy.routing',
 'indexpy.websocket']

package_data = \
{'': ['*']}

install_requires = \
['a2wsgi>=1.0.0,<2.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'jinja2>=2.10.3,<3.0.0',
 'pydantic>=1.6,<2.0',
 'python-multipart>=0.0.5,<0.0.6',
 'pyyaml>=5.3,<6.0',
 'starlette>=0.13.6,<0.14.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0'],
 'full': ['gunicorn>=20.0.4,<21.0.0',
          'requests>=2.24.0,<3.0.0',
          'uvicorn>=0.11.3,<0.12.0'],
 'serve': ['gunicorn>=20.0.4,<21.0.0', 'uvicorn>=0.11.3,<0.12.0'],
 'test': ['requests>=2.24.0,<3.0.0']}

entry_points = \
{'console_scripts': ['index-cli = indexpy.cli:main']}

setup_kwargs = {
    'name': 'index.py',
    'version': '0.12.5',
    'description': 'An easy-to-use asynchronous web framework based on ASGI.',
    'long_description': '<div align="center">\n\n<h1> index.py </h1>\n\n<p>\n中文\n|\n<a href="https://github.com/abersheeran/index.py/tree/master/README-en.md">English</a>\n</p>\n\n<p>\n<a href="https://github.com/abersheeran/index.py/actions?query=workflow%3ATest">\n<img src="https://github.com/abersheeran/index.py/workflows/Test/badge.svg" alt="Github Action Test" />\n</a>\n\n<a href="https://github.com/abersheeran/index.py/actions?query=workflow%3A%22Build+setup.py%22">\n<img src="https://github.com/abersheeran/index.py/workflows/Build%20setup.py/badge.svg" alt="Build setup.py" />\n</a>\n</p>\n\n<p>\n<a href="https://github.com/abersheeran/index.py/actions?query=workflow%3A%22Publish+PyPi%22">\n<img src="https://github.com/abersheeran/index.py/workflows/Publish%20PyPi/badge.svg" alt="Publish PyPi" />\n</a>\n\n<a href="https://pypi.org/project/index.py/">\n<img src="https://img.shields.io/pypi/v/index.py" alt="PyPI" />\n</a>\n</p>\n\n<p>\n<img src="https://img.shields.io/pypi/pyversions/index.py" alt="PyPI - Python Version" />\n</p>\n\n一个基于 Radix Tree 的高性能 web 框架。\n\n<a href="https://index-py.abersheeran.com">Index.py 文档</a>\n\n</div>\n\n---\n\nIndex.py 实现了 [ASGI3](http://asgi.readthedocs.io/en/latest/) 接口，并使用 Radix Tree 进行路由查找。是最快的 Python web 框架之一。一切特性都服务于快速开发高性能的 Web 服务。\n\n- 灵活且高效的路由系统 (基于 Radix Tree)\n- 自动解析请求 & 生成文档 (基于 `pydantic`)\n- 可视化 API 接口 (基于 `ReDoc`, 针对中文字体优化)\n- 非常简单的部署 (基于 `uvicorn` 与 `gunicorn`)\n- 挂载 ASGI/WSGI 应用 (基于 [a2wsgi](https://github.com/abersheeran/a2wsgi/))\n- 进程内后台任务 (基于 `asyncio`)\n- 可使用任何可用的 ASGI 生态\n\n## Install\n\n```bash\npip install -U index.py\n```\n\n或者直接从 Github 上安装最新版本（不稳定）\n\n```bash\npip install -U git+https://github.com/abersheeran/index.py@setup.py\n```\n\n## Quick start\n\n向一个 `.py` 文件写入如下代码并直接执行它，访问 `http://127.0.0.1:4190`。\n\n```python\nfrom indexpy import Index\n\n\napp = Index()\n\n\n@app.router.http("/", method="get")\nasync def homepage(request):\n    return "hello, index.py"\n\n\nif __name__ == "__main__":\n    import uvicorn\n\n    uvicorn.run(app, interface="asgi3", port=4190)\n```\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/index.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
