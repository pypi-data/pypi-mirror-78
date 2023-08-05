import logging
from pprint import pprint

from yufuquantsdk.clients import RESTAPIClient

# 开启日志
logger = logging.getLogger("yufuquantsdk")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


async def main():
    http_client = RESTAPIClient(
        base_url="http://127.0.0.1:8000/api/v1",
        auth_token="09ee6b65ad1e3ca4ee6f8d10dd584fe624d43fb0",
    )

    result = await http_client.get_robot_config(robot_id=6)
    pprint(result)

    result = await http_client.post_robot_ping(robot_id=6)
    pprint(result)

    result = await http_client.patch_robot_asset_record(
        robot_id=6, data={"total_balance": 10000}
    )
    pprint(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
