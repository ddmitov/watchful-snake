#!/usr/bin/env python3

# Watchful Snake is a MySQL BinLog to Redis Streams Data Pipeline.

# Watchful Snake is licensed under the
# GNU General Public License Version 3.
# Dimitar D. Mitov 2021
# https://github.com/ddmitov/watchful-snake

# Python Standard Library modules:
from collections import OrderedDict
import json

# PyPI modules:
import asyncio
import aioredis

REDIS_URL = 'redis://localhost:6379/0'
REDIS_STREAM = 'watchful_snake:mysql:initial_testing:persons:insert'


async def redis_stream_reader():
    redis = await aioredis.create_redis(
        REDIS_URL,
        encoding='utf8'
    )

    last_id = '0-0'

    while True:
        events = await redis.xread(
            [REDIS_STREAM],
            timeout=0,
            count=5,
            latest_ids=[last_id]
        )

        for key, id, fields in events:
            fields_json = json.dumps(fields)

            print(key)
            print(id)
            print(fields_json)
            print('==============================')

            last_id = id


if __name__ == '__main__':
    try:
        stream_reader_instance = asyncio.ensure_future(redis_stream_reader())
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        print('\n')
        exit(0)
