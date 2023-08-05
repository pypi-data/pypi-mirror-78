'''Redis client

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.

TODO:
    RESP3 support (start by sending hello3) / then use hash types
'''

import asyncio
import logging

import hiredis

from rcc.hash_slot import getHashSlot
from rcc.pool import ConnectionPool

from rcc.commands.cluster import ClusterCommandsMixin
from rcc.commands.pubsub import PubSubCommandsMixin
from rcc.commands.generic import GenericCommandsMixin
from rcc.response import convertResponse


class RedisClient(ClusterCommandsMixin, PubSubCommandsMixin, GenericCommandsMixin):
    def __init__(
        self,
        url: str = None,
        password: str = None,
        user: str = None,
        multiplexing=False,
    ):
        self.url = url or 'redis://localhost:6379'

        # FIXME: do we need those member variables ?
        self.password = password
        self.user = user

        self.multiplexing = multiplexing

        self.urls = {}
        self.pool = ConnectionPool(password, user, self.multiplexing)
        self.connection = self.pool.get(self.url)
        self.cluster = False
        self.lock = asyncio.Lock()

    def __del__(self):
        '''
        It is a smell that we have to do this manually,
        but without it we get a big resource leak
        '''
        self.close()

    def close(self):
        self.pool.flush()

    @property
    def host(self):
        return self.connection.host

    @property
    def port(self):
        return self.connection.port

    async def connect(self):
        await self.connection.connect()

        try:
            info = await self.send('INFO')
        except hiredis.ReplyError:
            pass
        else:
            self.cluster = info.get('cluster_enabled') == '1'

        if self.cluster:
            await self.connect_cluster_nodes()

    def connected(self):
        return self.connection.connected()

    async def connect_cluster_nodes(self):
        nodes = await self.cluster_nodes()
        for node in nodes:
            if node.role == 'master':
                url = f'redis://{node.ip}:{node.port}'
                for slot in node.slots:
                    self.urls[slot] = url

    async def readResponse(self, connection):
        response = await connection.readResponse()
        return response

    async def getConnection(self, key):
        hashSlot = None
        if key is not None:
            hashSlot = getHashSlot(key)

        url = self.urls.get(hashSlot, self.url)

        connection = self.pool.get(url)

        msg = f'key {key} -> slot {hashSlot}'
        msg += f' -> connection {connection.host}:{connection.port}'
        logging.debug(msg)

        return connection

    def findKey(self, cmd, *args):
        '''Find where the key lives in a command, so that it can be hashed
        with crc16.
        '''

        if cmd in ('XREAD', 'XREADGROUP'):
            idx = -1
            for i, arg in enumerate(args):
                if arg in (b'STREAMS', 'STREAMS'):
                    idx = i

            if idx == -1:
                raise ValueError(f"{cmd} arguments '{args}' do not contain STREAMS")
            else:
                idx = idx + 1
            key = args[idx]
        elif cmd in ('XGROUP', 'XINFO'):
            key = args[1]
        else:
            key = None if len(args) == 0 else args[0]

        return key

    async def send(self, cmd, *args, **kargs):
        '''Small wrapper to be able to disconnect on error
        1. to avoid resource leaks
        2. to handle redis cluster re-configuring itself
        '''
        try:
            # We need to extract the key to hash it in cluster mode
            # key is at different spot than first args for
            # some commands such as STREAMS
            key = kargs.get('key')
            if key is None:
                key = self.findKey(cmd, *args)

            return await self.doSend(cmd, key, *args)
        except asyncio.CancelledError:
            raise
        except Exception:
            self.close()
            raise

    async def doSend(self, cmd, key, *args):
        '''Send a command to the redis server.
        Handle cluster mode redirects with the MOVE response
        '''
        attempts = 10

        async with self.lock:
            while attempts > 0:
                # we should optimize this for the common case
                connection = await self.getConnection(key)

                await connection.send(cmd, *args)
                response = await self.readResponse(connection)

                responseType = type(response)
                if responseType != hiredis.ReplyError:
                    return convertResponse(response, cmd)

                attempts -= 1

                responseStr = str(response)
                if responseStr.startswith('MOVED'):
                    tokens = responseStr.split()
                    slotStr = tokens[1]
                    slot = int(slotStr)
                    url = tokens[2]
                    url = 'redis://' + url

                    self.urls[slot] = url
                else:
                    raise response

        raise ValueError(f'Error sending command, too many redirects: {cmd} {args}')

    def __repr__(self):
        return f'<RedisClient at {self.host}:{self.port}>'
