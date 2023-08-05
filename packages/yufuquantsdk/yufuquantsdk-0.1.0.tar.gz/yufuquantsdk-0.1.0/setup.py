# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yufuquantsdk']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.14.2,<0.15.0', 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'yufuquantsdk',
    'version': '0.1.0',
    'description': 'SDK for yufuquant development.',
    'long_description': '# yufuquant SDK\n\nyufuquant SDK 封装了用于和 yufuquant 后端进行交互的常用方法。\n\nyufuquant SDK 目前只支持 Python，由于大多数 API 都是基于 asyncio 的异步 API，因此要求 Python 的最低版本为 Python 3.7，推荐使用 Python 3.8。\n\n## 安装\n\n```bash\n$ pip install yufuquantsdk\n```\n\n## REST API 客户端\n\nREST API 客户端用于和 yufuquant 后端的 RESTful API 进行交互。\n\n```python\nfrom yufuquantsdk.clients import RESTAPIClient\n\nbase_url="https://yufuquant.cc/api/v1" # 系统后端接口地址\nauth_token="xxxxx" # 认证令牌\nrobot_id = 1 # 机器人 id\nrest_api_client = RESTAPIClient(base_url=base_url, auth_token=auth_token)\n\n# 获取机器人配置\nawait rest_api_client.get_robot_config(robot_id)\n\n# 更新机器人的资产信息\ndata = {\n  "total_balance": 5.8\n}\nawait rest_api_client.patch_robot_asset_record(robot_id, data)\n\n# 发送 ping\nawait rest_api_client.post_robot_ping(robot_id)\n```\n\n以下是一个完整的示例：\n\n```python\nimport logging\nfrom pprint import pprint\nfrom yufuquantsdk.clients import RESTAPIClient\n\n\n# 开启日志\nlogger = logging.getLogger("yufuquantsdk")\nlogger.addHandler(logging.StreamHandler())\nlogger.setLevel(logging.DEBUG)\n\nasync def main():\n    http_client = RESTAPIClient(\n        base_url="https://yufuquant.cc/api/v1",\n        auth_token="8g2e470579ba14ea69000859eba6c421b69ff95d",\n    )\n    \n    result = await http_client.get_robot_config(robot_id=1)\n    pprint(result)\n    \n    result = await http_client.post_robot_ping(robot_id=1)\n    pprint(result)\n    \n    result = await http_client.patch_robot_asset_record(\n      robot_id=1, data={"total_balance": 10000}\n    )\n    pprint(result)\n\nif __name__ == "__main__":\n    import asyncio\n    asyncio.run(main())\n```\n\n## Websocket API 客户端\n\nWebsocket API 客户端用于和 yufuquant 后端的 Websocket API 进行交互。\n\n```python\nfrom yufuquantsdk.clients import WebsocketAPIClient\n\nuri="wss://yufuquant.cc/ws/v1/streams/" # 系统后端接口地址\nauth_token="xxxxx" # 认证令牌\ntopics = ["robot#1.ping", "robot#1.log"] # 订阅的话题\nws_api_client = WebsocketAPIClient(uri=uri)\n\n# 认证\nawait ws_api_client.auth(auth_token)\n\n# 订阅话题\nawait ws_api_client.sub(topics)\n\n# 取消话题订阅\nawait ws_api_client.unsub(topics)\n\n# 发送机器人 ping\nawait ws_api_client.robot_ping()\n\n# 发送机器人日志\nawait ws_api_client.robot_log()\n```\n\n以下是一个完整的示例：\n\n```python\nimport logging\nfrom yufuquantsdk.clients import WebsocketAPIClient\n\n# 开启日志\nlogger = logging.getLogger("yufuquantsdk")\nlogger.addHandler(logging.StreamHandler())\nlogger.setLevel(logging.DEBUG)\n\nasync def main():\n    ws_api_client = WebsocketAPIClient(uri="wss://yufuquant.cc/ws/v1/streams/")\n    \n    await ws_api_client.auth("8d2e470575ba04ea69000859eba6c421a69ff95c")\n    await ws_api_client.sub(topics=["robot#1.log"])\n    while True:\n        await ws_api_client.robot_ping()\n        await ws_api_client.robot_log("Test robot log...", level="INFO")\n        await asyncio.sleep(1)\n\nif __name__ == "__main__":\n    import asyncio\n    asyncio.run(main())\n```\n\n',
    'author': 'zmrenwu',
    'author_email': 'zmrenwu@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yufuquant/yufuquant-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
