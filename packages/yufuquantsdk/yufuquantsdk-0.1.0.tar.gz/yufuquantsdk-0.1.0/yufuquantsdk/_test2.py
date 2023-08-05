import logging
from pprint import pprint

from yufuquantsdk.clients import WebsocketAPIClient

# 开启日志
logger = logging.getLogger("yufuquantsdk")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


async def main():
    ws_api_client = WebsocketAPIClient(uri="ws://127.0.0.1:8000/ws/v1/streams/")

    await ws_api_client.auth("09ee6b65ad1e3ca4ee6f8d10dd584fe624d43fb0")
    await ws_api_client.sub(topics=["robot#1.log"])
    while True:
        await ws_api_client.robot_ping()
        await ws_api_client.robot_log("Test robot log...", level="INFO")
        await asyncio.sleep(1)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
