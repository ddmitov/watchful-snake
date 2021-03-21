#!/usr/bin/env python3

# Watchful Snake is a MySQL BinLog to Redis Streams Data Pipeline.

# Watchful Snake is licensed under the
# GNU General Public License Version 3.
# Dimitar D. Mitov 2021
# https://github.com/ddmitov/watchful-snake

# Python Standard Library modules:
import json

# PyPI modules:
import redis

# GLOBAL CONSTANTS: #
#####################
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''

PREFIX = 'watchful_snake:mysql'

MYSQL_SETTINGS = {
    'connection': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'tester',
        'passwd': 'tralala'
    },
    'schemas': ['initial_testing'],
    'tables': ['persons']
}


def main():
    redis_server = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD
    )

    try:
        redis_server.set(
            PREFIX + ':settings',
            json.dumps(MYSQL_SETTINGS)
        )
    except (ConnectionRefusedError, redis.ConnectionError):
        print('No Redis!')
        exit(1)

    redis_server.close()


if __name__ == '__main__':
    main()
