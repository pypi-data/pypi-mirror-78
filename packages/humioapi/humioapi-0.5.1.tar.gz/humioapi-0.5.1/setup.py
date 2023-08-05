# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['humioapi']

package_data = \
{'': ['*']}

install_requires = \
['aiostream>=0.4.1,<0.5.0',
 'chardet>=3.0.4,<4.0.0',
 'colorama>=0.4.3,<0.5.0',
 'httpx>=0.14.2,<0.15.0',
 'pendulum>=2.1.2,<3.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'snaptime>=0.2.4,<0.3.0',
 'structlog-pretty>=0.2.0,<0.3.0',
 'structlog>=20.1.0,<21.0.0',
 'tqdm>=4.48.2,<5.0.0',
 'tzlocal>=2.1,<3.0']

setup_kwargs = {
    'name': 'humioapi',
    'version': '0.5.1',
    'description': 'A Python library for easy interaction with the Humio API',
    'long_description': '# Humio API (unofficial lib)\n\n> This project requires `Python>=3.6.1`\n\nThis is an unofficial library for interacting with [Humio](https://www.humio.com/)\'s API. If you\'re looking for the official Python Humio library it can be found [here: humiolib](https://github.com/humio/python-humio). This library mostly exists because the official library was incredibly basic back in 2019 when I needed this.\n\n## Installation\n\n    pip install humiocli\n\n## Main features\n\n* Asyncronous and syncronous streaming queries supported by `httpx`.\n* Queryjobs which can be polled once, or until completed.\n* Chainable relative time modifiers (similar to Splunk e.g. `-1d@h-30m`).\n* List repository details (*NOTE*: normal Humio users cannot see repos without read permission).\n* Easy env-variable based configuration.\n* Ingest data to Humio, although you probably want to use Filebeat for anything other than one-off things to your sandbox.\n* CLI companion tool available at [humiocli](https://github.com/gwtwod/humiocli).\n* Create and update parsers.\n* (*Work in progress*) An updateable timeseries, which can follow a moving timewindow using relative modifiers, optionally querying only the changed timewindow since previous update.\n\n## Usage\n\nFor convenience your Humio URL and token should be set in the environment variables `HUMIO_BASE_URL` and `HUMIO_TOKEN`. These can be set in `~/.config/humio/.env` and loaded by `humioapi.loadenv()`.\n\n## Query repositories\n\nCreate an instance of HumioAPI to get started\n\n```python\nimport humioapi\nhumioapi.setup_excellent_logging(\'INFO\')\napi = humioapi.HumioAPI(**humioapi.loadenv())\nrepositories = api.repositories()\n```\n\n## Iterate over syncronouys streaming searches sequentially\n\n```python\nimport humioapi\nhumioapi.setup_excellent_logging(\'INFO\')\napi = humioapi.HumioAPI(**humioapi.loadenv())\nstream = api.streaming_search(\n    query="log_type=trace user=someone",\n    repos=[\'frontend\', \'backend\', \'integration\'],\n    start="-1week@day",\n    stop="now"\n)\nfor event in stream:\n    print(event)\n```\n\n## Itreate over asyncronous streaming searches in parallell, from a syncronous context\n\n```python\nimport asyncio\nimport humioapi\nhumioapi.setup_excellent_logging(\'INFO\')\napi = humioapi.HumioAPI(**humioapi.loadenv())\nloop = asyncio.new_event_loop()\n\ntry:\n    asyncio.set_event_loop(loop)\n    tasks = api.async_streaming_tasks(\n        loop,\n        query="log_type=trace user=someone",\n        repos=[\'frontend\', \'backend\', \'integration\'],\n        start="-1week@day",\n        stop="now",\n        concurrent_limit=10,\n    )\n\n    for event in humioapi.consume_async(loop, tasks):\n        print(event)\nfinally:\n    try:\n        loop.run_until_complete(loop.shutdown_asyncgens())\n    finally:\n        asyncio.set_event_loop(None)\n        loop.close()\n```\n\n## Jupyter Notebook\n\n```python\npew new --python=python36 humioapi\n# run the following commands inside the virtualenv\npip install git+https://github.com/gwtwod/humio-api.git\npip install ipykernel seaborn matplotlib\npython -m ipykernel install --user --name \'python36-humioapi\' --display-name \'Python 3.6 (venv humioapi)\'\n```\n\nStart the notebook by running `jupyter-notebook` and choose the newly created kernel when creating a new notebook.\n\nRun this code to get started:\n\n```python\nimport humioapi\nhumioapi.setup_excellent_logging(\'INFO\')\napi = humioapi.HumioAPI(**humioapi.loadenv())\n\nresults = api.streaming_search(query=\'log_type=trace user=someone\', repos=[\'frontend\', \'backend\'], start="@d", stop="now")\nfor i in results:\n    print(i)\n```\n\nTo get a list of all readable repositories with names starting with \'frontend\':\n\n```python\nrepos = sorted([k for k,v in api.repositories().items() if v[\'read_permission\'] and k.startswith(\'frontend\')])\n```\n\nMaking a timechart (lineplot):\n\n```python\n%matplotlib inline\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport pandas as pd\n\nsns.set(color_codes=True)\nsns.set_style(\'darkgrid\')\n\nresults = api.streaming_search(query=\'log_type=stats | timechart(series=metric)\', repos=[\'frontend\'], start=start, stop=stop)\ndf = pd.DataFrame(results)\ndf[\'_count\'] = df[\'_count\'].astype(float)\n\ndf[\'_bucket\'] = pd.to_datetime(df[\'_bucket\'], unit=\'ms\', origin=\'unix\', utc=True)\ndf.set_index(\'_bucket\', inplace=True)\n\ndf.index = df.index.tz_convert(\'Europe/Oslo\')\ndf = df.pivot(columns=\'metric\', values=\'_count\')\n\nsns.lineplot(data=df)\n```\n',
    'author': 'Jostein Haukeli',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gwtwod/humioapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
