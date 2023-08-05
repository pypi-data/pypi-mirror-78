# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cy_weather_api', 'cy_weather_api.models']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.5.0,<2.0.0', 'orjson>=3.0.0,<4.0.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'cy-weather-api',
    'version': '0.1.1',
    'description': 'Caiyun Weather API Python SDK',
    'long_description': '# Caiyun Weather API Python SDK\n\n## Install\n\nPython 3.6+ is required.\n\n```sh\npip install cy-weather-api\n```\n\n## Usage\n\n### Request Caiyun API\n\n```py\nfrom cy_weather_api import CyWeatherAPIClient\n\nclient = CyWeatherAPIClient(token="TAkhjf8d1nlSlspN")\napiResult = client.fetch(lng=101.8551, lat=26.6832, lang="zh_CN", alert=True)\nprint(apiResult.result.hourly.description)\napiResult = client.fetch(lng=-0.2008, lat=51.5024, lang="en_GB")\nprint(apiResult.result.hourly.description)\napiResult = client.fetch(lng=73.9808, lat=40.7648, lang="en_US")\nprint(apiResult.result.hourly.description)\n```\n\nOutput sample:\n\n```\n\xe6\x99\xb4\xef\xbc\x8c\xe4\xbb\x8a\xe5\xa4\xa9\xe6\x99\x9a\xe9\x97\xb420\xe7\x82\xb9\xe9\x92\x9f\xe5\x90\x8e\xe8\xbd\xac\xe5\xb0\x8f\xe9\x9b\xa8\xef\xbc\x8c\xe5\x85\xb6\xe5\x90\x8e\xe5\xa4\x9a\xe4\xba\x91\nclear weather over the next 24 hours\nclear weather, overcast after 20 o\'clock this afternoon, followed by cloudy\n```\n\n### Use our dataclass models\n\nThe default HTTP client is requests, you can other HTTP cient to request API,\nand pass the response dict to our models (based on `dataclasss`):\n\n```py\nfrom cy_weather_api import initFromDict\n\ndata = {\n    "status": "ok",\n    "api_version": "v2.5",\n    "api_status": "active",\n    "lang": "en_US",\n    "unit": "metric",\n    "tzshift": 28800,\n    "timezone": "Asia/Shanghai",\n    "server_time": 1589125757,\n    "location": [39.888888, 116.674501],\n    "result": {"forecast_keypoint": "test forecast_keypoint", "primary": 0},\n}\napiResult = initFromDict(data)\n```\n',
    'author': 'ringsaturn',
    'author_email': 'ringsaturn.me@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/caiyunapp/caiyun-weather-api-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
