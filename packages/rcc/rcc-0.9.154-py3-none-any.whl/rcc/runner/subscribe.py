'''Subscribe to a channel (with XREAD)

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.
'''

import logging
import traceback

import click
from rcc.client import RedisClient
from rcc.subscriber import RedisSubscriberMessageHandlerClass, runSubscriber
from datetime import datetime, timedelta


class Throttle(object):
    def __init__(self, seconds: int = 1, minutes: int = 0, hours: int = 0) -> None:
        self.throttle_period = timedelta(seconds=seconds, minutes=minutes, hours=hours)
        self.time_of_last_call = datetime.min

    def exceedRate(self) -> bool:
        now = datetime.now()
        time_since_last_call = now - self.time_of_last_call

        if time_since_last_call > self.throttle_period:
            self.time_of_last_call = now
            return False
        else:
            return True


class MessageHandlerClass(RedisSubscriberMessageHandlerClass):
    def __init__(self, obj):
        self.cnt = 0
        self.cntPerSec = 0

        self.throttle = Throttle(seconds=1)

    def log(self, msg):
        print(msg)

    async def on_init(self, initInfo):
        if not initInfo.get('success', False):
            print('Failure connecting to redis')
        else:
            print(f'initInfo: {initInfo}')

    async def handleMsg(self, msg: str, position: str, payloadSize: int) -> bool:
        self.cnt += 1
        self.cntPerSec += 1

        if self.throttle.exceedRate():
            return True

        print(f"#messages {self.cnt} msg/s {self.cntPerSec}")
        self.cntPerSec = 0

        return True


# rcc subscribe --redis_url redis://localhost:7379 --channel foo


@click.command()
@click.option(
    '--redis-url', '-u', envvar='RCC_REDIS_URL', default='redis://localhost:30001'
)
@click.option('--password', '-a')
@click.option('--user')
@click.option('--channel', default='foo')
@click.option('--position')
def subscribe(redis_url, password, user, channel, position):
    '''Subscribe (with XREAD) to a channel'''

    redisClient = RedisClient(redis_url, password, user)

    try:
        runSubscriber(redisClient, channel, position, MessageHandlerClass)
    except Exception as e:
        backtrace = traceback.format_exc()
        logging.debug(f'traceback: {backtrace}')
        logging.error(f'subcribe error: {e}')
