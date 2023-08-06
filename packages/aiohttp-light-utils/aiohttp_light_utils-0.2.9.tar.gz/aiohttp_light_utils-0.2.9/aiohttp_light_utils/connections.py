import asyncio

try:
    import aioredis
except ImportError:
    pass

try:
    import sentry_sdk
except ImportError:
    pass

import ujson

try:
    from bson import json_util
except ImportError:
    pass

try:
    from motor.motor_asyncio import AsyncIOMotorClient
except ImportError:
    pass

try:
    from jsonrpcclient.clients.aiohttp_client import AiohttpClient
    from jsonrpcclient.exceptions import ReceivedErrorResponseError, ReceivedNon2xxResponseError
except ImportError:
    pass

from sentry_sdk.integrations.aiohttp import AioHttpIntegration

try:
    from aiokafka import AIOKafkaProducer
except ImportError:
    pass


import aiohttp

from .exceptions import RpcClientError


loop = asyncio.get_event_loop()


class AIOConnections:
    # Коннекты
    # HTTP-сессия
    _opt_http_session = None
    _opt_db = None
    _opt_cache = None
    _opt_broker_producer = None

    def __init__(self, db=None, raven_dsn=None, cache=None, broker_producer=None):
        self._db = db
        self._cache = cache
        self._raven_dsn = raven_dsn
        self._broker_producer = broker_producer

    async def init_connections(self):
        self._opt_http_session = aiohttp.ClientSession(json_serialize=ujson.dumps)

        if self._db:
            conn = AsyncIOMotorClient(self._db['url'])
            self._opt_db = conn[self._db['db_name']]

        if self._cache:
            self._opt_cache = await aioredis.create_redis_pool(
                self._cache['url'],
                db=self._cache['db_name'],
            )

        if self._raven_dsn:
            sentry_sdk.init(
                dsn=self._raven_dsn, integrations=[AioHttpIntegration()]
            )

        if self._broker_producer:
            self._opt_broker_producer = AIOKafkaProducer(
                loop=loop,
                bootstrap_servers=self._broker_producer['bootstrap_servers']
            )
            # Get cluster layout and initial topic/partition leadership information
            await self._opt_broker_producer.start()

    async def close_connections(self):
        if self._opt_http_session:
            await self._opt_http_session.close()

        if self._opt_db:
            self._opt_db.client.close()

        if self._opt_cache:
            self._opt_cache.close()
            await self._opt_cache.wait_closed()

        if self._opt_broker_producer:
            # Wait for all pending messages to be delivered or expire.
            await self._opt_broker_producer.stop()

    async def send_prc_message(self, domain, method, **kwargs):
        client = AiohttpClient(self.http_session, domain)
        try:
            response = await client.request(method, **kwargs)
        except ReceivedNon2xxResponseError as e:
            raise RpcClientError(code='unknown', status_code=e.code)
        except ReceivedErrorResponseError as e:
            if e.response.message == 'Server error':
                code = 'server_error'
            else:
                code = e.response.data.rsplit(':')[0]
            raise RpcClientError(code=code)
        r_data = json_util.loads(response.data.result)
        return r_data

    @property
    def http_session(self):
        return self._opt_http_session

    @property
    def db(self):
        if not self._opt_db:
            raise ValueError('Не заданы параметры подключения к БД')
        return self._opt_db

    @property
    def cache(self):
        if not self._opt_cache:
            raise ValueError('Не заданы параметры подключения к redis')
        return self._opt_cache

    @property
    def broker_producer(self):
        if not self._opt_broker_producer:
            raise ValueError('Не заданы параметры подключения к брокер prodicer')
        return self._opt_broker_producer


async def init_connections(app):
    connections = AIOConnections(
        db=app['config']['db'],
        cache=app['config']['cache'],
        raven_dsn=app['config']['raven_dsn'],
        broker_producer=app['config']['broker_producer']
    )

    await connections.init_connections()

    app['connections'] = connections


async def close_connections(app):
    await app['connections'].close_connections()
